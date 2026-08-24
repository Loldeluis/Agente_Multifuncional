import os
import json
import base64

from services.gemma_service import consultar_gemma


def procesar_imagen(ruta_imagen: str) -> dict:
    """
    Envía una imagen a Gemma 3 mediante Ollama y devuelve
    la información analizada en formato JSON.
    """

    if not os.path.exists(ruta_imagen):
        raise FileNotFoundError(
            f"No se encontró la imagen: {ruta_imagen}"
        )

    # Leer y convertir la imagen a Base64
    with open(ruta_imagen, "rb") as archivo:
        imagen_base64 = base64.b64encode(
            archivo.read()
        ).decode("utf-8")

    prompt = """
Analiza cuidadosamente la imagen proporcionada.

Extrae únicamente información que realmente esté presente
en la imagen.

Devuelve exclusivamente un JSON válido con esta estructura:

{
    "fuente": "imagen",
    "tipo_contenido": "",
    "descripcion_general": "",
    "texto_detectado": [],
    "objetos_detectados": [],
    "datos_relevantes": {},
    "nivel_confianza": ""
}

Reglas:
- No inventes información.
- Si no puedes identificar un dato, usa null.
- texto_detectado debe ser una lista.
- objetos_detectados debe ser una lista.
- Devuelve únicamente JSON.
"""

    # Por ahora usamos la API de Ollama directamente
    # porque necesitamos enviar la imagen junto al prompt.
    import requests

    payload = {
        "model": "gemma3:4b",
        "prompt": prompt,
        "images": [imagen_base64],
        "stream": False,
        "format": "json"
    }

    response = requests.post(
        "http://127.0.0.1:11434/api/generate",
        json=payload,
        timeout=(10, 300)
    )

    response.raise_for_status()

    respuesta = response.json()["response"]

    return json.loads(respuesta)