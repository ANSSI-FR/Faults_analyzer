import parser.manage_manip as mm
import numpy as np
import sys
import matplotlib as mpl
import matplotlib.pyplot as plt
import time

def get_args():
    if len(sys.argv) < 2:
        print("Error : Missing arguments")
        print("Usage : {} [manip_dir]".format(sys.argv[0]))
        exit(1)
    manip_dir = sys.argv[1]
    if manip_dir[-1] != "/":
        manip_dir = manip_dir + "/"
    return manip_dir

def build_matrix(manip):
    matrix = np.zeros(manip.get_size())
    for ope in manip:
        if ope.get("plan.done") == True:
            x_grid = int(ope.get("x_grid"))
            y_grid = int(ope.get("y_grid"))
            try:
                matrix[y_grid, x_grid] += 1
            except IndexError:
                pass
    return matrix

manip_dir = get_args()
manip = mm.manage_manip(manip_dir)
matrix = build_matrix(manip)
max_round = manip.get_repeat()

f = plt.figure()
ax = f.gca()
#colorbar
cmap = plt.cm.jet
if matrix.min() != matrix.max():
    bounds = np.linspace(int(matrix.min()), int(matrix.max()), int(matrix.max()-matrix.min())+1)
    norm = mpl.colors.BoundaryNorm(np.arange(matrix.min()-0.5, matrix.max()+1+0.5, 1), cmap.N)
else:
    bounds = np.linspace(matrix.min()-1, matrix.min()+1, 3)
    norm = mpl.colors.BoundaryNorm(np.arange(matrix.min()-0.5-1, matrix.max()+1+0.5+1, 1), cmap.N)
cax = ax.matshow(matrix, cmap=cmap, norm=norm)
cb = f.colorbar(cax, ticks=bounds)
f.show()

while 1:
    manip.refresh_results()
    matrix = build_matrix(manip)
    cmap = plt.cm.jet
    if matrix.min() != matrix.max():
        bounds = np.linspace(int(matrix.min()), int(matrix.max()), int(matrix.max()-matrix.min())+1)
        norm = mpl.colors.BoundaryNorm(np.arange(matrix.min()-0.5, matrix.max()+1+0.5, 1), cmap.N)
    else:
        bounds = np.linspace(matrix.min()-1, matrix.min()+1, 3)
        norm = mpl.colors.BoundaryNorm(np.arange(matrix.min()-0.5-1, matrix.max()+1+0.5+1, 1), cmap.N)
    cax = ax.matshow(matrix, cmap=cmap, norm=norm)
    cb.remove()
    cb = f.colorbar(cax, ticks=bounds)
    rnd = manip.get_current_repeat()
    f.suptitle("Current round is {}/{}".format(rnd, max_round))
    f.canvas.draw()
    time.sleep(1)

f.close()
