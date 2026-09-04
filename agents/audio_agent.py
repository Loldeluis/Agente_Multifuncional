import json

try:
    import whisper
except Exception as exc:  # pragma: no cover - local native environment issue
    whisper = None
    _WHISPER_IMPORT_ERROR = exc
else:
    _WHISPER_IMPORT_ERROR = None

from services.gemma_service import consultar_gemma_json


# Cargar modelo una sola vez
if whisper is not None:
    modelo_whisper = whisper.load_model("base")
else:
    modelo_whisper = None


def procesar_audio(ruta_audio: str) -> dict:
    """
    Procesa un audio:
    
    Audio → Whisper → Transcripción → Gemma → JSON
    """

    if whisper is None:
        raise RuntimeError(
            "Whisper no está disponible en este entorno. "
            "La librería nativa de Whisper/Numba falló al cargar. "
            "Recrea el entorno con Python 3.11/3.12 o reinstala Whisper."
        ) from _WHISPER_IMPORT_ERROR

    print("[1/4] Transcribiendo audio...")

    resultado_whisper = modelo_whisper.transcribe(
        ruta_audio,
        language="es"
    )

    transcripcion = resultado_whisper["text"].strip()

    print("[2/4] Transcripción obtenida:")
    print(transcripcion)

    prompt = f"""
Analiza la siguiente transcripción de audio.

TRANSCRIPCIÓN:

{transcripcion}

Extrae la información relevante y devuelve únicamente
un JSON válido con esta estructura:

{{
    "fuente": "audio",
    "transcripcion": "",
    "resumen": "",
    "temas_detectados": [],
    "datos_relevantes": {{}},
    "nivel_confianza": ""
}}

Reglas:

- No inventes información.
- Utiliza únicamente información presente en la transcripción.
- "temas_detectados" debe ser una lista.
- "datos_relevantes" debe ser un objeto JSON.
- Devuelve únicamente JSON válido.
"""

    print("[3/4] Analizando transcripción con Gemma...")

    resultado_gemma = consultar_gemma_json(prompt)

    resultado_gemma["transcripcion"] = transcripcion

    print("[4/4] Análisis de audio completado.")

    return resultado_gemma