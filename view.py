import tkinter as tk
from tkinter import ttk
import pyvista as pv
import numpy as np

class SplineView:
    def __init__(self, master):
        self.master = master
        master.title("Spline Surface Generator")

        self.frame = ttk.Frame(master, padding=10)
        self.frame.grid(row=0, column=0)

        ttk.Label(self.frame, text="Spline Resolution (points):").grid(row=0, column=0)
        self.n_point_var = tk.StringVar(value="100")
        ttk.Entry(self.frame, textvariable=self.n_point_var).grid(row=0, column=1)

        ttk.Label(self.frame, text="Revolution Resolution (angles):").grid(row=1, column=0)
        self.n_angle_var = tk.StringVar(value="120")
        ttk.Entry(self.frame, textvariable=self.n_angle_var).grid(row=1, column=1)

        self.generate_button = ttk.Button(self.frame, text="Generate")
        self.generate_button.grid(row=2, column=0, columnspan=2, pady=10)

    def set_generate_command(self, command):
        self.generate_button.config(command=command)

    def get_n_points(self):
        return int(self.n_point_var.get())

    def get_n_angles(self):
        return int(self.n_angle_var.get())

    def show_error(self, message):
        tk.messagebox.showerror("Error", message)

    def plot_surface(self, curve, surface, arc_length_val, surface_area_val, volume_val, curvature_vals, normals_vals):
        mesh = self._generate_mesh(surface)
        plotter = pv.Plotter()
        plotter.add_mesh(mesh, show_edges=True, color='lightblue')

        # Add curvature as a scalar field (mapped to color)
        curv_vals_display = np.pad(curvature_vals, (0, len(surface[0]) - len(curvature_vals)), 'edge')
        mesh.point_data["Curvature"] = np.tile(curv_vals_display, len(surface))

        plotter.add_mesh(mesh, scalars="Curvature", cmap="viridis", show_scalar_bar=True)

        # Show normals
        for i in range(0, len(curve), 10):
            p = np.array([*curve[i], 0])
            n = np.array([*normals_vals[i], 0])
            plotter.add_arrows(p[None], n[None], mag=0.2, color='red')

        # Show surface area and volume
        plotter.add_text(f"Arc Length: {arc_length_val:.2f}", font_size=10)
        plotter.add_text(f"Surface Area: {surface_area_val:.2f}", font_size=10, position=(1, 500))  # Top left custom
        plotter.add_text(f"Volume: {volume_val:.2f}", font_size=10, position=(0, 520))  # Bottom left custom

        plotter.add_axes()
        plotter.show()

    def _generate_mesh(self, points_3d):
        n_angles, n_points, _ = points_3d.shape
        x = points_3d[:,:,0].T
        y = points_3d[:,:,1].T
        z = points_3d[:,:,2].T
        return pv.StructuredGrid(x, y, z)