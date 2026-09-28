import shutil
import subprocess


class LocalLLMEngine:
    def __init__(self) -> None:
        self.enabled = self._detect_ollama()

    def _detect_ollama(self) -> bool:
        return shutil.which("ollama") is not None

    def is_available(self) -> bool:
        return self.enabled

    def answer(self, question: str) -> str | None:
        if not self.enabled:
            return None
        try:
            proc = subprocess.run(["ollama", "run", "llama3.2", question], capture_output=True, text=True, timeout=12)
            if proc.returncode == 0 and proc.stdout.strip():
                return proc.stdout.strip()
            if proc.stderr:
                return proc.stderr.strip()
        except Exception:
            return None
        return None
