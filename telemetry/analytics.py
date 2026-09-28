from __future__ import annotations

from typing import Any, Dict


class TelemetryAnalytics:
    def __init__(self, logger) -> None:
        self.logger = logger

    def summary(self) -> Dict[str, Any]:
        return self.logger.summary()
