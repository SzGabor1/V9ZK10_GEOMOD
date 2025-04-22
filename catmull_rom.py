import numpy as np
import pyvista as pv
import tkinter as tk
from tkinter import ttk

# ---------------- Spline Functions ---------------- #
def catmull_rom_spline(P, n_points=100):
    def tj(ti, pi, pj, alpha=0.5):
        return ((np.linalg.norm(pj - pi))**alpha) + ti

    P = np.array(P)
    if len(P) < 4:
        raise ValueError("Need at least 4 points for Catmull-Rom")

    curve = []
    for i in range(len(P) - 3):
        p0, p1, p2, p3 = P[i:i+4]
        t0 = 0
        t1 = tj(t0, p0, p1)
        t2 = tj(t1, p1, p2)
        t3 = tj(t2, p2, p3)

        t = np.linspace(t1, t2, n_points)
        for tj_val in t:
            A1 = (t1 - tj_val)/(t1 - t0)*p0 + (tj_val - t0)/(t1 - t0)*p1
            A2 = (t2 - tj_val)/(t2 - t1)*p1 + (tj_val - t1)/(t2 - t1)*p2
            A3 = (t3 - tj_val)/(t3 - t2)*p2 + (tj_val - t2)/(t3 - t2)*p3

            B1 = (t2 - tj_val)/(t2 - t0)*A1 + (tj_val - t0)/(t2 - t0)*A2
            B2 = (t3 - tj_val)/(t3 - t1)*A2 + (tj_val - t1)/(t3 - t1)*A3

            C = (t2 - tj_val)/(t2 - t1)*B1 + (tj_val - t1)/(t2 - t1)*B2
            curve.append(C)
    return np.array(curve)

# ---------------- Surface of Revolution ---------------- #
def revolve_curve_around_y(curve, n_angles=100):
    angles = np.linspace(0, 2 * np.pi, n_angles)
    verts = []
    for theta in angles:
        rot = np.array([[np.cos(theta), 0, np.sin(theta)],
                        [0, 1, 0],
                        [-np.sin(theta), 0, np.cos(theta)]])
        ring = [rot @ np.array([x, y, 0]) for x, y in curve]
        verts.append(ring)
    return np.array(verts)

# ---------------- Math Analysis ---------------- #
def arc_length(curve):
    return np.sum(np.linalg.norm(np.diff(curve, axis=0), axis=1))

def curvature(curve):
    curve_3d = np.hstack([curve, np.zeros((curve.shape[0], 1))])
    d1 = np.gradient(curve_3d, axis=0)
    d2 = np.gradient(d1, axis=0)
    num = np.linalg.norm(np.cross(d1, d2), axis=1)
    denom = np.linalg.norm(d1, axis=1)**3
    return np.nan_to_num(num / denom)

def normals_2d(curve):
    d1 = np.gradient(curve, axis=0)
    norm = np.stack([-d1[:, 1], d1[:, 0]], axis=1)
    return norm / np.linalg.norm(norm, axis=1, keepdims=True)

# ---------------- Mesh Construction ---------------- #
def generate_mesh(points_3d):
    n_angles, n_points, _ = points_3d.shape
    x = points_3d[:,:,0].T
    y = points_3d[:,:,1].T
    z = points_3d[:,:,2].T
    return pv.StructuredGrid(x, y, z)
# ---------------- Surface Area Calculation ---------------- #
def surface_area(curve):
    # Use numerical integration to approximate the surface area
    ds = np.linalg.norm(np.diff(curve, axis=0), axis=1)
    area = 0
    for i in range(1, len(curve)):
        y = curve[i, 1]  # y-coordinate (height of the curve)
        ds_val = ds[i-1]  # segment length
        area += 2 * np.pi * y * ds_val
    return area

# ---------------- Volume Calculation ---------------- #
def volume(curve):
    # Use numerical integration to approximate the volume
    ds = np.linalg.norm(np.diff(curve, axis=0), axis=1)
    vol = 0
    for i in range(1, len(curve)):
        r = curve[i, 1]  # radius (y-coordinate)
        ds_val = ds[i-1]  # segment length
        vol += np.pi * r**2 * ds_val
    return vol

