import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Circle

class GUIDraw:
    def __init__(self, gui):
        self.gui = gui

    def create_plot(self):
        if hasattr(self.gui, 'canvas'):
            self.gui.canvas.get_tk_widget().pack_forget()

        self.gui.fig, self.gui.ax = plt.subplots(figsize=(7, 7))
        self.gui.ax.set_title("Incremental Voronoi Diagram", fontsize=16, fontweight="bold")
        self.gui.ax.set_xlim(-15, 15)
        self.gui.ax.set_ylim(-15, 15)
        self.gui.ax.set_aspect('equal')
        self.gui.ax.grid(True, alpha=0.3)

        self.gui.canvas = FigureCanvasTkAgg(self.gui.fig, master=self.gui.root)
        self.gui.canvas.get_tk_widget().pack(side="right", fill="both", expand=True)

    def draw_point(self, p, label=None, s=40, color='blue'):
        x, y = p
        self.gui.ax.scatter(x, y, s=s, color=color, zorder=5)
        if label:
            self.gui.ax.text(x + 0.3, y + 0.3, label, fontsize=12, fontweight='bold')

    def draw_circle(self, p, radius=1.2, edgecolor='black', fill=False, alpha=0.4, linewidth=1.5):
        x, y = p
        circ = Circle((x, y), radius=radius, edgecolor=edgecolor, facecolor='none' if not fill else edgecolor, alpha=alpha, linewidth=linewidth)
        self.gui.ax.add_patch(circ)

    def draw_line(self, linestring, **kwargs):
        coords = list(linestring.coords)
        xs, ys = zip(*coords)
        self.gui.ax.plot(xs, ys, **kwargs)

    def draw_polygon(self, poly, edgecolor='black', color=None, fill=False, alpha=0.2, linewidth=1.5):
        try:
            coords = list(poly.exterior.coords)[:-1]
        except:
            coords = poly
        if not coords:
            return
        
        xs, ys = zip(*(coords + [coords[0]]))
        self.gui.ax.plot(xs, ys, color=edgecolor, linewidth=linewidth)
        if fill:
            fill_color = color if color is not None else edgecolor
            self.gui.ax.fill(xs, ys, alpha=alpha, color=fill_color)
