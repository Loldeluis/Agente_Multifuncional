# Agente Multimodal

Sistema de inteligencia artificial basado en agentes especializados para procesar imagen, audio y comandos de voz. El proyecto convierte la informacion multimodal en JSON estructurado, consolida los resultados con Gemma ejecutado localmente, genera informes en PDF y construye grafos de conocimiento.

La version actual incorpora un asistente de voz capaz de interpretar una instruccion, decidir que agente debe ejecutarla y devolver el resultado correspondiente.

## Vista general

```text
Usuario -> Voice Controller -> Whisper -> Voice Agent
                                      -> Orchestrator -> Agent Executor
                                                           |
             +--------------------+------------------------+----------------+
             v                    v                        v                v
        Image Agent         Audio Agent              Report Agent      Graph Agent
             |                    |                        |                |
             +-----------> Integration Agent               |        Knowledge Agent
                              |                             |                |
                              v                             v                v
                       consolidado.json                informe.json     knowledge.json
                                                            |                |
                                                            v                v
                                                    informe_voz.pdf       GraphML
```

## Que hace

- Analiza imagenes con Gemma 3 y devuelve texto, objetos, descripcion y datos relevantes.
- Transcribe audio en espanol mediante Whisper.
- Analiza la transcripcion y la convierte en informacion estructurada.
- Integra resultados de imagen y audio, identificando coincidencias, informacion exclusiva y contradicciones.
- Interpreta comandos de voz como `generar reporte del paciente Juan Perez`.
- Selecciona y ejecuta agentes especializados mediante un orquestador.
- Genera informes JSON y PDF.
- Extrae entidades y relaciones para crear un grafo de conocimiento en GraphML.
- Ejecuta Gemma localmente mediante Ollama, sin depender de una API de IA externa.

## Versiones

### V1.0: procesamiento multimodal

La primera version implementa el pipeline de procesamiento:

```text
Imagen -> Image Agent -> imagen.json
Audio  -> Audio Agent -> audio.json

imagen.json + audio.json -> Integration Agent -> consolidado.json
                                                     |
                                      +--------------+--------------+
                                      v                             v
                                Report Agent                  Knowledge Agent
                                      |                             |
                                      v                             v
                                informe.json                knowledge.json
                                      |                             |
                                      v                             v
                                 PDF Service                Graph Service
                                                                    |
                                                                    v
                                                       grafo_conocimiento.graphml
```

### V2.0: asistente de voz

La segunda version anade captura desde microfono, deteccion automatica de silencio, transcripcion con Whisper, interpretacion de intencion, orquestacion y ejecucion de agentes.

```text
Microfono -> deteccion de silencio -> Whisper -> Voice Agent
                                                   -> Orchestrator Agent
                                                   -> Agent Executor
                                                   -> agente especializado
                                                   -> resultado
```

## Tecnologias

| Tecnologia | Uso |
| --- | --- |
| Python | Lenguaje y coordinacion de componentes |
| Ollama | Ejecucion local y API HTTP del modelo |
| Gemma 3 `gemma3:4b` | Analisis multimodal, interpretacion, integracion y conocimiento |
| OpenAI Whisper | Transcripcion de audio en espanol |
| Requests | Comunicacion HTTP con Ollama |
| Ollama Python | Prueba directa de conexion con el modelo |
| NumPy | Procesamiento de muestras de audio |
| SoundDevice | Captura de audio desde el microfono |
| SciPy | Escritura de grabaciones WAV |
| NetworkX | Construccion de grafos dirigidos |
| GraphML | Formato portable para guardar grafos |
| ReportLab | Generacion de informes PDF |
| PyTorch | Motor utilizado por Whisper |

## Requisitos

- Python 3.10 o superior recomendado.
- Ollama instalado y ejecutandose.
- Modelo `gemma3:4b` descargado.
- FFmpeg instalado y disponible en el `PATH`.
- Microfono configurado para utilizar la V2.0.
- Memoria y capacidad suficientes para ejecutar Whisper y Gemma localmente.

El proyecto se ha probado en Windows usando PowerShell y un entorno virtual `.venv`. En equipos que ejecutan Gemma unicamente con CPU, las respuestas pueden tardar varios segundos.

## Instalacion

### 1. Clonar el repositorio

```powershell
git clone https://github.com/Loldeluis/Agente_Multifuncional.git
cd Agente_Multifuncional
```

### 2. Crear el entorno virtual

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Si PowerShell bloquea la activacion, utiliza directamente el interprete del entorno:

```powershell
.\.venv\Scripts\python.exe --version
```

### 3. Instalar dependencias

El archivo historico `requiriments.txt` contiene dependencias y comandos de prueba mezclados. Para instalar las librerias utilizadas por el codigo:

```powershell
python -m pip install --upgrade pip
python -m pip install requests ollama openai-whisper networkx reportlab numpy sounddevice scipy
```

