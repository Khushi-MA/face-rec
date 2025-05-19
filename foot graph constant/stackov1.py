import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path

# Create a heat map with 20x20 random data
ax = plt.subplot(111)
plt.pcolor(np.random.random((20, 20)))

# Define a foot shape - scaled for 20x20
foot_verts = [
    (6.4, 15),  # Start point
    (5.8, 11.2),
    (8.2, 8.8),
    (8, 7),  # Cubic Bezier controls and end point
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

# Rest of the code remains same
foot_codes = [
    Path.MOVETO,
    Path.CURVE4,
    Path.CURVE4,
    Path.CURVE4,
    Path.CURVE4,
    Path.CURVE4,
    Path.CURVE4,
    Path.CURVE4,
    Path.CURVE4,
    Path.CURVE4,
    Path.CURVE4,
    Path.CURVE4,
    Path.CURVE4,
    Path.CURVE4,
    Path.CURVE4,
    Path.CURVE4,
    Path.CURVE4,
    Path.CURVE4,
    Path.CURVE4,
]

xlim = ax.get_xlim()
ylim = ax.get_ylim()

ax_verts = [
    (xlim[0], ylim[0]),
    (xlim[0], ylim[1]),
    (xlim[1], ylim[1]),
    (xlim[1], ylim[0]),
    (xlim[0], ylim[0]),
]

ax_codes = [Path.MOVETO, Path.LINETO, Path.LINETO, Path.LINETO, Path.LINETO]

path = Path(ax_verts + foot_verts, ax_codes + foot_codes)
patch = patches.PathPatch(path, facecolor="white", edgecolor="none")
ax.add_patch(patch)

plt.show()
