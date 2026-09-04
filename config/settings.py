# ==========================================
# CONFIGURACIN GENERAL
# ==========================================

PROJECT_NAME = "Agente Multimodal"

# ==========================================
# GEMMA / OLLAMA
# ==========================================

GEMMA_MODEL = "gemma3:4b" 

OLLAMA_URL = "http://127.0.0.1:11434"

OLLAMA_TIMEOUT = 180


# ==========================================
# WHISPER
# ==========================================

WHISPER_MODEL = "base"

WHISPER_LANGUAGE = "es"

WHISPER_FP16 = False


# ==========================================
# VOZ
# ==========================================

VOICE_SAMPLE_RATE = 16000

VOICE_CHANNELS = 1

VOICE_BLOCK_SIZE = 1024

VOICE_SILENCE_THRESHOLD = 0.01

VOICE_SILENCE_DURATION = 1.0

VOICE_MAX_DURATION = 20.0


# ==========================================
# RUTAS
# ==========================================

VOICE_TEMP_PATH = "data/temp/voz_actual.wav"

OUTPUT_PATH = "data/output"

REPORT_OUTPUT = "data/output/informe_voz.pdf"