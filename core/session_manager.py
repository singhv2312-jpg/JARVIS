import csv
import datetime as dt
from pathlib import Path

from config import SESSION_LOG_DIR


class SessionManager:
    def __init__(self) -> None:
        self.session_start = dt.datetime.now()
        self.history = []

    def add_entry(self, entry: dict) -> None:
        self.history.append(entry)

    def command_history(self, limit: int = 10) -> str:
        entries = self.history[-limit:]
        if not entries:
            return "TIME | COMMAND | INTENT | SOURCE | STATUS | LATENCY\nNO COMMANDS IN SESSION HISTORY"
        lines = ["TIME | COMMAND | INTENT | SOURCE | STATUS | LATENCY"]
        for e in entries:
            lines.append(
                f"{e.get('timestamp', '--')} | {str(e.get('user_input', ''))[:30]} | {e.get('intent', '--')} | {e.get('response_source', '--')} | {e.get('status', '--')} | {e.get('latency', 0.0):.2f}s"
            )
        return "\n".join(lines)

    def export_csv(self, filename: str = "session_log.csv") -> str:
        path = SESSION_LOG_DIR / filename
        fieldnames = ["timestamp", "user_input", "intent", "response_source", "latency", "system_state", "status"]
        with path.open("w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=fieldnames)
            writer.writeheader()
            for entry in self.history:
                writer.writerow({name: entry.get(name, "") for name in fieldnames})
        return str(path)

    def mission_report_text(self) -> str:
        if not self.history:
            return "J.A.R.V.I.S.\nSESSION INTELLIGENCE REPORT\n\nNO INTERACTIONS RECORDED."
        total = len(self.history)
        success = sum(1 for e in self.history if e.get("status") == "SUCCESS")
        avg_latency = sum(float(e.get("latency", 0.0) or 0.0) for e in self.history) / total
        duration = (dt.datetime.now() - self.session_start).total_seconds()
        return (
            "J.A.R.V.I.S.\nSESSION INTELLIGENCE REPORT\n\n"
            f"TOTAL INTERACTIONS: {total}\n"
            f"SYSTEM COMMANDS: {sum(1 for e in self.history if e.get('response_source') == 'SYSTEM')}\n"
            f"AI QUERIES: {sum(1 for e in self.history if e.get('intent') == 'KNOWLEDGE_QUERY')}\n"
            f"KNOWLEDGE CORE QUERIES: {sum(1 for e in self.history if e.get('response_source') == 'KNOWLEDGE_CORE')}\n"
            f"AVERAGE LATENCY: {avg_latency:.2f}s\n"
            f"SESSION DURATION: {duration:.2f}s\n"
            f"SYSTEM STATUS: NOMINAL\n\nCORE STATUS: NOMINAL\nSUCCESS RATE: {((success / total) * 100 if total else 0):.0f}%"
        )
