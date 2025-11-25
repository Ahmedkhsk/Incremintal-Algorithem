class GUIData:
    def __init__(self):
        self.points_for_voronoi = []
        self.num_points = 0

        self.pairs = []
        self.current_pair_idx = 0
        self.current_step_idx = 0

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

        self.stored_midpoints = []
        self.stored_bisectors = []

        self.final_steps_started = False
        self.current_final_step_idx = 0
        self.step_messages = []
