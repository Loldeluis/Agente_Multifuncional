from typing import Dict, Any
import os

from agents.report_agent import generar_informe
from services.pdf_service import generar_pdf


def ejecutar_agente(
    agente: str,
    accion: str,
    datos: Dict[str, Any]
) -> Dict[str, Any]:

    # ==========================================
    # REPORT AGENT
    # ==========================================

    if agente == "report_agent":

        print("\n📄 Ejecutando Report Agent...")

        ruta_consolidado = os.path.join(
            "data",
            "output",
            "consolidado.json"
        )

        ruta_pdf = os.path.join(
            "data",
            "output",
            "informe_voz.pdf"
        )

        try:

            # ----------------------------------
            # Generar informe
            # ----------------------------------

            informe = generar_informe(
                ruta_consolidado
            )

            # ----------------------------------
            # Generar PDF
            # ----------------------------------

            generar_pdf(
                informe,
                ruta_pdf
            )

            return {
                "estado": "completado",
                "agente": "report_agent",
                "accion": accion,
                "datos": datos,
                "archivo": ruta_pdf
            }

        except Exception as e:

            return {
                "estado": "error",
                "agente": "report_agent",
                "accion": accion,
                "datos": datos,
                "error": str(e)
            }

    # ==========================================
    # GRAPH AGENT
    # ==========================================

    if agente == "graph_agent":

        print("\n🕸️ Ejecutando Graph Agent...")

        return {
            "estado": "pendiente",
            "agente": "graph_agent",
            "accion": accion,
            "datos": datos
        }

    # ==========================================
    # KNOWLEDGE AGENT
    # ==========================================

    if agente == "knowledge_agent":

        print("\n🧠 Ejecutando Knowledge Agent...")

        return {
            "estado": "pendiente",
            "agente": "knowledge_agent",
            "accion": accion,
            "datos": datos
        }

    # ==========================================
    # IMAGE AGENT
    # ==========================================

    if agente == "image_agent":

        print("\n🖼️ Ejecutando Image Agent...")

        return {
            "estado": "pendiente",
            "agente": "image_agent",
            "accion": accion,
            "datos": datos
        }

    # ==========================================
    # AUDIO AGENT
    # ==========================================

    if agente == "audio_agent":

        print("\n🎧 Ejecutando Audio Agent...")

        return {
            "estado": "pendiente",
            "agente": "audio_agent",
            "accion": accion,
            "datos": datos
        }

    # ==========================================
    # DESCONOCIDO
    # ==========================================

    return {
        "estado": "error",
        "agente": None,
        "accion": "desconocido",
        "datos": datos,
        "mensaje": "No existe un agente asociado."
    }