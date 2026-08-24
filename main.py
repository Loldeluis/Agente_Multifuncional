from agents.image_agent import procesar_imagen
from agents.audio_agent import procesar_audio
from agents.integration_agent import integrar_datos
from agents.report_agent import generar_informe


def main():

    print("Procesando imagen...")

    datos_imagen = procesar_imagen(
        "data/input/imagen.jpg"
    )

    print(datos_imagen)

    print("\nProcesando audio...")

    datos_audio = procesar_audio(
        "data/input/audio.mp3"
    )

    print(datos_audio)

    print("\nIntegrando información...")

    datos = integrar_datos(
        datos_imagen,
        datos_audio
    )

    print("\nGenerando informe con Gemma...")

    informe = generar_informe(datos)

    print(informe)


if __name__ == "__main__":
    main()