# main.py
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

from geometry_utils import GeometryUtils
from shapely_helper import ShapelyHelper
from voronoi_geometry import VoronoiGeometry
from voronoi_diagram import VoronoiDiagram
from cell import Cell
from itertools import combinations

SH = ShapelyHelper()
VG = VoronoiGeometry(SH)
VD = VoronoiDiagram(shapely_helper=SH, voronoi_geo=VG, bbox=20)

class VoronoiGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Incremental Voronoi Diagram - Step by Step")

        self.pair_steps = [
            "Compute Midpoint",
            "Calculate Slope",
            "Perpendicular Slope",
            "Bisector Line"
        ]
        self.final_steps = [
            "Bisector vs Bounding Box",
            "Clip polygons",
            "Incremental Voronoi"
        ]

        self.points_for_voronoi = []
        self.num_points = 0

        self.pairs = []
        self.current_pair_idx = 0
        self.current_step_idx = 0

        self.stored_midpoints = []
        self.stored_bisectors = []

        self.final_steps_started = False
        self.current_final_step_idx = 0

        self.setup_ui()
        self.create_plot()
        self.populate_step_listbox()

    def setup_ui(self):
        left = ttk.Frame(self.root)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=20, pady=20)

        ttk.Label(left, text="Voronoi Steps", font=("Arial", 16, "bold")).pack(pady=12)

        self.step_listbox = tk.Listbox(left, height=14, width=45, font=("Arial", 12))
        self.step_listbox.pack(pady=12)

        btn_width = 20
        ttk.Button(left, text="Enter Number of Points", command=self.enter_num_points, width=btn_width).pack(pady=6)
        ttk.Button(left, text="Set Points", command=self.set_points, width=btn_width).pack(pady=6)

        btn_frame = ttk.Frame(left)
        btn_frame.pack(pady=12)
        ttk.Button(btn_frame, text="Start", command=self.start, width=btn_width).pack(pady=6)
        ttk.Button(btn_frame, text="Next Step", command=self.next_step, width=btn_width).pack(pady=6)
        ttk.Button(btn_frame, text="Previous Step", command=self.prev_step, width=btn_width).pack(pady=6)
        ttk.Button(btn_frame, text="Reset Plot", command=self.reset_all, width=btn_width).pack(pady=6)

    def populate_step_listbox(self):
        self.step_listbox.delete(0, tk.END)
        for s in self.pair_steps + self.final_steps:
            self.step_listbox.insert(tk.END, s)

    def enter_num_points(self):
        n = simpledialog.askinteger("Input", "Enter number of points (≥2):", minvalue=2)
        if n is not None:
            self.num_points = n
            messagebox.showinfo("Info", f"Number of points set to {n}. Now click 'Set Points'.")

    def set_points(self):
        if self.num_points < 2:
            messagebox.showerror("Error", "Please enter number of points first.")
            return
        self.points_for_voronoi.clear()
        for i in range(self.num_points):
            while True:
                coords = simpledialog.askstring("Point Input", f"Enter coordinates of point {i+1} as x,y:")
                if coords is None:
                    return
                try:
                    x_str, y_str = coords.split(",")
                    x, y = float(x_str.strip()), float(y_str.strip())
                    self.points_for_voronoi.append((x, y))
                    break
                except Exception:
                    messagebox.showerror("Error", "Invalid format. Please enter as x,y")
        self.pairs = list(combinations(self.points_for_voronoi, 2))
        self.create_plot()

    def create_plot(self):
        if hasattr(self, 'canvas'):
            self.canvas.get_tk_widget().pack_forget()

        self.fig, self.ax = plt.subplots(figsize=(7, 7))
        self.ax.set_title("Incremental Voronoi Diagram", fontsize=16, fontweight="bold")
        self.ax.set_xlim(-15, 15)
        self.ax.set_ylim(-15, 15)
        self.ax.set_aspect('equal')
        self.ax.grid(True, alpha=0.3)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        for idx, p in enumerate(self.points_for_voronoi):
            self.draw_point(p, f"P{idx+1}")

        for M in self.stored_midpoints:
            self.draw_point(M, s=50, color='red')
        for bis in self.stored_bisectors:
            self.draw_line_from_linestring(bis, linewidth=2, linestyle='--', color='gray')

        self.canvas.draw()

    def reset_all(self):
        self.current_pair_idx = 0
        self.current_step_idx = 0
        self.stored_midpoints.clear()
        self.stored_bisectors.clear()
        self.final_steps_started = False
        self.current_final_step_idx = 0
        self.populate_step_listbox()
        self.create_plot()

    def start(self):
        if len(self.points_for_voronoi) < 2:
            messagebox.showerror("Error", "Please set at least 2 points.")
            return
        self.reset_all()
        self.run_step()

    def highlight_step(self, step_name):
        all_steps = self.pair_steps + self.final_steps
        try:
            idx = all_steps.index(step_name)
            self.step_listbox.selection_clear(0, tk.END)
            self.step_listbox.selection_set(idx)
            self.step_listbox.see(idx)
        except:
            pass

    def next_step(self):
        if not self.pairs:
            return

        if not self.final_steps_started:
            self.current_step_idx += 1
            if self.current_step_idx >= len(self.pair_steps):
                self.current_step_idx = 0
                self.current_pair_idx += 1
                if self.current_pair_idx >= len(self.pairs):
                    self.final_steps_started = True
                    self.current_final_step_idx = 0
        else:
            self.current_final_step_idx += 1
            if self.current_final_step_idx >= len(self.final_steps):
                messagebox.showinfo("تم!", "تم عرض جميع الخطوات بنجاح!")
                self.current_final_step_idx = len(self.final_steps) - 1

        self.run_step()

    def prev_step(self):
        if self.final_steps_started:
            self.current_final_step_idx -= 1
            if self.current_final_step_idx < 0:
                self.final_steps_started = False
                self.current_pair_idx = len(self.pairs) - 1
                self.current_step_idx = len(self.pair_steps) - 1
        else:
            self.current_step_idx -= 1
            if self.current_step_idx < 0:
                self.current_pair_idx -= 1
                if self.current_pair_idx < 0:
                    self.current_pair_idx = 0
                    self.current_step_idx = 0
                else:
                    self.current_step_idx = len(self.pair_steps) - 1
        self.run_step()

    # --------- Drawing Functions ---------
    def draw_point(self, p, label=None, s=40, color='blue'):
        x, y = p
        self.ax.scatter(x, y, s=s, color=color, zorder=5)
        if label:
            self.ax.text(x + 0.3, y + 0.3, label, fontsize=12, fontweight='bold')

    def draw_line_from_linestring(self, linestring, **kwargs):
        try:
            coords = list(linestring.coords)
        except:
            coords = list(linestring)
        xs, ys = zip(*coords)
        self.ax.plot(xs, ys, **kwargs)

    def draw_polygon(self, poly, edgecolor='black', fill=False, alpha=0.2, linewidth=1.5):
        try:
            coords = list(poly.exterior.coords)[:-1]
        except:
            coords = poly
        if not coords:
            return
        xs, ys = zip(*(coords + [coords[0]]))
        self.ax.plot(xs, ys, color=edgecolor, linewidth=linewidth)
        if fill:
            self.ax.fill(xs, ys, alpha=alpha, color=edgecolor)

    # --------- Main Step Execution ---------
    def run_step(self):
        self.ax.clear()
        self.ax.set_xlim(-15, 15)
        self.ax.set_ylim(-15, 15)
        self.ax.set_aspect('equal')
        self.ax.grid(True, alpha=0.3)
        self.ax.set_title("Incremental Voronoi Diagram", fontsize=16, fontweight="bold")

        for idx, p in enumerate(self.points_for_voronoi):
            self.draw_point(p, f"P{idx+1}")

        step_name = ""
        if not self.final_steps_started:
            if self.current_pair_idx >= len(self.pairs):
                self.final_steps_started = True
                self.current_final_step_idx = 0
                self.run_step()
                return

            p1, p2 = self.pairs[self.current_pair_idx]
            step_name = self.pair_steps[self.current_step_idx]

            if step_name == "Compute Midpoint":
                M = tuple(GeometryUtils.midpoint(p1, p2))
                self.draw_point(M, f"M_{self.current_pair_idx+1}", s=70, color='red')
                if M not in self.stored_midpoints:
                    self.stored_midpoints.append(M)

            elif step_name == "Calculate Slope":
                x1, y1 = p1; x2, y2 = p2
                slope = "vertical" if abs(x2 - x1) < 1e-12 else f"{(y2 - y1)/(x2 - x1):.3f}"
                self.ax.text(-14, 14, f"Slope of P{self.points_for_voronoi.index(p1)+1}P{self.points_for_voronoi.index(p2)+1}: {slope}", 
                            fontsize=12, bbox=dict(boxstyle="round", facecolor="wheat"))

            elif step_name == "Perpendicular Slope":
                x1, y1 = p1; x2, y2 = p2
                if abs(x2 - x1) < 1e-12:
                    perp = "horizontal (slope = 0)"
                else:
                    m = (y2 - y1) / (x2 - x1)
                    perp = "vertical" if abs(m) < 1e-12 else f"{-1/m:.3f}"
                self.ax.text(-14, 14, f"Perpendicular slope: {perp}", 
                            fontsize=12, bbox=dict(boxstyle="round", facecolor="lightgreen"))

            elif step_name == "Bisector Line":
                bisector = VG.perpendicular_bisector(p1, p2, length=60)
                self.draw_line_from_linestring(bisector, linewidth=2.5, linestyle='--', color='purple')
                if bisector not in self.stored_bisectors:
                    self.stored_bisectors.append(bisector)
                M = tuple(GeometryUtils.midpoint(p1, p2))
                self.draw_point(M, f"M", s=70, color='red')

        else:
            step_name = self.final_steps[self.current_final_step_idx]

            if step_name == "Bisector vs Bounding Box":
                box = VD.initial_polygon()
                self.draw_polygon(box, edgecolor='gray', linewidth=2)

            elif step_name == "Clip polygons":
                initial = VD.initial_polygon()
                cells = [Cell(p, polygon=initial, shapely_helper=SH, voronoi_geo=VG) for p in self.points_for_voronoi]
                for idx, (p1, p2) in enumerate(self.pairs):
                    bisector = VG.perpendicular_bisector(p1, p2, length=1000)
                    (x1, y1), (x2, y2) = list(bisector.coords)
                    a = y1 - y2; b = x2 - x1; c = x1*y2 - x2*y1
                    line = (a, b, c)
                    keep_positive_for_p1 = VD.choose_halfplane_side(new_point=p1, old_point=p2, bisector=bisector)
                    for cell in cells:
                        if cell.generator == p1:
                            cell.clip_with_halfplane(line, keep_positive_for_p1)
                        elif cell.generator == p2:
                            cell.clip_with_halfplane(line, not keep_positive_for_p1)
                colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57', '#DDA0DD']
                for i, cell in enumerate(cells):
                    col = colors[i % len(colors)]
                    self.draw_polygon(cell.polygon, edgecolor=col, fill=True, alpha=0.15, linewidth=2.5)

            elif step_name == "Incremental Voronoi":
                self.stored_bisectors.clear()  

                cells = VD.incremental_voronoi(self.points_for_voronoi)
                beautiful_colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57', '#DDA0DD', '#98D8C8', '#F7DC6F']

                for i, cell in enumerate(cells):
                    col = beautiful_colors[i % len(beautiful_colors)]

                    self.draw_polygon(cell.polygon, edgecolor=col, fill=True, alpha=0.35, linewidth=4)

                    gx, gy = cell.generator
                    self.ax.scatter(gx, gy, s=400, color='black', zorder=6)
                    self.ax.scatter(gx, gy, s=250, color='white', zorder=6)
                    self.ax.scatter(gx, gy, s=140, color=col, zorder=6)

                    self.ax.text(gx, gy, f"P{i+1}", fontsize=18, fontweight='bold', color='white',
                                ha='center', va='center',
                                bbox=dict(boxstyle="circle,pad=0.5", facecolor=col, edgecolor='black', linewidth=2.5),
                                zorder=7)

        for M in self.stored_midpoints:
            self.draw_point(M, s=60, color='red')
        for bis in self.stored_bisectors:
            self.draw_line_from_linestring(bis, linewidth=2, linestyle='--', color='gray', alpha=0.7)

        self.highlight_step(step_name)
        self.ax.legend().set_visible(False)
        self.canvas.draw()


if __name__ == "__main__":
    root = tk.Tk()
    app = VoronoiGUI(root)
    root.geometry("1200x700")
    root.mainloop()