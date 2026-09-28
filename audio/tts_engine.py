import threading
import subprocess
import shutil


class TTSManager:
    def __init__(self) -> None:
        self.available = False
        self.command = None
        self._detect()

    def _detect(self) -> None:
        for cmd in ["say", "espeak", "espeak-ng", "spd-say", "flite"]:
            if shutil.which(cmd):
                self.available = True
                self.command = cmd
                return
        try:
            import pyttsx3
            self.available = True
            self.command = "pyttsx3"
        except Exception:
            self.available = False
            self.command = None

    def speak_async(self, text: str) -> None:
        if not self.available or not text:
            return
        threading.Thread(target=self._speak_worker, args=(text,), daemon=True).start()

    def _speak_worker(self, text: str) -> None:
        try:
            if self.command == "pyttsx3":
                import pyttsx3
                engine = pyttsx3.init()
                engine.say(text)
                engine.runAndWait()
                return
            if self.command == "say":
                subprocess.run(["say", text], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
                return
            if self.command in {"espeak", "espeak-ng", "spd-say"}:
                subprocess.run([self.command, text], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
                return
            if self.command == "flite":
                subprocess.run(["flite", "-t", text], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
        except Exception:
            pass
