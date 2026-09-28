from pathlib import Path

APP_TITLE = "J.A.R.V.I.S."
APP_SUBTITLE = "JUST A RATHER VERY INTELLIGENT SYSTEM"
APP_TEAM = "PyVanguard"

ROOT_DIR = Path(__file__).resolve().parent
DATA_DIR = ROOT_DIR / "data"
SESSION_LOG_DIR = DATA_DIR / "session_logs"
ASSET_DIR = ROOT_DIR / "assets"

DATA_DIR.mkdir(parents=True, exist_ok=True)
SESSION_LOG_DIR.mkdir(parents=True, exist_ok=True)
ASSET_DIR.mkdir(parents=True, exist_ok=True)

HELP_TEXT = """AVAILABLE COMMAND CATEGORIES
SYSTEM | TELEMETRY | HUD | DATA | UTILITY

EXAMPLES:
JARVIS, initiate system diagnostic.
JARVIS, show telemetry.
JARVIS, activate reactor.
JARVIS, enter defense mode.
JARVIS, show command history.
JARVIS, run performance scan.
JARVIS, initiate protocol omega.
JARVIS, generate mission report.
What is artificial intelligence?
"""
