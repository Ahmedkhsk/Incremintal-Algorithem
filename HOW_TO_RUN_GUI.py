#!/usr/bin/env python3
"""
HOW TO RUN THE VORONOI DIAGRAM GUI APPLICATION

This guide shows you step-by-step how to run the interactive GUI
"""

print("""
╔════════════════════════════════════════════════════════════════════╗
║        HOW TO RUN THE INCREMENTAL VORONOI DIAGRAM GUI             ║
╚════════════════════════════════════════════════════════════════════╝

STEP 1: MAKE SURE DEPENDENCIES ARE INSTALLED
============================================

Run this command (tkinter comes bundled with Python):

    python -m pip install matplotlib numpy shapely

✅ NOTE: tkinter is already included with Python - do NOT try to pip install it!

STEP 2: RUN THE GUI APPLICATION
================================

From the command line, run:

    python voronoi_gui.py

Or from Windows PowerShell:

    cd c:\\_home\\college\\comp-411-incremental-algorithm\\Incremintal-Algorithem
    python voronoi_gui.py

STEP 3: USING THE GUI
======================

When the window opens:

1. Click "Enter Number of Points"
   → Choose a number (2-5 recommended for first test)
   → Example: 3

2. Click "Set Points"
   → You'll be prompted to enter coordinates for each point
   → Format: x,y (separated by comma)
   → Example inputs:
        Point 1: 0,0
        Point 2: 2,0
        Point 3: 1,2

3. Click "Start"
   → Initializes the visualization
   → Shows initial bounding box

4. Click "Next Step" to step through the algorithm
   → Shows each step of the Voronoi construction:
        - Compute Midpoint
        - Calculate Slope
        - Perpendicular Slope
        - Bisector Line
        - Bisector vs Bounding Box
        - Clip polygons
        - Incremental Voronoi

5. Click "Previous Step" to go back

6. Click "Reset Plot" to start over with new points

TIPS FOR TESTING
================

✅ Small point sets work best: 2-3 points to start
✅ Try different shapes:
   - Horizontal line: (0,0), (2,0)
   - Triangle: (0,0), (2,0), (1,2)
   - Square: (0,0), (2,0), (2,2), (0,2)

✅ The GUI shows:
   - Points as red dots
   - Cells as blue polygons
   - Bisectors as lines
   - Step-by-step construction

TROUBLESHOOTING
===============

If tkinter doesn't work:
  → tkinter comes with Python - if missing, reinstall Python with tkinter option
  → Check: python -c "import tkinter; print('OK')"

If matplotlib doesn't work:
  → Run: python -m pip install matplotlib --upgrade

If numpy/shapely missing:
  → Run: python -m pip install numpy shapely

QUICK START (ONE COMMAND)
==========================

Windows PowerShell:
  cd c:\\_home\\college\\comp-411-incremental-algorithm\\Incremintal-Algorithem
  python voronoi_gui.py

Linux/Mac:
  cd /path/to/Incremintal-Algorithem
  python voronoi_gui.py

✅ THAT'S IT! The GUI should open!

""")

# Try to run the GUI
if __name__ == "__main__":
    import sys
    print("\nNote: This file just shows instructions.")
    print("To actually run the GUI, execute:")
    print("  python voronoi_gui.py")
