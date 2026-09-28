from __future__ import annotations

from typing import Any, Dict, List


class MissionReportGenerator:
    def __init__(self) -> None:
        pass

    def generate_report(self, events: List[Dict[str, Any]]) -> str:
        if not events:
            return "J.A.R.V.I.S.\nSESSION INTELLIGENCE REPORT\n\nNO INTERACTIONS RECORDED."
        total = len(events)
        system_commands = sum(1 for e in events if e.get("response_source") == "SYSTEM")
        ai_queries = sum(1 for e in events if e.get("intent") == "KNOWLEDGE_QUERY")
        knowledge_core = sum(1 for e in events if e.get("response_source") == "KNOWLEDGE_CORE")
        avg_latency = sum(float(e.get("latency", 0.0) or 0.0) for e in events) / total
        success_rate = (sum(1 for e in events if e.get("status") == "SUCCESS") / total) * 100 if total else 0.0
        report = (
            "J.A.R.V.I.S.\nSESSION INTELLIGENCE REPORT\n\n"
            f"TOTAL INTERACTIONS: {total}\n"
            f"SYSTEM COMMANDS: {system_commands}\n"
            f"AI QUERIES: {ai_queries}\n"
            f"KNOWLEDGE CORE QUERIES: {knowledge_core}\n"
            f"AVERAGE LATENCY: {avg_latency:.2f}s\n"
            f"SUCCESS RATE: {success_rate:.0f}%\n"
            "SYSTEM STATUS: NOMINAL\n\nCORE STATUS: NOMINAL"
        )
        return report
