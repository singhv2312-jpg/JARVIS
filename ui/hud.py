from __future__ import annotations

import math
import random
import time

from tkinter import Canvas


class ReactorHUD:
    def __init__(self, canvas: Canvas) -> None:
        self.canvas = canvas
        self.state = "IDLE"
        self.intensity = 1.0
        self.start_time = time.time()
        self.particles = []
        for _ in range(40):
            self.particles.append({
                "x": random.random(),
                "y": random.random(),
                "r": random.uniform(1.2, 3.0),
                "dx": random.uniform(-0.01, 0.01),
                "dy": random.uniform(-0.01, 0.01),
            })

    def set_state(self, state: str, intensity: float = 1.0) -> None:
        self.state = state
        self.intensity = intensity

    def draw(self) -> None:
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        cx = width / 2
        cy = height / 2
        r = min(width, height) * 0.32
        self.canvas.delete("all")

        # grid lines
        self.canvas.create_line(cx - r * 1.5, cy, cx + r * 1.5, cy, fill="#1d3b58", width=1)
        self.canvas.create_line(cx, cy - r * 1.5, cx, cy + r * 1.5, fill="#1d3b58", width=1)
        for i in range(12):
            ang = math.radians(i * 30)
            x1 = cx + (r * 1.4) * math.cos(ang)
            y1 = cy + (r * 1.4) * math.sin(ang)
            x2 = cx + (r * 1.8) * math.cos(ang)
            y2 = cy + (r * 1.8) * math.sin(ang)
            self.canvas.create_line(x1, y1, x2, y2, fill="#143453", width=1)

        # rings
        for idx, radius in enumerate([r * 0.92, r * 1.06, r * 1.18, r * 1.28]):
            color = "#4fe6ff" if idx % 2 == 0 else "#ff455c"
            self.canvas.create_oval(cx - radius, cy - radius, cx + radius, cy + radius, outline=color, width=2 if idx < 2 else 1)

        # scan arc
        spin = (time.time() - self.start_time) * {"IDLE": 0.5, "PROCESSING": 0.9, "DIAGNOSTIC": 1.4, "TELEMETRY": 1.1, "TACTICAL": 1.8, "WARNING": 1.4, "COMPLETE": 1.2}.get(self.state, 0.7) * 80
        self.canvas.create_arc(cx - r * 1.2, cy - r * 1.2, cx + r * 1.2, cy + r * 1.2, start=spin, extent=130, outline="#4fe6ff", width=3, style="arc")
        self.canvas.create_arc(cx - r * 0.9, cy - r * 0.9, cx + r * 0.9, cy + r * 0.9, start=spin + 50, extent=110, outline="#ff455c", width=2, style="arc")

        # reactor core
        pulse = 1 + 0.3 * math.sin((time.time() - self.start_time) * 4.5 * self.intensity)
        rr = r * pulse * 0.5
        self.canvas.create_oval(cx - rr, cy - rr, cx + rr, cy + rr, outline="#3fe4ff", width=3)
        tri = [(cx, cy - rr * 0.9), (cx - rr * 0.75, cy + rr * 0.8), (cx + rr * 0.75, cy + rr * 0.8)]
        self.canvas.create_polygon(tri, outline="#7ffaff", fill="#0a2a42", width=2)
        self.canvas.create_oval(cx - rr * 0.28, cy - rr * 0.28, cx + rr * 0.28, cy + rr * 0.28, fill="#c6fbff", outline="#c6fbff")

        # particles
        for part in self.particles:
            part["x"] += part["dx"] * self.intensity * 18
            part["y"] += part["dy"] * self.intensity * 18
            if part["x"] < 0 or part["x"] > 1:
                part["x"] = random.random()
            if part["y"] < 0 or part["y"] > 1:
                part["y"] = random.random()
            px = cx + (part["x"] - 0.5) * r * 2.2
            py = cy + (part["y"] - 0.5) * r * 2.2
            self.canvas.create_oval(px - part["r"], py - part["r"], px + part["r"], py + part["r"], fill="#7adeff", outline="")
