import tkinter as tk
from model import SplineModel
from view import SplineView

class SplineController:
    def __init__(self, root, model, view):
        self.root = root
        self.model = model
        self.view = view
        self.view.set_generate_command(self.generate_surface)

    def generate_surface(self):
        try:
            n_points = self.view.get_n_points()
            n_angles = self.view.get_n_angles()
        except ValueError:
            self.view.show_error("Please enter valid integer values for resolution.")
            return

        curve = self.model.catmull_rom_spline(n_points)
        surface = self.model.revolve_curve_around_y(curve, n_angles)

        # Calculate metrics using the model
        arc_len = self.model.arc_length(curve)
        curv_vals = self.model.curvature(curve)
        normals = self.model.normals_2d(curve)
        surf_area = self.model.surface_area(curve)
        vol = self.model.volume(curve)

        # Pass data to the view for plotting
        self.view.plot_surface(curve, surface, arc_len, surf_area, vol, curv_vals, normals)

    def run(self):
        self.root.mainloop()