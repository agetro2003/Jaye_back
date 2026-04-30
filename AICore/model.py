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
import traceback 

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

def escape_chords_for_magenta(abc_text: str) -> str:
    """
    Convierte los acordes entre comillas ("Em") a "^Em" para que Magenta
    no los interprete como acordes, pero mantiene las comillas para la partitura.
    """
    def replacer(match):
        chord = match.group(1)
        return f'"^{chord}"'

    # Reemplaza "Em" → "^Em", "D7" → "^D7", etc.
    escaped = re.sub(r'"([^"]+)"', replacer, abc_text)
    return escaped



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

    # 1. Creamos archivos temporales de forma segura y cerramos el "candado" de Python
    fd_abc, path_abc_in = tempfile.mkstemp(suffix=".abc")
    fd_mid, path_mid_in = tempfile.mkstemp(suffix=".mid")
    os.close(fd_abc)
    os.close(fd_mid)

    try:

        safe_abc = escape_chords_for_magenta(abc_text)
        # Escribimos el ABC
        with open(path_abc_in, 'w', encoding='utf-8') as f:
            f.write(safe_abc)

        # 2. abc2midi: Capturamos errores para saber por qué falla
        try:
            subprocess.run(["abc2midi", path_abc_in, "-o", path_mid_in], check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ Error crítico en abc2midi: {e.stderr}")
            raise Exception(f"Fallo en abc2midi: {e.stderr}")

        # Leemos el MIDI a NoteSequence
        input_sequence = note_seq.midi_file_to_note_sequence(path_mid_in)
        
        # Configuración de generación
        qpm = input_sequence.tempos[0].qpm if input_sequence.tempos else 120
        seconds_per_step = 60.0 / qpm / model.steps_per_quarter
        total_steps = bars * model.steps_per_quarter * 4
        duration_to_generate = total_steps * seconds_per_step
        last_end_time = max(note.end_time for note in input_sequence.notes) if input_sequence.notes else 0

        # Generar variaciones
        for _ in range(num_variations): 
            generator_options = generator_pb2.GeneratorOptions()
            generator_options.args['temperature'].float_value = temperature
            generator_options.generate_sections.add(
                start_time=last_end_time,
                end_time=last_end_time + duration_to_generate
            )

            generated_sequence = model.generate(input_sequence, generator_options)
            
            # 3. Archivo temporal para la salida de la IA
            fd_out, path_mid_out = tempfile.mkstemp(suffix=".mid")
            os.close(fd_out)

            try:
                note_seq.sequence_proto_to_midi_file(generated_sequence, path_mid_out)
                result = subprocess.run(["midi2abc", path_mid_out], capture_output=True, text=True, check=True)
                raw_new_abc = result.stdout
            except subprocess.CalledProcessError as e:
                print(f"❌ Error crítico en midi2abc: {e.stderr}")
                raise Exception(f"Fallo en midi2abc: {e.stderr}")
            finally:
                if os.path.exists(path_mid_out): os.remove(path_mid_out)

            clean_abc = remove_abc_header(raw_new_abc)
            clean_abc = remove_initial_rests(clean_abc)

            # Extraemos los compases nuevos
            bar_list = [c.strip() for c in clean_abc.split("|") if c.strip()]
            if len(bar_list) > bars:
                new_bar = bar_list[-bars:]
                proposal = "|".join(new_bar) + " |]"
            else: 
                proposal = clean_abc
            
            proposals.append(proposal)

    except Exception as e:
        print("\n=== ERROR INTERNO EN LA GENERACIÓN DE IA ===")
        traceback.print_exc()
        print("============================================\n")
        raise e
        
    finally:
        # Limpieza segura final
        if os.path.exists(path_abc_in): os.remove(path_abc_in)
        if os.path.exists(path_mid_in): os.remove(path_mid_in)

    return proposals