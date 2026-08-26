import whisper


_modelo = None


def obtener_modelo(
    nombre_modelo: str = "base"
):
    """
    Carga Whisper una sola vez y reutiliza
    el modelo durante la ejecución del programa.
    """

    global _modelo

    if _modelo is None:

        print(
            f"\n🧠 Cargando Whisper ({nombre_modelo})..."
        )

        _modelo = whisper.load_model(
            nombre_modelo
        )

        print(
            "✅ Whisper cargado correctamente."
        )

    return _modelo


def transcribir_audio(
    ruta_audio: str,
    idioma: str = "es"
) -> str:
    """
    Transcribe un archivo de audio utilizando
    el modelo Whisper cargado en memoria.
    """

    modelo = obtener_modelo()

    print(
        "\n🎧 Transcribiendo audio..."
    )

    resultado = modelo.transcribe(
        ruta_audio,
        language=idioma,
        fp16=False
    )

    return resultado["text"].strip()