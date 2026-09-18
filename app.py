"""Tkinter interface for the DFA/NFA Time Format Validator Simulator."""

import tkinter as tk
from tkinter import ttk

from automata import validate_time


class SimulatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Time Format Validator – DFA & NFA Simulator")
        self.geometry("900x650")
        self.minsize(760, 560)
        self.configure(bg="#eef2ff")
        self._build_style()
        self._build_ui()

    def _build_style(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Title.TLabel", font=("Segoe UI", 20, "bold"), background="#eef2ff", foreground="#1e1b4b")
        style.configure("Info.TLabel", font=("Segoe UI", 10), background="#eef2ff", foreground="#475569")
        style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=8)
        style.configure("Treeview", font=("Consolas", 10), rowheight=27)
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

    def _build_ui(self):
        ttk.Label(self, text="Time Format Validator", style="Title.TLabel").pack(pady=(22, 3))
        ttk.Label(self, text="A Python simulator showing how DFA and NFA process an input one character at a time.", style="Info.TLabel").pack()

        controls = ttk.Frame(self, padding=18)
        controls.pack(fill="x", padx=28, pady=18)
        ttk.Label(controls, text="Automaton:").grid(row=0, column=0, sticky="w", padx=(0, 8))
        self.machine = ttk.Combobox(controls, state="readonly", width=28,
                                    values=["DFA – 24-hour (HH:MM)", "NFA – 12-hour (hh:mm AM/PM)"])
        self.machine.current(0)
        self.machine.grid(row=0, column=1, sticky="ew", padx=(0, 18))
        self.machine.bind("<<ComboboxSelected>>", self._mode_changed)

        ttk.Label(controls, text="Time input:").grid(row=0, column=2, sticky="w", padx=(0, 8))
        self.time_input = ttk.Entry(controls, width=22, font=("Consolas", 13))
        self.time_input.grid(row=0, column=3, sticky="ew", padx=(0, 12))
        self.time_input.insert(0, "09:30")
        self.time_input.bind("<Return>", lambda _event: self.run_simulation())
        ttk.Button(controls, text="Simulate", command=self.run_simulation).grid(row=0, column=4)
        controls.columnconfigure(1, weight=1)
        controls.columnconfigure(3, weight=1)

        self.rule = ttk.Label(controls, text="Rule: exactly HH:MM; hours 00–23 and minutes 00–59.")
        self.rule.grid(row=1, column=0, columnspan=5, sticky="w", pady=(12, 0))

        self.result = tk.Label(self, text="Enter a time, then click Simulate.", font=("Segoe UI", 13, "bold"),
                               bg="#eef2ff", fg="#334155")
        self.result.pack(pady=(0, 10))

        table_frame = ttk.Frame(self, padding=(28, 0, 28, 15))
        table_frame.pack(fill="both", expand=True)
        self.table = ttk.Treeview(table_frame, columns=("step", "current", "symbol", "next"), show="headings")
        for col, title, width in [("step", "Step", 60), ("current", "Current State(s)", 210),
                                  ("symbol", "Input Symbol", 130), ("next", "Next State(s)", 210)]:
            self.table.heading(col, text=title)
            self.table.column(col, width=width, anchor="center")
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)
        self.table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        notes = ttk.LabelFrame(self, text="State guide", padding=10)
        notes.pack(fill="x", padx=28, pady=(0, 22))
        self.guide = ttk.Label(notes, text="q0 start → q1/q2 hour check → q3 colon → q4/q6 minute check → q5 accept")
        self.guide.pack(anchor="w")

    def _mode_changed(self, _event=None):
        if self.machine.get().startswith("DFA"):
            self.rule.config(text="Rule: exactly HH:MM; hours 00–23 and minutes 00–59.")
            self.guide.config(text="q0 start → q1/q2 hour check → q3 colon → q4/q6 minute check → q5 accept")
            sample = "09:30"
        else:
            self.rule.config(text="Rule: exactly hh:mm AM/PM; hours 01–12 and minutes 00–59 (AM/PM is case-insensitive).")
            self.guide.config(text="n0 start → branching hour paths → n3 colon → n4/n5 minutes → n7/n8 AM or PM → n9 accept")
            sample = "09:30 AM"
        self.time_input.delete(0, tk.END)
        self.time_input.insert(0, sample)
        self._clear_table()
        self.result.config(text="Enter a time, then click Simulate.", fg="#334155")

    def _clear_table(self):
        for row in self.table.get_children():
            self.table.delete(row)

    def run_simulation(self):
        text = self.time_input.get()
        simulation = validate_time(text, self.machine.get())
        self._clear_table()
        for index, (current, symbol, next_state) in enumerate(simulation.steps):
            self.table.insert("", "end", values=(index, current, symbol, next_state))
        verdict = "ACCEPTED" if simulation.accepted else "REJECTED"
        color = "#15803d" if simulation.accepted else "#b91c1c"
        self.result.config(text=f"{verdict} — {simulation.explanation}", fg=color)


if __name__ == "__main__":
    SimulatorApp().mainloop()
