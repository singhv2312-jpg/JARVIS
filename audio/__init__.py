from __future__ import annotations

import datetime as dt
import threading
import time
import tkinter as tk
from pathlib import Path

from ai.llm_engine import LocalLLMEngine
from audio.tts_engine import TTSManager
from config import HELP_TEXT
from core.command_engine import CommandEngine
from core.knowledge_core import KnowledgeCore
from core.response_manager import ResponseManager
from core.router import CommandRouter
from core.session_manager import SessionManager
from core.state_manager import SystemState
from telemetry.logger import TelemetryLogger
from telemetry.report import MissionReportGenerator
from ui.hud import ReactorHUD
from ui.panels import MetricCard, StatusRow
from ui.terminal import TerminalWidget


class JARVISApp:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("J.A.R.V.I.S.")
        self.root.geometry("1440x980")
        self.root.configure(bg="#020c17")
        self.root.minsize(1200, 900)

        self.state = SystemState()
        self.router = CommandRouter()
        self.logger = TelemetryLogger()
        self.session_manager = SessionManager()
        self.report_generator = MissionReportGenerator()
        self.command_engine = CommandEngine(self.state, self.session_manager, self.logger, self.report_generator)
        self.knowledge_core = KnowledgeCore()
        self.llm_engine = LocalLLMEngine()
        self.tts = TTSManager()

        self.ui = self._build_ui()
        self.response_manager = ResponseManager(self.state, self.router, self.command_engine, self.knowledge_core, self.llm_engine, self.logger, self.tts, self.ui)

        self._register_boot_sequence()
        self._seed_terminal()

    def _build_ui(self):
        container = tk.Frame(self.root, bg="#020c17")
        container.pack(fill="both", expand=True, padx=18, pady=14)

        topbar = tk.Frame(container, bg="#071827", height=64, highlightbackground="#1d9ce3", highlightthickness=2)
        topbar.pack(fill="x", pady=(0, 10))

        title = tk.Label(topbar, text="J.A.R.V.I.S.", bg="#071827", fg="#dff7ff", font=("Segoe UI", 28, "bold"), anchor="w")
        title.place(x=18, y=8)
        subtitle = tk.Label(topbar, text="JUST A RATHER VERY INTELLIGENT SYSTEM", bg="#071827", fg="#61d7ff", font=("Segoe UI", 10, "bold"), anchor="w")
        subtitle.place(x=20, y=40)

        meta = tk.Label(topbar, text="OFFLINE CYBER-TERMINAL   |   HYBRID AI COMMAND CENTER   |   TACTICAL INTELLIGENCE INTERFACE", bg="#071827", fg="#8ec9ff", font=("Segoe UI", 9), anchor="center")
        meta.place(relx=0.47, rely=0.5, anchor="center")
        clock = tk.Label(topbar, text=dt.datetime.now().strftime("%a %d %b %Y   %H:%M:%S"), bg="#071827", fg="#dff7ff", font=("Segoe UI", 10, "bold"), anchor="e")
        clock.place(relx=0.95, rely=0.5, anchor="e")

        self.clock_label = clock

        body = tk.Frame(container, bg="#020c17")
        body.pack(fill="both", expand=True)

        left = tk.Frame(body, bg="#020c17", width=220)
        left.pack(side="left", fill="y", padx=(0, 12))

        nav = tk.Frame(left, bg="#081d2d", highlightbackground="#1f87d4", highlightthickness=1)
        nav.pack(fill="x")

        menu_items = ["HOME", "TERMINAL", "TELEMETRY", "ANALYTICS", "COMMANDS", "MEMORY", "SETTINGS"]
        for item in menu_items:
            btn = tk.Button(nav, text=item, bg="#081d2d", fg="#dff7ff", activebackground="#0e2d44", activeforeground="#7fe8ff", bd=0, highlightthickness=0, font=("Segoe UI", 10, "bold"), pady=8)
            btn.pack(fill="x", padx=8, pady=3)

        status_panel = tk.Frame(left, bg="#071827", highlightbackground="#1f87d4", highlightthickness=1)
        status_panel.pack(fill="x", pady=(12, 0))
        header = tk.Label(status_panel, text="SYSTEM STATUS", bg="#071827", fg="#dff7ff", font=("Segoe UI", 11, "bold"), anchor="w")
        header.pack(fill="x", padx=8, pady=(8, 0))
        self.status_rows = []
        for name, state in [("CORE", "ONLINE"), ("HUD", "ONLINE"), ("VOICE ENGINE", "ONLINE"), ("TELEMETRY", "ONLINE"), ("AI ENGINE", "ONLINE"), ("DATA LOGGER", "ONLINE")]:
            row = StatusRow(status_panel, name=name, status=state)
            row.pack(fill="x")
            self.status_rows.append(row)

        terminal_box = tk.Frame(left, bg="#071827", highlightbackground="#1f87d4", highlightthickness=1)
        terminal_box.pack(fill="both", expand=True, pady=(12, 0))
        terminal_title = tk.Label(terminal_box, text="LIVE TERMINAL", bg="#071827", fg="#5ee3ff", font=("Segoe UI", 10, "bold"), anchor="w")
        terminal_title.pack(fill="x", padx=10, pady=(8, 4))
        self.terminal = TerminalWidget(terminal_box, height=15)
        self.terminal.pack(fill="both", expand=True, padx=10, pady=(4, 10))

        quick = tk.Frame(left, bg="#071827", highlightbackground="#1f87d4", highlightthickness=1)
        quick.pack(fill="x", pady=(12, 0))
        quick_title = tk.Label(quick, text="QUICK COMMANDS", bg="#071827", fg="#dff7ff", font=("Segoe UI", 10, "bold"), anchor="w")
        quick_title.pack(fill="x", padx=10, pady=(8, 4))
        for label in ["SYSTEM DIAGNOSTIC", "SHOW TELEMETRY", "ACTIVATE REACTOR", "COMMAND HISTORY", "PROTOCOL OMEGA"]:
            cmd = tk.Button(quick, text=label, bg="#071827", fg="#9feaff", activebackground="#143a57", activeforeground="#dff7ff", bd=1, relief="solid", padx=8, pady=6, font=("Segoe UI", 9, "bold"))
            cmd.pack(side="left", padx=6, pady=8)

        center = tk.Frame(body, bg="#020c17")
        center.pack(side="left", fill="both", expand=True)

        hub = tk.Frame(center, bg="#081d2d", highlightbackground="#1f87d4", highlightthickness=1)
        hub.pack(fill="both", expand=True)
        self.hud_canvas = tk.Canvas(hub, bg="#020d19", highlightthickness=0)
        self.hud_canvas.pack(fill="both", expand=True)
        self.reactor_hud = ReactorHUD(self.hud_canvas)

        bottom = tk.Frame(center, bg="#020c17")
        bottom.pack(fill="x", pady=(10, 0))
        self.command_entry = tk.Entry(bottom, bg="#081d2d", fg="#dff7ff", insertbackground="#dff7ff", font=("Segoe UI", 12), relief="flat", highlightbackground="#1f87d4", highlightthickness=1)
        self.command_entry.pack(fill="x", side="left", expand=True, ipady=10, padx=(0, 8))
        self.command_entry.bind("<Return>", self.handle_command)
        send = tk.Button(bottom, text="EXECUTE", bg="#040d18", fg="#7fe8ff", activebackground="#0f304a", font=("Segoe UI", 10, "bold"), command=lambda: self.handle_command(None))
        send.pack(side="right")

        right = tk.Frame(body, bg="#020c17", width=360)
        right.pack(side="left", fill="y", padx=(12, 0))

        telemetry_box = tk.Frame(right, bg="#071827", highlightbackground="#1f87d4", highlightthickness=1)
        telemetry_box.pack(fill="x")
        telemetry_title = tk.Label(telemetry_box, text="TELEMETRY", bg="#071827", fg="#dff7ff", font=("Segoe UI", 11, "bold"), anchor="w")
        telemetry_title.pack(fill="x", padx=10, pady=(8, 0))

        metrics = tk.Frame(telemetry_box, bg="#071827")
        metrics.pack(fill="x", padx=10, pady=8)
        self.metric_cards = [
            MetricCard(metrics, label="CPU", value="18%", color="#39d3ff"),
            MetricCard(metrics, label="MEMORY", value="42%", color="#4ade8a"),
            MetricCard(metrics, label="DISK", value="28%", color="#f5d76e"),
            MetricCard(metrics, label="NETWORK", value="1.4 KB/s", color="#ff4d5a"),
        ]
        for card in self.metric_cards:
            card.pack(side="left", fill="x", expand=True, padx=4)

        perf_box = tk.Frame(right, bg="#071827", highlightbackground="#1f87d4", highlightthickness=1)
        perf_box.pack(fill="x", pady=(12, 0))
        perf_title = tk.Label(perf_box, text="PERFORMANCE", bg="#071827", fg="#dff7ff", font=("Segoe UI", 11, "bold"), anchor="w")
        perf_title.pack(fill="x", padx=10, pady=(8, 0))
        self.perf_canvas = tk.Canvas(perf_box, width=320, height=120, bg="#071827", highlightthickness=0)
        self.perf_canvas.pack(fill="x", padx=10, pady=(6, 10))

        ai_box = tk.Frame(right, bg="#071827", highlightbackground="#1f87d4", highlightthickness=1)
        ai_box.pack(fill="x", pady=(12, 0))
        ai_title = tk.Label(ai_box, text="AI INTELLIGENCE", bg="#071827", fg="#dff7ff", font=("Segoe UI", 11, "bold"), anchor="w")
        ai_title.pack(fill="x", padx=10, pady=(8, 0))
        self.ai_status = tk.Label(ai_box, text="Ready for your command...", bg="#071827", fg="#8ec9ff", anchor="w", justify="left")
        self.ai_status.pack(fill="x", padx=10, pady=(6, 8))

        mem_box = tk.Frame(right, bg="#071827", highlightbackground="#1f87d4", highlightthickness=1)
        mem_box.pack(fill="x", pady=(12, 0))
        mem_text = tk.Label(mem_box, text="SESSION MEMORY", bg="#071827", fg="#dff7ff", font=("Segoe UI", 11, "bold"), anchor="w")
        mem_text.pack(fill="x", padx=10, pady=(8, 0))
        self.session_memory = tk.Label(mem_box, text="Total interactions: 0\nSystem commands: 0\nAI queries: 0", bg="#071827", fg="#8ec9ff", justify="left", anchor="w", font=("Segoe UI", 9))
        self.session_memory.pack(fill="x", padx=10, pady=(6, 12))

        footer = tk.Frame(container, bg="#020c17", height=38)
        footer.pack(fill="x", pady=(12, 0))
        tk.Label(footer, text="PYQUEST 2026   |   PROJECT J.A.R.V.I.S.", bg="#020c17", fg="#60d4ff", font=("Segoe UI", 9, "bold")).pack(side="left")
        tk.Label(footer, text="INTELLIGENCE  |  AUTOMATION  |  YOU", bg="#020c17", fg="#dff7ff", font=("Segoe UI", 9, "bold")).pack(side="right")

        self.ui_handle = {
            "status_rows": self.status_rows,
            "terminal": self.terminal,
            "ai_status": self.ai_status,
            "session_memory": self.session_memory,
            "sym": None,
        }
        return self.ui_handle

    def _register_boot_sequence(self) -> None:
        self.state.mark_boot_complete()
        self.reactor_hud.set_state("IDLE", 1.0)
        self.command_entry.insert(0, "")
        self.root.after(150, self._animate_boot)

    def _animate_boot(self) -> None:
        boot_steps = [
            "INITIALIZING J.A.R.V.I.S...",
            "CORE ENGINE ........ ONLINE",
            "COMMAND ENGINE ..... ONLINE",
            "HUD ENGINE ......... ONLINE",
            "TELEMETRY .......... ONLINE",
            "DATA ENGINE ........ ONLINE",
            "VOICE ENGINE ....... ONLINE",
            "KNOWLEDGE CORE ..... ONLINE",
            "GENERATIVE CORE .... READY / STANDBY",
            "BOOT SEQUENCE COMPLETE. WELCOME BACK, SIR.",
        ]
        for step in boot_steps:
            self.terminal.append(step)
            self.root.update_idletasks()
            self.root.after(180, lambda: None)
        self.state.hud_state = "IDLE"
        self.reactor_hud.set_state("IDLE", 1.0)
        self.ai_status.config(text="Ready for your command...")

    def _seed_terminal(self) -> None:
        self.terminal.clear()
        self.terminal.append("J.A.R.V.I.S.> Boot sequence complete.")
        self.terminal.append("J.A.R.V.I.S.> All systems online.")
        self.terminal.append("J.A.R.V.I.S.> Ready for command input.")
        self.terminal.append("J.A.R.V.I.S.> What would you like to do?")

    def handle_command(self, event) -> None:
        text = self.command_entry.get().strip()
        if not text:
            return
        self.command_entry.delete(0, tk.END)
        self.terminal.append(f"> {text}")
        self._submit_command(text)

    def _submit_command(self, raw_text: str) -> None:
        self.state.set_hud("PROCESSING", 1.4)
        self.reactor_hud.set_state("PROCESSING", 1.4)
        self.ai_status.config(text="Processing command...")

        route = self.router.classify(raw_text)
        intent = route.get("intent", "UNKNOWN")
        result = self.response_manager.process(raw_text)
        source = result.get("source", "SYSTEM")
        resp = result.get("result", {}).get("response", "")
        self.terminal.append(resp)

        self.logger.log_event(
            timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
            user_input=raw_text,
            intent=intent,
            response_source=source,
            latency=result.get("latency", 0.0),
            system_state=self.state.get_snapshot(),
            status=result.get("result", {}).get("status", "SUCCESS"),
        )

        self.session_manager.add_entry({
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "user_input": raw_text,
            "intent": intent,
            "response_source": source,
            "latency": result.get("latency", 0.0),
            "status": result.get("result", {}).get("status", "SUCCESS"),
        })

        self._refresh_status()
        self._refresh_memory()
        self._draw_perf_chart()
        self.reactor_hud.set_state(self.state.hud_state if self.state.hud_state else "IDLE", self.state.reactor_intensity)

    def _refresh_status(self) -> None:
        self.state.get_snapshot()
        for row, (name, status) in zip(self.status_rows, [
            ("CORE", "ONLINE"),
            ("HUD", self.state.hud_state),
            ("VOICE ENGINE", self.state.voice_state),
            ("TELEMETRY", self.state.telemetry_state),
            ("AI ENGINE", self.state.ai_state),
            ("DATA LOGGER", "ONLINE"),
        ]):
            row.status.config(text=status)
            row.status.configure(fg="#35f4d0")

    def _refresh_memory(self) -> None:
        summary = self.logger.summary()
        self.session_memory.config(
            text=(
                f"Total interactions: {summary.get('total_interactions', 0)}\n"
                f"System commands: {summary.get('system_commands', 0)}\n"
                f"AI queries: {summary.get('ai_queries', 0)}\n"
                f"Knowledge responses: {summary.get('knowledge_responses', 0)}\n"
                f"LLM responses: {summary.get('llm_responses', 0)}"
            )
        )

    def _draw_perf_chart(self) -> None:
        self.perf_canvas.delete("all")
        events = self.logger.events
        if not events:
            return
        width = 320
        height = 120
        values = [min(100, max(10, float(e.get("latency", 0.0) or 0.0) * 100)) for e in events[-20:]]
        if not values:
            return
        max_val = max(values)
        step = width / max(1, len(values) - 1)
        prev = None
        for idx, value in enumerate(values):
            x = 10 + idx * step
            y = height - 10 - (value / max_val) * 80
            if prev is not None:
                self.perf_canvas.create_line(prev[0], prev[1], x, y, fill="#39d3ff", width=2)
            prev = (x, y)
        self.perf_canvas.create_line(10, height - 10, width - 10, height - 10, fill="#1a95df")

    def append_terminal(self, text: str) -> None:
        self.terminal.append(text)

    def set_hud_state(self, state: str) -> None:
        self.reactor_hud.set_state(state, self.state.reactor_intensity)

    def refresh_telemetry(self) -> None:
        self._refresh_memory()
        self._draw_perf_chart()

    def refresh_history(self) -> None:
        pass

    def run(self) -> None:
        self.root.after(200, self._update_clock)
        self.root.after(150, self._animate_hud_loop)
        self.root.mainloop()

    def _update_clock(self) -> None:
        self.clock_label.config(text=dt.datetime.now().strftime("%a %d %b %Y   %H:%M:%S"))
        self.root.after(1000, self._update_clock)

    def _animate_hud_loop(self) -> None:
        self.reactor_hud.draw()
        self.root.after(30, self._animate_hud_loop)
