from services.voice_recorder import grabar_audio
from services.whisper_service import transcribir_audio

from agents.voice_agent import interpretar_comando
from agents.orchestrator_agent import ejecutar_intencion
from agents.agent_executor import ejecutar_agente


RUTA_AUDIO = "data/temp/voz_actual.wav"


def ejecutar_comando_voz(
    duracion: int = 7
):
    """
    Ejecuta el flujo completo:

    Micrófono
        ↓
    Whisper
        ↓
    Voice Agent
        ↓
    Orchestrator
        ↓
    Agent Executor
    """

    print("\n================================")
    print("       VOICE CONTROLLER")
    print("================================")

    # ==========================================
    # 1. GRABAR
    # ==========================================

    print("\n🎙️ Paso 1/5 - Capturando voz...")

    grabar_audio(
        RUTA_AUDIO,
        duracion=duracion
    )

    # ==========================================
    # 2. TRANSCRIBIR
    # ==========================================

    print("\n🧠 Paso 2/5 - Procesando voz...")

    texto = transcribir_audio(
        RUTA_AUDIO,
        idioma="es"
    )

    print("\n📝 Transcripción:")
    print("--------------------------------")
    print(texto)
    print("--------------------------------")

    if not texto:
        raise ValueError(
            "Whisper no detectó ningún texto."
        )

    # ==========================================
    # 3. VOICE AGENT
    # ==========================================

    print("\n🤖 Paso 3/5 - Analizando intención...")

    intencion = interpretar_comando(
        texto
    )

    print("\n🎯 Intención detectada:")
    print(intencion)

    # ==========================================
    # 4. ORCHESTRATOR
    # ==========================================

    print("\n🧠 Paso 4/5 - Orquestando...")

    decision = ejecutar_intencion(
        intencion
    )

    print("\n🚦 Decisión:")
    print(decision)

    # ==========================================
    # 5. EXECUTOR
    # ==========================================

    print("\n⚙️ Paso 5/5 - Ejecutando agente...")

    resultado_final = ejecutar_agente(
        agente=decision["agente"],
        accion=decision["accion"],
        datos=decision["datos"]
    )

    print("\n================================")
    print("       RESULTADO FINAL")
    print("================================")

    print(resultado_final)

    return resultado_final