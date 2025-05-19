import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.animation import FuncAnimation
import os


class DynamicHeatmap:
    def __init__(self):
        self.arrays = []
        self.current_idx = 0
        self.frame_count = 0
        self.frames_between = 20  # Interpolation frames
        self.load_arrays()

    def load_arrays(self):
        for i in range(20):
            path = f"foot-array/array_{i+1}.npy"
            if os.path.exists(path):
                self.arrays.append(np.load(path))

    def setup_animation(self):
        self.fig, self.ax = plt.subplots(figsize=(10, 8))
        colors = ["#0000ff", "#00ffff", "#00ff00", "#ffff00", "#ff0000"]
        custom_cmap = LinearSegmentedColormap.from_list("custom_cmap", colors)
        self.im = self.ax.imshow(
            self.arrays[0],
            cmap=custom_cmap,
            # cmap= 'YlOrRd',
            interpolation="nearest",
            aspect="equal",
            vmin=0,
            vmax=800,
        )
        plt.colorbar(self.im)

    def interpolate(self, arr1, arr2, fraction):
        """Linear interpolation between two arrays"""
        return arr1 + (arr2 - arr1) * fraction

    def update(self, frame):
        # Calculate which arrays we're transitioning between
        total_arrays = len(self.arrays)
        array_index = (frame // self.frames_between) % total_arrays
        next_index = (array_index + 1) % total_arrays

        # Calculate interpolation fraction
        fraction = (frame % self.frames_between) / self.frames_between

        # Get current and next arrays
        current = self.arrays[array_index]
        next_array = self.arrays[next_index]

        # Interpolate between arrays
        interpolated = self.interpolate(current, next_array, fraction)

        # Update display
        self.im.set_array(interpolated)
        self.ax.set_title(f"Transitioning: Array {array_index + 1} → {next_index + 1}")
        return [self.im]

    def animate(self):
        self.setup_animation()
        anim = FuncAnimation(
            self.fig,
            self.update,
            frames=len(self.arrays) * self.frames_between,
            interval=50,  # Shorter interval for smoother transition
            blit=True,
            repeat=True,
        )
        plt.show()


if __name__ == "__main__":
    viz = DynamicHeatmap()
    viz.animate()
