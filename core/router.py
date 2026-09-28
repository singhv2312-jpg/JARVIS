import re


def normalize_command(raw: str) -> str:
    text = (raw or "").strip().lower()
    text = text.replace("\n", " ")
    text = re.sub(r"[^a-z0-9\s\-]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


class CommandRouter:
    def __init__(self) -> None:
        self.system_patterns = [
            "system diagnostic", "run diagnostics", "system check", "check the system",
            "diagnostic", "system status", "system information", "system scan", "check systems"
        ]
        self.telemetry_patterns = [
            "show telemetry", "show analytics", "performance", "session statistics",
            "system activity", "telemetry", "analytics", "performance scan"
        ]
        self.hud_patterns = [
            "activate reactor", "activate hud", "tactical mode", "defense mode",
            "scan mode", "enter defense mode", "protocol omega", "maximum power",
            "emergency protocol", "activate defense", "activate tactical"
        ]
        self.data_patterns = [
            "command history", "session log", "export data", "mission report",
            "generate mission report", "show command history", "show session log"
        ]
        self.utility_patterns = ["help", "clear", "reset", "about", "time", "what time"]
        self.knowledge_patterns = [
            "what is", "who are you", "how do you work", "what is your architecture",
            "are you offline", "do you use an llm", "how were you built",
            "what language are you written in", "what is the hud", "what is telemetry",
            "what is artificial intelligence", "what is python", "what is ai"
        ]

    def classify(self, raw: str) -> dict:
        text = normalize_command(raw)
        if not text:
            return {"intent": "UNKNOWN", "category": "UTILITY", "source": "SYSTEM"}

        if text.startswith("jarvis"):
            text = text.replace("jarvis", "", 1).strip()

        if any(p in text for p in self.system_patterns):
            return {"intent": "SYSTEM_DIAGNOSTIC", "category": "SYSTEM", "source": "SYSTEM"}
        if any(p in text for p in self.telemetry_patterns):
            return {"intent": "SHOW_TELEMETRY", "category": "TELEMETRY", "source": "SYSTEM"}
        if any(p in text for p in self.hud_patterns):
            if "protocol omega" in text or "maximum power" in text or "emergency protocol" in text:
                return {"intent": "PROTOCOL_OMEGA", "category": "SPECIAL", "source": "SYSTEM"}
            if "defense" in text or "tactical" in text:
                return {"intent": "DEFENSE_MODE", "category": "HUD", "source": "SYSTEM"}
            return {"intent": "ACTIVATE_REACTOR", "category": "HUD", "source": "SYSTEM"}
        if any(p in text for p in self.data_patterns):
            if "mission report" in text or "generate" in text:
                return {"intent": "GENERATE_MISSION_REPORT", "category": "DATA", "source": "SYSTEM"}
            if "history" in text or "session log" in text:
                return {"intent": "SHOW_COMMAND_HISTORY", "category": "DATA", "source": "SYSTEM"}
            return {"intent": "DATA_QUERY", "category": "DATA", "source": "SYSTEM"}
        if any(p in text for p in self.utility_patterns):
            if "time" in text:
                return {"intent": "TIME", "category": "UTILITY", "source": "SYSTEM"}
            if "help" in text:
                return {"intent": "HELP", "category": "UTILITY", "source": "SYSTEM"}
            if "clear" in text:
                return {"intent": "CLEAR", "category": "UTILITY", "source": "SYSTEM"}
            if "reset" in text:
                return {"intent": "RESET", "category": "UTILITY", "source": "SYSTEM"}
            if "about" in text:
                return {"intent": "ABOUT", "category": "UTILITY", "source": "SYSTEM"}
            return {"intent": "UTILITY", "category": "UTILITY", "source": "SYSTEM"}
        if any(p in text for p in self.knowledge_patterns) or text.startswith("what ") or text.startswith("how ") or text.startswith("who "):
            return {"intent": "KNOWLEDGE_QUERY", "category": "AI", "source": "KNOWLEDGE_CORE"}
        return {"intent": "UNKNOWN", "category": "UTILITY", "source": "SYSTEM"}
