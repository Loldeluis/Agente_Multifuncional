import json
import subprocess
import os
import shutil
from typing import Optional
from config.settings import (
    GEMMA_MODEL,
    OLLAMA_URL,
    OLLAMA_TIMEOUT
)

try:
    import requests
except ImportError:
    requests = None


# ==============================
# CONFIGURACIÓN
# ==============================

MODEL = GEMMA_MODEL
OLLAMA_URL = OLLAMA_URL
OLLAMA_TIMEOUT = OLLAMA_TIMEOUT


# ==============================
# CONSULTA HTTP A OLLAMA
# ==============================
def _try_http(
    prompt: str,
    model: str = MODEL,
    timeout: int = 600,
    format_json: bool = False,
    options: Optional[dict] = None
) -> Optional[str]:

    if requests is None:
        return None

    url = f"{OLLAMA_URL}/api/generate"

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }

    if format_json:
        payload["format"] = "json"

    if options:
        payload["options"] = options

    try:

        response = requests.post(
            url,
            json=payload,
            timeout=timeout
        )

        # Mostrar el error real de Ollama
        if response.status_code != 200:

            print(
                "\n❌ ERROR RESPONDIDO POR OLLAMA"
            )

            print(
                f"Status: {response.status_code}"
            )

            print(
                f"Respuesta: {response.text}"
            )

            return None

        data = response.json()

        return data.get("response")

    except requests.exceptions.Timeout:

        print(
            "\n⏳ Ollama tardó demasiado en responder."
        )

        return None

    except requests.exceptions.ConnectionError:

        print(
            "\n🔌 No fue posible conectar con Ollama."
        )

        return None

    except Exception as e:

        print(
            f"\n❌ Error inesperado con Ollama: {e}"
        )

        return None

# ==============================
# FALLBACK CLI
# ==============================

def _try_cli(
    prompt: str,
    model: str = MODEL,
    timeout: int = 400
) -> Optional[str]:
    """
    Intenta consultar Ollama mediante la CLI.
    Solo se utiliza como respaldo para respuestas de texto.
    """

    ollama_cmd = os.environ.get("OLLAMA_PATH")

    if not ollama_cmd:
        ollama_cmd = (
            shutil.which("ollama")
            or shutil.which("ollama.exe")
        )

    if not ollama_cmd:
        return None

    try:
        proc = subprocess.run(
            [
                ollama_cmd,
                "run",
                model
            ],
            input=prompt,
            capture_output=True,
            text=True,
            timeout=timeout,
            encoding="utf-8"
        )

        if proc.returncode == 0:
            respuesta = proc.stdout.strip()

            if respuesta:
                return respuesta

    except subprocess.TimeoutExpired:
        print("\nGemma tardó demasiado usando la CLI.\n")

    except Exception as e:
        print(f"\nError usando Ollama CLI: {e}\n")

    return None


# ==============================
# CONSULTA GENERAL
# ==============================

def consultar_gemma(
    prompt: str,
    model: str = MODEL,
    formato_json: bool = False,
    opciones: Optional[dict] = None
) -> str:
    """
    Consulta Gemma mediante Ollama.

    Estrategia:
    1. API HTTP.
    2. Si es texto normal y falla HTTP, intenta CLI.
    3. Si se solicita JSON, NO usa CLI para evitar
       respuestas sin formato estructurado.
    """

    # 1. Intentar API HTTP
    respuesta = _try_http(
        prompt,
        model=model,
        format_json=formato_json,
        options=opciones
    )

    if respuesta:
        return respuesta

    # 2. Solo usar CLI para texto normal
    if not formato_json:

        respuesta = _try_cli(
            prompt,
            model=model
        )

        if respuesta:
            return respuesta

    # 3. Error final
    raise ConnectionError(
        f"No fue posible obtener una respuesta de Ollama "
        f"usando el modelo '{model}'.\n\n"
        "Comprueba:\n"
        "1. Ejecuta: ollama list\n"
        "2. Verifica que el modelo esté instalado.\n"
        "3. Ejecuta: ollama ps\n"
        "4. Comprueba que Ollama esté disponible en el puerto 11434."
    )


# ==============================
# LIMPIEZA DE RESPUESTA JSON
# ==============================

def _limpiar_json(texto: str) -> str:
    """
    Limpia una posible respuesta de Gemma antes
    de convertirla a JSON.
    """

    texto = texto.strip()

    # Eliminar bloques Markdown
    if texto.startswith("```json"):
        texto = texto[7:]

    elif texto.startswith("```"):
        texto = texto[3:]

    if texto.endswith("```"):
        texto = texto[:-3]

    return texto.strip()


# ==============================
# CONSULTA JSON
# ==============================

def consultar_gemma_json(
    prompt: str,
    model: str = MODEL,
    opciones: Optional[dict] = None
) -> dict:
    """
    Consulta Gemma solicitando JSON estructurado
    y lo convierte en un diccionario Python.
    """

    respuesta = consultar_gemma(
        prompt,
        model=model,
        formato_json=True,
        opciones=opciones
    )

    if not respuesta:
        raise ValueError(
            "Gemma devolvió una respuesta vacía."
        )

    texto = _limpiar_json(respuesta)

    try:
        resultado = json.loads(texto)

        # Verificamos que realmente sea un objeto JSON
        if not isinstance(resultado, dict):
            raise ValueError(
                "Gemma devolvió JSON válido, "
                "pero no devolvió un objeto/diccionario."
            )

        return resultado

    except json.JSONDecodeError as e:

        print("\n========== RESPUESTA RAW DE GEMMA ==========")
        print(texto)
        print("============================================\n")

        raise ValueError(
            f"Gemma devolvió un JSON inválido: {e}"
        ) from e