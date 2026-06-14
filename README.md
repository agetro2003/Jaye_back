# ⚙️ Jaye - Backend API (FastAPI & Magenta AI)

Este repositorio contiene la API RESTful y el motor de Inteligencia Artificial que da vida a **Jaye**, la plataforma web de composición musical asistida. 

Este backend utiliza **Google Magenta (TensorFlow)** con un modelo RNN (Recurrent Neural Network) para predecir y generar secuencias musicales reales. Además, implementa un pipeline de conversión bidireccional entre texto (Notación ABC) y audio (MIDI) utilizando binarios del sistema.

Este proyecto forma parte de un Trabajo de Fin de Máster (TFM) y se distribuye bajo la licencia MIT.

## ✨ Características Principales

* **Autenticación y Seguridad:** Sistema de login/registro utilizando JSON Web Tokens (JWT), passlib y bcrypt para el cifrado seguro de contraseñas.
* **Arquitectura RESTful:** Endpoints estructurados (`/auth`, `/users`, `/folders`, `/songs`) para la gestión completa del CRUD de usuarios y composiciones.
* **Motor de IA Musical (Magenta):** Integración del modelo `basic_rnn.mag` de Magenta para generar variaciones de melodías continuadas, ajustables mediante temperatura (creatividad).
* **Pipeline ABC <-> MIDI:** Procesamiento de archivos en tiempo real. Utiliza `abcmidi` para convertir la notación ABC del usuario a archivos `.mid`, alimentarlos a la IA, y realizar ingeniería inversa (`midi2abc`) para devolver la partitura generada.
* **Base de Datos Relacional:** Persistencia de datos en PostgreSQL gestionada con SQLAlchemy.

## 🛠️ Stack Tecnológico

* **Framework API:** FastAPI / Uvicorn
* **Base de Datos:** PostgreSQL / psycopg2-binary
* **Inteligencia Artificial:** Magenta, note-seq, TensorFlow
* **Dependencias de Sistema:** abcmidi, ffmpeg, libasound2-dev 
* **Contenedorización:** Docker (python:3.8-slim) 

## 🚀 Instalación y Ejecución (Recomendado: Docker)

Debido a que el modelo de IA y el conversor de partituras requieren dependencias directas del sistema operativo (`abcmidi` y librerías de audio ), **la ejecución mediante Docker es el método oficial y recomendado** para garantizar que el entorno funcione perfectamente en cualquier máquina.

### 1. Requisitos Previos
* Tener instalado [Docker](https://www.docker.com/) y Docker Compose.
* Una base de datos PostgreSQL (local o en la nube como Supabase).

### 2. Configuración del Entorno
Clona el repositorio y crea un archivo `.env` en la raíz del proyecto con la conexión a tu base de datos:
```env
DATABASE_URL=postgresql://usuario:contraseña@host:puerto/nombre_bd
```

### 3. Construir y Levantar el Contenedor
[cite_start]Ejecuta el siguiente comando para compilar la imagen (esto instalará Python 3.8, los compiladores de audio y las librerías de Python automáticamente) y arrancar el servidor exponiendo el puerto 8000[cite: 4, 7]:

```bash
docker build -t jaye-backend .
docker run -p 8000:8000 --env-file .env jaye-backend
```

La API estará disponible en `http://localhost:8000`. 
Puedes explorar y probar todos los endpoints en la documentación interactiva (Swagger) entrando a `http://localhost:8000/docs`.

## 🧪 Pruebas Internas

El repositorio incluye un script de validación del pipeline del sistema (`test.py`) que comprueba la correcta instalación de las herramientas de compilación musical. Puedes ejecutarlo dentro del contenedor para verificar que `abc2midi` y `midi2abc` funcionan correctamente en el sistema anfitrión.
