from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass
class SystemState:
    hud_state: str = "IDLE"
    system_status: str = "NOMINAL"
    ai_state: str = "STANDBY"
    voice_state: str = "ONLINE"
    telemetry_state: str = "ONLINE"
    command_engine: str = "ONLINE"
    knowledge_state: str = "ONLINE"
    protocol_mode: str = "STANDARD"
    reactor_intensity: float = 1.0
    boot_complete: bool = False
    last_response: str = ""
    last_intent: str = "UNKNOWN"
    subsystems: Dict[str, str] = field(
        default_factory=lambda: {
            "CORE": "ONLINE",
            "COMMAND ENGINE": "ONLINE",
            "HUD ENGINE": "ONLINE",
            "TELEMETRY ENGINE": "ONLINE",
            "DATA ENGINE": "ONLINE",
            "VOICE ENGINE": "ONLINE",
            "KNOWLEDGE CORE": "ONLINE",
            "GENERATIVE CORE": "READY / STANDBY",
        }
    )

    def set_hud(self, state: str, intensity: Optional[float] = None) -> None:
        self.hud_state = state
        if intensity is not None:
            self.reactor_intensity = max(0.5, min(2.8, intensity))

    def get_snapshot(self) -> Dict[str, str]:
        return {
            "hud_state": self.hud_state,
            "system_status": self.system_status,
            "ai_state": self.ai_state,
            "voice_state": self.voice_state,
            "telemetry_state": self.telemetry_state,
            "knowledge_state": self.knowledge_state,
            "command_engine": self.command_engine,
            "protocol_mode": self.protocol_mode,
        }

    def mark_boot_complete(self) -> None:
        self.boot_complete = True
        self.hud_state = "IDLE"
        self.system_status = "NOMINAL"
        self.ai_state = "STANDBY"
