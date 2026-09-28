from __future__ import annotations

import tkinter as tk


class MetricCard(tk.Frame):
    def __init__(self, master=None, label="CPU", value="18%", color="#39d3ff"):
        super().__init__(master, bg="#071827", highlightbackground="#1a6db4", highlightthickness=1)
        self.label = tk.Label(self, text=label.upper(), bg="#071827", fg="#8cc9ff", font=("Segoe UI", 9, "bold"))
        self.value = tk.Label(self, text=value, bg="#071827", fg=color, font=("Segoe UI", 15, "bold"))
        self.label.pack(pady=(12, 2))
        self.value.pack(pady=(0, 12))


class StatusRow(tk.Frame):
    def __init__(self, master=None, name="CORE", status="ONLINE"):
        super().__init__(master, bg="#071827")
        self.name = tk.Label(self, text=name, bg="#071827", fg="#e2f8ff", anchor="w", font=("Segoe UI", 10))
        self.dot = tk.Label(self, text="●", bg="#071827", fg="#39ff99", font=("Segoe UI", 12))
        self.status = tk.Label(self, text=status, bg="#071827", fg="#35f4d0", font=("Segoe UI", 9, "bold"))
        self.name.pack(side="left", padx=(12, 0), pady=8)
        self.dot.pack(side="left", padx=(10, 0), pady=8)
        self.status.pack(side="right", padx=(0, 12), pady=8)
