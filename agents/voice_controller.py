from services.voice_recorder import (
    grabar_audio_hasta_silencio
)

from services.whisper_service import (
    transcribir_audio
)

from agents.voice_agent import (
    interpretar_comando
)

from agents.orchestrator_agent import (
    ejecutar_intencion
)

from agents.agent_executor import (
    ejecutar_agente
)

from config.settings import (
    VOICE_TEMP_PATH
)

def ejecutar_comando_voz():
    """
    Ejecuta el flujo completo de voz:

    Micrófono
        ↓
    Detección automática de silencio
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

    print("\n🎙️ Paso 1/5 - Escuchando comando...")

    grabar_audio_hasta_silencio(
        ruta_salida=VOICE_TEMP_PATH
    )

    # ==========================================
    # 2. TRANSCRIBIR
    # ==========================================

    print("\n🧠 Paso 2/5 - Procesando voz...")

    texto = transcribir_audio(
        ruta_audio=VOICE_TEMP_PATH,
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