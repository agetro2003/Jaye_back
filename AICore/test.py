import subprocess
import os

def test_abc_conversion():
    print("🤖 Iniciando prueba de abcmidi...")
    
    # 1. Creamos un texto ABC de prueba muy básico (Estrellita dónde estás)
    abc_content = """X:1
T:Prueba AI
M:4/4
L:1/4
K:C
C C G G | A A G2 | F F E E | D D C2 |]"""

    # 2. Guardamos el texto en un archivo
    with open("prueba.abc", "w") as f:
        f.write(abc_content)
        
    print("✅ Archivo prueba.abc creado.")

    try:
        # 3. Llamamos a abc2midi desde Python para convertirlo a MIDI
        # subprocess.run ejecuta comandos en la terminal como si fueras tú
        print("🎵 Convirtiendo ABC a MIDI...")
        subprocess.run(["abc2midi", "prueba.abc", "-o", "prueba.mid"], check=True)
        print("✅ Archivo prueba.mid generado con éxito.")
        
        # 4. (Opcional) Llamamos a midi2abc para hacer el camino inverso
        print("📜 Convirtiendo MIDI de vuelta a ABC...")
        result = subprocess.run(["midi2abc", "prueba.mid"], capture_output=True, text=True, check=True)
        print("✅ ¡Texto ABC recuperado con éxito desde el MIDI!\n")
        
        print("--- RESULTADO DEL MIDI2ABC ---")
        print(result.stdout)
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al ejecutar el comando: {e}")
    finally:
        # Limpiamos los archivos para no dejar basura
        if os.path.exists("prueba.abc"): os.remove("prueba.abc")
        if os.path.exists("prueba.mid"): os.remove("prueba.mid")

if __name__ == "__main__":
    test_abc_conversion()