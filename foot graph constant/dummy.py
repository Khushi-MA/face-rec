import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path
from matplotlib.animation import FuncAnimation


class DynamicHeatmap:
    def __init__(self):
        self.fig, self.ax = plt.subplots()
        self.setup_foot_shape()

    def setup_foot_shape(self):
        # Define foot shape vertices and codes
        self.foot_verts = [
            (6.4, 15),
            (5.8, 11.2),
            (8.2, 8.8),
            (8, 7),
            (8.2, 5),
            (7.8, 2.6),
            (8.8, 1.2),
            (10, 0),
            (12.6, 0.4),
            (13.6, 1),
            (14.6, 3.4),
            (13.4, 5.2),
            (13, 7.6),
            (12.8, 10.2),
            (15.2, 11.4),
            (14.4, 16.6),
            (13.4, 21.6),
            (7, 18.8),
            (6.4, 15),
        ]

        self.foot_codes = [Path.MOVETO] + [Path.CURVE4] * 18

    def update(self, frame):
        self.ax.clear()
        # Generate new random data
        data = np.random.random((20, 20))
        # Plot heatmap
        self.heatmap = plt.pcolor(data)

        # Add foot shape mask
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()

        ax_verts = [
            (xlim[0], ylim[0]),
            (xlim[0], ylim[1]),
            (xlim[1], ylim[1]),
            (xlim[1], ylim[0]),
            (xlim[0], ylim[0]),
        ]
        ax_codes = [Path.MOVETO] + [Path.LINETO] * 4

        path = Path(ax_verts + self.foot_verts, ax_codes + self.foot_codes)
        patch = patches.PathPatch(path, facecolor="white", edgecolor="none")
        self.ax.add_patch(patch)

        return (self.heatmap,)

    def animate(self):
        self.anim = FuncAnimation(
            self.fig, self.update, interval=1000, blit=True, repeat=True  # 1 second
        )
        plt.show()


if __name__ == "__main__":
    viz = DynamicHeatmap()
    viz.animate()
