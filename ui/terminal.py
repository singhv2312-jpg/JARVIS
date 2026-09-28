from __future__ import annotations

import tkinter as tk


class TerminalWidget(tk.Text):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(
            bg="#071826",
            fg="#dff7ff",
            insertbackground="#7fe8ff",
            relief="flat",
            highlightthickness=0,
            wrap=tk.WORD,
            font=("Consolas", 10),
            padx=12,
            pady=10,
        )

    def append(self, message: str) -> None:
        self.configure(state=tk.NORMAL)
        self.insert(tk.END, message + "\n")
        self.see(tk.END)
        self.configure(state=tk.DISABLED)

    def clear(self) -> None:
        self.configure(state=tk.NORMAL)
        self.delete("1.0", tk.END)
        self.configure(state=tk.DISABLED)
