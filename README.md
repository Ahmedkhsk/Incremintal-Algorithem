# Incremental Voronoi Diagram Generator

This project implements an **Incremental Algorithm** to generate Voronoi Diagrams using Python. The system is built upon the `Shapely` library for geometric operations and `Matplotlib` for visualization.

The project is divided into four distinct modules: Theoretical Documentation, Geometry Kernel, Core Algorithm, and Visualization.

## 📋 Project Overview

The goal is to build a robust tool that constructs Voronoi cells step-by-step. 
1.  **Geometry Kernel:** Handles vector math, perpendicular bisectors, and polygon splitting.
2.  **Incremental Algorithm:** Inserts sites one by one, dynamically updating the mesh by clipping existing cells.
3.  **Visualization:** Renders the resulting cells and animates the construction process.

## 🛠️ Installation & Dependencies

Ensure you have Python installed. Install the required libraries using pip:

```bash
pip install numpy shapely matplotlib