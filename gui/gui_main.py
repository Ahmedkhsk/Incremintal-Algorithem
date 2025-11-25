import tkinter as tk
from tkinter import ttk, simpledialog, messagebox

from gui.gui_data import GUIData
from gui.gui_draw import GUIDraw
from gui.gui_steps import GUISteps

from core.shapely_helper import ShapelyHelper
from core.voronoi_geometry import VoronoiGeometry
from core.voronoi_diagram import VoronoiDiagram

from itertools import combinations


class VoronoiGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Incremental Voronoi Diagram")

        self.status_frame = ttk.Frame(self.root)
        self.status_frame.pack(side="top", fill="x")
        self.status_text = tk.Text(self.status_frame, height=4, wrap='word', state='disabled', font=("Arial", 10))
        self.status_text.pack(side="left", fill="x", expand=True, padx=6, pady=6)

        self.data = GUIData()
        self.draw = GUIDraw(self)
        self.steps = GUISteps(self)

        self.SH = ShapelyHelper()
        self.VG = VoronoiGeometry(self.SH)
        self.VD = VoronoiDiagram(self.SH, self.VG, bbox=20)

        self.setup_ui()
        self.draw.create_plot()
        self.populate_step_listbox()

    def setup_ui(self):
        left = ttk.Frame(self.root)
        left.pack(side="left", fill="y", padx=20, pady=20)

        ttk.Label(left, text="Voronoi Steps", font=("Arial", 16, "bold")).pack(pady=12)

        self.step_listbox = tk.Listbox(left, height=14, width=45, font=("Arial", 12))
        self.step_listbox.pack(pady=12)

        w = 22
        ttk.Button(left, text="Enter Number of Points", command=self.enter_num_points, width=w).pack(pady=6)
        ttk.Button(left, text="Set Points", command=self.set_points, width=w).pack(pady=6)
        ttk.Button(left, text="Start", command=self.start, width=w).pack(pady=6)
        ttk.Button(left, text="Next Step", command=self.next_step, width=w).pack(pady=6)
        ttk.Button(left, text="Prev Step", command=self.prev_step, width=w).pack(pady=6)
        ttk.Button(left, text="Reset", command=self.reset, width=w).pack(pady=6)

    def populate_step_listbox(self):
        self.step_listbox.delete(0, "end")
        for s in self.data.pair_steps + self.data.final_steps:
            self.step_listbox.insert("end", s)

    def log(self, message: str):
        self.data.step_messages.append(message)
        self.status_text.config(state='normal')
        self.status_text.insert('end', message + '\n')
        self.status_text.see('end')
        self.status_text.config(state='disabled')

    def clear_log(self):
        self.data.step_messages.clear()
        self.status_text.config(state='normal')
        self.status_text.delete('1.0', 'end')
        self.status_text.config(state='disabled')

    def enter_num_points(self):
        n = simpledialog.askinteger("Input", "Enter number of points:", minvalue=2)
        if n:
            self.data.num_points = n

    def set_points(self):
        if self.data.num_points <= 0:
            n = simpledialog.askinteger("Input", "Enter number of points:", minvalue=2)
            if not n:
                return
            self.data.num_points = n

        win = tk.Toplevel(self.root)
        win.title("Enter Points")
        win.transient(self.root)

        entry_widgets = []
        for i in range(self.data.num_points):
            row = ttk.Frame(win)
            row.pack(fill='x', padx=8, pady=4)
            ttk.Label(row, text=f"Point {i+1} (x,y):", width=16).pack(side='left')
            e = ttk.Entry(row, width=20)
            e.pack(side='left', padx=6)
            entry_widgets.append(e)

        def submit_points():
            pts = []
            for idx, e in enumerate(entry_widgets):
                txt = e.get().strip()
                if not txt:
                    messagebox.showerror("Error", f"Point {idx+1} is empty. Enter as x,y")
                    return
                try:
                    x, y = txt.split(",")
                    pts.append((float(x), float(y)))
                except Exception:
                    messagebox.showerror("Error", f"Point {idx+1} invalid. Enter as x,y")
                    return

            self.data.points_for_voronoi = pts
            self.data.pairs = list(combinations(self.data.points_for_voronoi, 2))
            self.draw.create_plot()
            win.destroy()

        btn_frame = ttk.Frame(win)
        btn_frame.pack(fill='x', pady=8)
        ttk.Button(btn_frame, text="Submit Points", command=submit_points).pack(side='left', padx=6)
        ttk.Button(btn_frame, text="Cancel", command=win.destroy).pack(side='left')

    def start(self):
        self.reset()
        self.steps.run()

    def reset(self):
        old_points = list(self.data.points_for_voronoi)
        self.data = GUIData()
        self.data.points_for_voronoi = old_points
        self.data.pairs = list(combinations(old_points, 2))

        self.draw.create_plot()
        self.populate_step_listbox()
        self.clear_log()

    def next_step(self):
        if not self.data.final_steps_started:
            self.data.current_step_idx += 1

            if self.data.current_step_idx >= len(self.data.pair_steps):
                self.data.current_step_idx = 0
                self.data.current_pair_idx += 1

                if self.data.current_pair_idx >= len(self.data.pairs):
                    self.data.final_steps_started = True
        else:
            self.data.current_final_step_idx += 1

            if self.data.current_final_step_idx >= len(self.data.final_steps):
                self.data.current_final_step_idx = len(self.data.final_steps) - 1
                messagebox.showinfo("Done", "All steps have been displayed.")

        self.steps.run()

    def prev_step(self):
        if self.data.final_steps_started:
            self.data.current_final_step_idx -= 1

            if self.data.current_final_step_idx < 0:
                self.data.final_steps_started = False
                self.data.current_pair_idx = len(self.data.pairs) - 1
                self.data.current_step_idx = len(self.data.pair_steps) - 1
        else:
            self.data.current_step_idx -= 1

            if self.data.current_step_idx < 0:
                self.data.current_pair_idx -= 1

                if self.data.current_pair_idx < 0:
                    self.data.current_pair_idx = 0
                    self.data.current_step_idx = 0
                else:
                    self.data.current_step_idx = len(self.data.pair_steps) - 1

        self.steps.run()
