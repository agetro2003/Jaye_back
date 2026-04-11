from magenta.models.melody_rnn import melody_rnn_sequence_generator
from magenta.models.shared import sequence_generator_bundle
import note_seq
from pathlib import Path
import tempfile
import os
import subprocess
from note_seq.protobuf import generator_pb2
import urllib.request
import re

#Modelo de IA para generar propuestas musicales a partir de un texto ABC
_MELODY_RNN_MODEL = None

def get_model(): 
    global _MELODY_RNN_MODEL
    if _MELODY_RNN_MODEL is None:
        model_name = 'basic_rnn.mag'
        model_path = Path("AI_models").resolve()
        model_path.mkdir(exist_ok=True)
        model_file = model_path / model_name    

        if not model_file.is_file():
            print(f"Descargando modelo {model_name}...")
            url = f"http://download.magenta.tensorflow.org/models/{model_name}"
            urllib.request.urlretrieve(url, model_file)
            print(f"Modelo {model_name} descargado y guardado en {model_file}")
        
        print(f"Cargando modelo {model_name}...")
        bundle = sequence_generator_bundle.read_bundle_file(str(model_file))
        generator_map = melody_rnn_sequence_generator.get_generator_map()
        _MELODY_RNN_MODEL = generator_map['basic_rnn'](checkpoint=None, bundle=bundle)
        _MELODY_RNN_MODEL.initialize()
        print(f"Modelo {model_name} cargado y listo para usar.")

    return _MELODY_RNN_MODEL


def remove_initial_rests(abc_text: str) -> str:
    lines = abc_text.splitlines()
    # saltar todas las líneas que sean solo silencios al inicio
    i = 0
    while i < len(lines) and re.match(r'^z\d*\|', lines[i].strip()):
        i += 1

    lines[i] = re.sub(r"^z\d*\s*", "", lines[i])
    
    return "\n".join(lines[i:]).strip()

def remove_abc_header(abc_text: str) -> str:
    """
    Elimina las líneas de cabecera de un ABC generado por midi2abc,
    devolviendo solo las notas/compases.
    """
    lines = abc_text.splitlines()
    body_lines = []

    for line in lines:
        # Saltar líneas de cabecera y comentarios
        if line.startswith(("X:", "T:", "M:", "L:", "K:", "Q:", "%", "V:", "%%")):
            continue
        body_lines.append(line)

    return "\n".join(body_lines).strip()



def generate_proposals(abc_text, bars=4, num_variations=3, temperature=1.0):
    model = get_model()
    proposals = []

# Convertimos el ABC a MIDI usando un archivo temporal para evitar problemas de concurrencia 
    with tempfile.NamedTemporaryFile(suffix=".abc", delete=False) as temp_abc_in, \
         tempfile.NamedTemporaryFile(suffix=".mid", delete=False) as temp_mid_in:
        temp_abc_in.write(abc_text.encode('utf-8'))
        temp_abc_in.flush()

        subprocess.run(["abc2midi", temp_abc_in.name, "-o", temp_mid_in.name], check=True)

        input_sequence = note_seq.midi_file_to_note_sequence(temp_mid_in.name)
    
    #limpiar archivos temporales
    os.remove(temp_abc_in.name)
    os.remove(temp_mid_in.name)

    # Configuracion de generación
    qpm = input_sequence.tempos[0].qpm if input_sequence.tempos else 120
    seconds_per_step = 60.0 / qpm / model.steps_per_quarter

    total_steps = bars * model.steps_per_quarter * 4  # 4/4 time signature
    duration_to_generate = total_steps * seconds_per_step

    last_end_time = max(note.end_time for note in input_sequence.notes) if input_sequence.notes else 0

    # Generar variaciones
    for _ in range (num_variations): 
        generator_options = generator_pb2.GeneratorOptions()
        generator_options.args['temperature'].float_value = temperature
        generator_options.generate_sections.add(
            start_time=last_end_time,
            end_time=last_end_time + duration_to_generate
        )

        generated_sequence = model.generate(input_sequence, generator_options)
        
        # Usamos un archivo temporal para convertir el resultado a ABC
        with tempfile.NamedTemporaryFile(suffix=".mid", delete=False) as temp_mid_out: 
            note_seq.sequence_proto_to_midi_file(generated_sequence, temp_mid_out.name)
            result = subprocess.run(["midi2abc", temp_mid_out.name], capture_output=True, text=True, check=True)
            raw_new_abc = result.stdout
        
        os.remove(temp_mid_out.name)

        clean_abc = remove_abc_header(raw_new_abc)
        clean_abc = remove_initial_rests(clean_abc)

        # separamos las propuestas de la entrada original
        bar_list = [c.strip() for c in clean_abc.split("|") if c.strip()]

        if len(bar_list) > bars:
            new_bar = bar_list[bars:]
            proposal = "|".join(new_bar)+" |]"
        else: 
            proposal = clean_abc
        proposals.append(proposal)

        

    return proposals