Whisper puede requerir una instalacion especifica de PyTorch segun el sistema operativo y el soporte de GPU. Si la instalacion automatica falla, instala PyTorch siguiendo las instrucciones oficiales de tu plataforma y vuelve a instalar `openai-whisper`.

### 4. Instalar FFmpeg

En Windows, una opcion es:

```powershell
winget install Gyan.FFmpeg.Shared
```

Comprueba la instalacion:

```powershell
ffmpeg -version
```

### 5. Instalar y preparar Ollama

Instala Ollama desde [ollama.com/download](https://ollama.com/download), abre la aplicacion y descarga el modelo:

```powershell
ollama pull gemma3:4b
ollama list
```

La API debe estar disponible en `http://127.0.0.1:11434`. Puedes probar el modelo con:

```powershell
ollama run gemma3:4b
```

## Ejecucion principal

El punto de entrada actual es `main.py` y ejecuta el asistente de voz V2.0:

```powershell
.\.venv\Scripts\python.exe main.py
```

El programa muestra el banner, espera ENTER, graba desde el microfono, detiene la grabacion despues del silencio configurado, transcribe el audio, detecta la intencion, selecciona el agente y ejecuta la accion.

Para cerrar el programa, utiliza `Ctrl+C`. Si el sistema pregunta si deseas dar otro comando, responde `n`.

## Comandos de voz

El `Voice Agent` reconoce estas intenciones:

| Intencion | Ejemplo |
| --- | --- |
| `generar_reporte` | Genera un reporte del paciente Juan Perez |
| `consultar_grafo` | Consulta el grafo de Juan Perez |
| `analizar_informacion` | Analiza la informacion disponible |
| `procesar_imagen` | Procesa la imagen |
| `procesar_audio` | Procesa el audio |
| `desconocido` | Se usa cuando no se identifica una accion valida |

El comando se convierte en un objeto como este:

```json
{
  "intencion": "generar_reporte",
  "datos": {
    "paciente": "Juan Perez"
  }
}
```

El agente de voz interpreta la orden, pero no ejecuta acciones directamente. La decision corresponde al `Orchestrator Agent` y la ejecucion al `Agent Executor`.

## Ejecucion por etapas

Para probar el pipeline V1.0 sin utilizar el controlador de voz, ejecuta desde la raiz:

```powershell
.\.venv\Scripts\python.exe .\prueba_gemma.py
.\.venv\Scripts\python.exe -m test.test_image_agent
.\.venv\Scripts\python.exe -m test.test_audio_agent
.\.venv\Scripts\python.exe -m test.test_integration_agent
.\.venv\Scripts\python.exe -m test.test_report_agent
.\.venv\Scripts\python.exe -m test.test_graph_agent
.\.venv\Scripts\python.exe -m test.test_knowledge_agent
```

Los archivos de entrada de ejemplo son `data/input/prueba.jpg` y `data/input/prueba.mp3`. Las etapas generan resultados en `data/output/`:

| Archivo | Descripcion |
| --- | --- |
| `imagen.json` | Analisis estructurado de la imagen |
| `audio.json` | Transcripcion y analisis del audio |
| `consolidado.json` | Integracion de las fuentes |
| `informe.json` | Informe estructurado generado por Gemma |
| `informe_final.pdf` | Informe PDF de la V1.0 |
| `informe_voz.pdf` | Informe generado desde el flujo de voz |
| `knowledge.json` | Entidades y relaciones extraidas |
| `grafo.graphml` | Grafo simple de datos consolidados |
| `grafo_conocimiento.graphml` | Grafo dirigido de entidades y relaciones |

Las grabaciones temporales se guardan en `data/temp/` y estan excluidas del control de versiones.

## Estructura del proyecto

```text
Agente_Multifuncional/
|-- main.py                         Entrada principal V2.0
|-- prueba_gemma.py                 Prueba directa de Ollama
|-- requiriments.txt                Dependencias y comandos originales
|-- .gitignore
|
|-- agents/
|   |-- image_agent.py              Analisis de imagenes
|   |-- audio_agent.py              Transcripcion y analisis de audio
|   |-- integration_agent.py        Consolidacion de resultados
|   |-- report_agent.py             Generacion de informes
|   |-- knowledge_agent.py          Extraccion de conocimiento
|   |-- graph_agent.py              Creacion de grafo simple
|   |-- voice_agent.py              Interpretacion de comandos
|   |-- orchestrator_agent.py       Seleccion de agente y accion
|   |-- agent_executor.py           Ejecucion de la decision
|   `-- voice_controller.py         Coordinacion del flujo de voz
|
|-- services/
|   |-- gemma_service.py            Cliente HTTP/CLI de Ollama
|   |-- whisper_service.py          Carga y uso de Whisper
|   |-- voice_recorder.py           Grabacion y deteccion de silencio
|   |-- file_service.py             Escritura de JSON
|   |-- pdf_service.py              Generacion de PDF
|   |-- graph_service.py            Construccion y guardado de grafos
|   `-- agent_result.py              Resultado comun de agentes
|
|-- config/
|   `-- settings.py                 Configuracion centralizada
|
|-- data/
|   |-- input/                      Archivos de entrada
|   |-- output/                     Resultados generados
|   `-- temp/                       Grabaciones temporales
|
|-- test/                           Scripts de prueba ejecutables
|-- docs/                           Documentacion tecnica ampliada
`-- graphs/                         Paquete relacionado con grafos
```

## Configuracion

La configuracion esta centralizada en `config/settings.py` e incluye el modelo y URL de Ollama, el modelo y lenguaje de Whisper, los parametros del microfono, el umbral y duracion del silencio, la duracion maxima de grabacion y las rutas de salida.

El servicio de Gemma utiliza la API HTTP primero. Para consultas de texto normales puede utilizar la CLI como respaldo. La variable opcional `OLLAMA_PATH` permite indicar manualmente la ruta del ejecutable de Ollama si no esta disponible en el `PATH`.

## Pruebas

Los archivos de `test/` son scripts ejecutables con llamadas reales a Whisper, el microfono y Ollama; no forman una suite aislada basada en mocks.

Para probar la interpretacion sin grabar audio:

```powershell
.\.venv\Scripts\python.exe -m test.test_voice_agent
```

Las pruebas que acceden al microfono requieren interaccion del usuario. La primera carga de Whisper puede descargar el modelo `base` y tardar mas que las ejecuciones siguientes.

## Solucion de problemas

### Ollama no responde

Comprueba que Ollama este abierto y ejecuta:

```powershell
ollama list
ollama ps
```

### Gemma tarda mucho

Gemma puede ejecutarse al 100% de CPU y tardar varios segundos o minutos. No interrumpas el proceso mientras aparece `Analizando intencion...`.

### `KeyboardInterrupt`

Aparece cuando se presiona `Ctrl+C` mientras Whisper u Ollama estan trabajando. No representa necesariamente un error del modelo.

### Error de microfono o FFmpeg

Comprueba los permisos de microfono de Windows, el dispositivo seleccionado, la instalacion de FFmpeg y la existencia de los archivos de entrada.

### El programa repite la grabacion

El ciclo de `main.py` permite introducir varios comandos. El mensaje `Presiona ENTER para hablar...` vuelve a aparecer despues de cada resultado. Para detenerlo, utiliza `Ctrl+C`. No importes scripts de `test/` desde modulos de produccion porque ejecutan codigo inmediatamente al importarse.

### JSON invalido

Las respuestas estructuradas se solicitan con `format: json` y se validan en `gemma_service.py`. Aun asi, un modelo generativo puede producir una salida inesperada; revisa la respuesta RAW mostrada por el servicio y repite la etapa.

## Limitaciones

- La calidad depende de Gemma, Whisper, la imagen y la claridad del audio.
- La instruccion de no inventar datos reduce el riesgo de alucinaciones, pero no sustituye la revision humana.
- La ejecucion local puede consumir bastante memoria, CPU y almacenamiento.
- El grafo simple depende de `datos_consolidados`; el grafo de conocimiento depende de las entidades y relaciones extraidas.
- El proyecto no es todavia una aplicacion web, un servicio multiusuario ni un sistema de produccion.
- Los comandos de voz dependen de que el modelo identifique correctamente la intencion y los datos mencionados.

## Documentacion adicional

La carpeta [`docs/`](docs/) contiene explicaciones ampliadas:

- [Descripcion del proyecto](docs/00-Proyecto.md)
- [Arquitectura](docs/01-Arquitectura.md)
- [Image Agent](docs/02-Image-Agent.md)
- [Audio Agent](docs/03-Audio-Agent.md)
- [Integration Agent](docs/04-Integration-Agent.md)
- [Report Agent](docs/05-Report-Agent.md)
- [Knowledge Agent](docs/06-Knowledge-Agent.md)
- [Graph Service](docs/07-Graph-Service.md)
- [Pipeline completo](docs/08-Pipeline.md)
- [Cierre de la V1.0](docs/09-Version-1.0.md)

La documentacion especifica de voz se encuentra en [`docs/version-2.0/`](docs/version-2.0/).

## Estado del proyecto

**Version actual: 2.0**

- V1.0: completada.
- V2.0: implementada con interaccion por voz, grabacion inteligente, configuracion centralizada y ejecucion orquestada.
- V3.0: etapa experimental futura para memoria, herramientas externas, automatizacion, APIs e interfaces graficas.

## Consideraciones de privacidad

Los audios, imagenes y documentos pueden contener datos personales o clinicos. Utiliza datos de prueba o anonimizados, solicita las autorizaciones necesarias y no distribuyas informacion sensible sin aplicar controles de proteccion de datos.

## Autor

**Luis Maldonado**

Proyecto academico de Inteligencia Artificial y Sistemas Multiagente.
