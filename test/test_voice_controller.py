from agents.voice_controller import (
    ejecutar_comando_voz
)


print("\n================================")
print("   ASISTENTE DE VOZ V2.0")
print("================================")

print(
    "\nWhisper se cargará una sola vez."
)


while True:

    input(
        "\nPresiona ENTER para hablar..."
    )

    resultado = ejecutar_comando_voz(
        duracion=7
    )

    print("\n📦 Resultado:")

    print(resultado)

    continuar = input(
        "\n¿Deseas dar otro comando? (s/n): "
    ).strip().lower()

    if continuar != "s":

        print(
            "\n👋 Finalizando asistente..."
        )

        break