import json
import time
from pathlib import Path

try:
    import pandas as pd
except Exception:  # pragma: no cover
    pd = None

from config import SESSION_LOG_DIR


class TelemetryLogger:
    def __init__(self) -> None:
        self.events = []
        self.path = SESSION_LOG_DIR / "telemetry_log.json"

    def log_event(self, **kwargs) -> dict:
        event = {
            "timestamp": kwargs.get("timestamp") or time.strftime("%Y-%m-%d %H:%M:%S"),
            "user_input": kwargs.get("user_input", ""),
            "intent": kwargs.get("intent", "UNKNOWN"),
            "response_source": kwargs.get("response_source", "SYSTEM"),
            "latency": float(kwargs.get("latency", 0.0) or 0.0),
            "system_state": kwargs.get("system_state", {}),
            "status": kwargs.get("status", "SUCCESS"),
        }
        self.events.append(event)
        try:
            with self.path.open("w", encoding="utf-8") as fh:
                json.dump(self.events, fh, indent=2)
        except Exception:
            pass
        return event

    def summary(self) -> dict:
        total = len(self.events)
        system_commands = sum(1 for e in self.events if e.get("response_source") == "SYSTEM")
        ai_queries = sum(1 for e in self.events if e.get("intent") == "KNOWLEDGE_QUERY")
        knowledge_responses = sum(1 for e in self.events if e.get("response_source") == "KNOWLEDGE_CORE")
        llm_responses = sum(1 for e in self.events if e.get("response_source") == "LLM")
        success = sum(1 for e in self.events if e.get("status") == "SUCCESS")
        lat = [float(e.get("latency", 0.0) or 0.0) for e in self.events]
        avg_latency = sum(lat) / len(lat) if lat else 0.0
        fastest = min(lat) if lat else 0.0
        slowest = max(lat) if lat else 0.0
        success_rate = (success / total) * 100 if total else 0.0
        return {
            "total_interactions": total,
            "system_commands": system_commands,
            "ai_queries": ai_queries,
            "knowledge_responses": knowledge_responses,
            "llm_responses": llm_responses,
            "success_rate": round(success_rate, 2),
            "avg_latency": avg_latency,
            "fastest_response": fastest,
            "slowest_response": slowest,
            "session_duration": sum(lat),
        }

    def dataframe(self):
        if pd is not None:
            return pd.DataFrame(self.events)
        return self.events
