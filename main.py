import tkinter as tk
import numpy as np
from model import SplineModel
from view import SplineView
from controller import SplineController

if __name__ == "__main__":
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

    root = tk.Tk()
    model = SplineModel(control_points)
    view = SplineView(root)
    controller = SplineController(root, model, view)
    controller.run()