# ---------------- Visualization ---------------- #
def plot_surface(curve, surface):
    mesh = generate_mesh(surface)
    plotter = pv.Plotter()
    plotter.add_mesh(mesh, show_edges=True, color='lightblue')

    # Add curvature as a scalar field (mapped to color)
    curv_vals = curvature(curve)
    curv_vals = np.pad(curv_vals, (0, len(surface[0]) - len(curv_vals)), 'edge')
    mesh.point_data["Curvature"] = np.tile(curv_vals, len(surface))

    plotter.add_mesh(mesh, scalars="Curvature", cmap="viridis", show_scalar_bar=True)

    # Show normals
    norms = normals_2d(curve)
    for i in range(0, len(curve), 10):
        p = np.array([*curve[i], 0])
        n = np.array([*norms[i], 0])
        plotter.add_arrows(p[None], n[None], mag=0.2, color='red')

    # Show surface area and volume
    plotter.add_text(f"Arc Length: {arc_length(curve):.2f}", font_size=10)
    plotter.add_text(f"Surface Area: {surface_area(curve):.2f}", font_size=10, position=(1, 500))  # Top left custom
    plotter.add_text(f"Volume: {volume(curve):.2f}", font_size=10, position=(0, 520))  # Bottom left custom



    plotter.add_axes()
    plotter.show()


# ---------------- UI ---------------- #
def run_app():
    def update():
        try:
            n_points = int(n_point_var.get())
            n_angles = int(n_angle_var.get())
        except ValueError:
            return

        curve = catmull_rom_spline(control_points, n_points)
        surface = revolve_curve_around_y(curve, n_angles)
        plot_surface(curve, surface)

    root = tk.Tk()
    root.title("Spline Surface Generator")

    frame = ttk.Frame(root, padding=10)
    frame.grid(row=0, column=0)

    ttk.Label(frame, text="Spline Resolution (points):").grid(row=0, column=0)
    n_point_var = tk.StringVar(value="100")
    ttk.Entry(frame, textvariable=n_point_var).grid(row=0, column=1)

    ttk.Label(frame, text="Revolution Resolution (angles):").grid(row=1, column=0)
    n_angle_var = tk.StringVar(value="120")
    ttk.Entry(frame, textvariable=n_angle_var).grid(row=1, column=1)

    ttk.Button(frame, text="Generate", command=update).grid(row=2, column=0, columnspan=2, pady=10)

    root.mainloop()

# ---------------- Main ---------------- #
if __name__ == "__main__":
    # control_points = np.array([
    #     [0, 0],
    #     [1, 2],
    #     [2, 3],
    #     [3, 1],
    #     [4, 0],
    #     [5, -1]
    # ])
    
    #Sinusoidal Curve 
#     control_points = np.array([
#     [0, 0],
#     [1, 1],
#     [2, 0],
#     [3, -1],
#     [4, 0],
#     [5, 1]
# ])
    
    #Curved Upwards
#     control_points = np.array([
#     [0, 0],
#     [1, 2],
#     [2, 4],
#     [3, 2],
#     [4, 0],
#     [5, -1]
# ])
    
    #Sharp Angles (Zig-Zag)
    
#     control_points = np.array([
#     [0, 0],
#     [1, 3],
#     [2, 1],
#     [3, 3],
#     [4, 0],
#     [5, -2]
# ])
    
    control_points = np.array([
        [0, 0],
        [1, 2],
        [2, 3],
        [3, 5],
        [4, 4],
        [5, 2],
        [6, 1],
        [7, -1],
        [8, -2],
        [9, -1],
        [10, 0],
        [11, 1],
        [12, 3],
        [13, 4],
        [14, 3],
        [15, 2],
        [16, 4],
        [17, 6],
        [18, 7],
        [19, 6]
    ])




    run_app()
