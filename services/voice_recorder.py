import os

import sounddevice as sd
from scipy.io.wavfile import write


SAMPLE_RATE = 16000
CHANNELS = 1


def grabar_audio(
    ruta_salida: str,
    duracion: int = 7
):
    """
    Graba audio desde el micrófono y lo guarda
    como archivo WAV.
    """

    print("\n🎙️ Preparando micrófono...")
    print(f"Duración: {duracion} segundos")

    try:

        print("\n🎙️ Grabando...")

        audio = sd.rec(
            int(duracion * SAMPLE_RATE),
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            dtype="int16"
        )

        sd.wait()

    except Exception as e:

        raise RuntimeError(
            f"No fue posible acceder al micrófono: {e}"
        )

    carpeta = os.path.dirname(ruta_salida)

    if carpeta:
        os.makedirs(
            carpeta,
            exist_ok=True
        )

    write(
        ruta_salida,
        SAMPLE_RATE,
        audio
    )

    print("\n✅ Grabación finalizada.")
    print(f"📁 Archivo: {ruta_salida}")

    return ruta_salida