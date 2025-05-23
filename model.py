import numpy as np
import pyvista as pv

class SplineModel:
    def __init__(self, control_points):
        self.control_points = np.array(control_points)
        self._curve = None
        self._surface = None
        self._arc_length = None
        self._curvature = None
        self._normals_2d = None
        self._surface_area = None
        self._volume = None

    def catmull_rom_spline(self, n_points=100):
        def tj(ti, pi, pj, alpha=0.5):
            return ((np.linalg.norm(pj - pi))**alpha) + ti

        P = self.control_points
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
        self._curve = np.array(curve)
        return self._curve

    def revolve_curve_around_y(self, curve, n_angles=100):
        angles = np.linspace(0, 2 * np.pi, n_angles)
        verts = []
        for theta in angles:
            rot = np.array([[np.cos(theta), 0, np.sin(theta)],
                            [0, 1, 0],
                            [-np.sin(theta), 0, np.cos(theta)]])
            ring = [rot @ np.array([x, y, 0]) for x, y in curve]
            verts.append(ring)
        self._surface = np.array(verts)
        return self._surface

    def arc_length(self, curve):
        self._arc_length = np.sum(np.linalg.norm(np.diff(curve, axis=0), axis=1))
        return self._arc_length

    def curvature(self, curve):
        curve_3d = np.hstack([curve, np.zeros((curve.shape[0], 1))])
        d1 = np.gradient(curve_3d, axis=0)
        d2 = np.gradient(d1, axis=0)
        num = np.linalg.norm(np.cross(d1, d2), axis=1)
        denom = np.linalg.norm(d1, axis=1)**3
        self._curvature = np.nan_to_num(num / denom)
        return self._curvature

    def normals_2d(self, curve):
        d1 = np.gradient(curve, axis=0)
        norm = np.stack([-d1[:, 1], d1[:, 0]], axis=1)
        self._normals_2d = norm / np.linalg.norm(norm, axis=1, keepdims=True)
        return self._normals_2d

    def generate_mesh(self, points_3d):
        n_angles, n_points, _ = points_3d.shape
        x = points_3d[:,:,0].T
        y = points_3d[:,:,1].T
        z = points_3d[:,:,2].T
        return pv.StructuredGrid(x, y, z)

    def surface_area(self, curve):
        ds = np.linalg.norm(np.diff(curve, axis=0), axis=1)
        area = 0
        for i in range(1, len(curve)):
            y = curve[i, 1]
            ds_val = ds[i-1]
            area += 2 * np.pi * y * ds_val
        self._surface_area = area
        return self._surface_area

    def volume(self, curve):
        ds = np.linalg.norm(np.diff(curve, axis=0), axis=1)
        vol = 0
        for i in range(1, len(curve)):
            r = curve[i, 1]
            ds_val = ds[i-1]
            vol += np.pi * r**2 * ds_val
        self._volume = vol
        return self._volume

    # Getter metódusok a számított értékek lekéréséhez
    def get_curve(self):
        return self._curve

    def get_surface(self):
        return self._surface

    def get_arc_length(self):
        return self._arc_length

    def get_curvature(self):
        return self._curvature

    def get_normals_2d(self):
        return self._normals_2d

    def get_surface_area(self):
        return self._surface_area

    def get_volume(self):
        return self._volume