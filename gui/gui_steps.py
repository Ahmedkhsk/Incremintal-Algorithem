from core.geometry_utils import GeometryUtils
from core.cell import Cell
from matplotlib import cm

class GUISteps:
    def __init__(self, gui):
        self.gui = gui

    def highlight(self, step_name):
        steps = self.gui.data.pair_steps + self.gui.data.final_steps
        if step_name in steps:
            idx = steps.index(step_name)
            self.gui.step_listbox.selection_clear(0, "end")
            self.gui.step_listbox.selection_set(idx)
            self.gui.step_listbox.see(idx)

    def run(self):
        self.gui.ax.clear()
        self.gui.ax.set_xlim(-15, 15)
        self.gui.ax.set_ylim(-15, 15)
        self.gui.ax.set_aspect('equal')
        self.gui.ax.grid(True, alpha=0.3)

        for idx, p in enumerate(self.gui.data.points_for_voronoi):
            self.gui.draw.draw_point(p, f"P{idx+1}")

        step_name = ""

        if not self.gui.data.final_steps_started:
            if self.gui.data.current_pair_idx >= len(self.gui.data.pairs):
                self.gui.data.final_steps_started = True
                self.gui.data.current_final_step_idx = 0
                self.run()
                return

            p1, p2 = self.gui.data.pairs[self.gui.data.current_pair_idx]
            step_name = self.gui.data.pair_steps[self.gui.data.current_step_idx]

            if step_name == "Compute Midpoint":
                M = tuple(GeometryUtils.midpoint(p1, p2))
                self.gui.draw.draw_point(M, s=70, color='red')
                self.gui.log(f"Compute Midpoint between {p1} and {p2} -> M={M}")
                if M not in self.gui.data.stored_midpoints:
                    self.gui.data.stored_midpoints.append(M)

            elif step_name == "Bisector Line":
                bisector = self.gui.VG.perpendicular_bisector(p1, p2, length=60)
                self.gui.draw.draw_line(bisector, linewidth=2.5, linestyle='--', color='purple')
                if bisector not in self.gui.data.stored_bisectors:
                    self.gui.data.stored_bisectors.append(bisector)
                self.gui.log(f"Bisector line for {p1} & {p2} drawn (approx extent shown)")

            elif step_name == "Calculate Slope":
                v = GeometryUtils.vec(p1, p2)
                dx = v[0]
                dy = v[1]
                if abs(dx) < 1e-12:
                    slope = float('inf')
                    self.gui.log(f"Calculate Slope: vertical line between {p1} and {p2} (slope=inf)")
                else:
                    slope = dy/dx
                    self.gui.log(f"Calculate Slope between {p1} and {p2}: dy={dy:.4f}, dx={dx:.4f}, slope={slope:.4f}")

            elif step_name == "Perpendicular Slope":
                v = GeometryUtils.vec(p1, p2)
                perp = GeometryUtils.perpendicular(v)
                self.gui.log(f"Perpendicular slope vector for {p1} & {p2}: {perp}")

        else:
            step_name = self.gui.data.final_steps[self.gui.data.current_final_step_idx]

            if step_name == "Incremental Voronoi":
                cells = self.gui.VD.incremental_voronoi(self.gui.data.points_for_voronoi)
                colors = cm.get_cmap('tab20').colors

                for i, cell in enumerate(cells):
                    color = colors[i % len(colors)]
                    self.gui.draw.draw_polygon(cell.polygon, fill=True, color=color, alpha=0.35)

                for p in self.gui.data.points_for_voronoi:
                    self.gui.draw.draw_circle(p, radius=1.2, edgecolor='black', fill=False, alpha=0.8, linewidth=1.8)

                self.gui.data.stored_bisectors.clear()
                self.gui.log("Final: colored each Voronoi region and drew circles around sites. Removed helper bisectors.")

        for m in self.gui.data.stored_midpoints:
            self.gui.draw.draw_point(m, s=55, color='red')

        if not self.gui.data.final_steps_started:
            for bis in self.gui.data.stored_bisectors:
                self.gui.draw.draw_line(bis, linestyle='--', color='gray', alpha=0.7)

        self.highlight(step_name)
        self.gui.canvas.draw()
