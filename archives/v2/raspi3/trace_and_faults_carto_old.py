import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import time
import argparse
import os, sys, inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
import parser.manage_manip as mm

FIGSIZE = (20,20) # Size of the figure (here ~ fullscreen)
TRACE = True      # Trace the cartography (ie. plot update in real time)

def get_args():
    if len(sys.argv) < 2:
        print("Error : Missing arguments")
        print("Usage : {} [manip_dir]".format(sys.argv[0]))
        exit(1)
    manip_dir = sys.argv[1]
    if manip_dir[-1] != "/":
        manip_dir = manip_dir + "/"
    return manip_dir

def build_trace_matrix(manip):
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

def build_fault_matrix(manip, no_reboot):
    matrix = np.zeros(manip.get_size())
    for ope in manip:
        if ope.get("plan.done") == True:
            log = ope.get("log")
            if log.find("i=50 j=50 cnt=2500") == -1:
                if log.find("reboot") != -1 and no_reboot:
                    pass
                else:
                    x_grid = int(ope.get("x_grid"))
                    y_grid = int(ope.get("y_grid"))
                    try:
                        matrix[y_grid, x_grid] += 1
                    except IndexError:
                        pass
    return matrix

def build_matrices(manip):
    matrices = []
    manip.refresh_results()
    matrices.append(build_trace_matrix(manip))
    matrices.append(build_fault_matrix(manip, 0))
    matrices.append(build_fault_matrix(manip, 1))
    return matrices

def get_axes(fig, nb_plots):
    axes = []
    nb_cols = np.ceil(np.sqrt(nb_plots))
    nb_rows = np.ceil(nb_plots/nb_cols)
    for i in range(nb_plots):
        axe = fig.add_subplot(nb_rows, nb_cols, i+1)
        axes.append(axe)
    return axes

def get_bounds_and_norm(matrix, cmap):
    if matrix.min() != matrix.max():
        bounds = np.linspace(int(matrix.min()), int(matrix.max()), int(matrix.max()-matrix.min())+1)
        norm = mpl.colors.BoundaryNorm(np.arange(matrix.min()-0.5, matrix.max()+1+0.5, 1), cmap.N)
        return bounds, norm
    else:
        bounds = np.linspace(matrix.min()-1, matrix.min()+1, 3)
        norm = mpl.colors.BoundaryNorm(np.arange(matrix.min()-0.5-1, matrix.max()+1+0.5+1, 1), cmap.N)
        return bounds, norm

def plot_in_axes(axes, matrices, cbs=None):
    cmap = plt.cm.jet
    if not cbs is None:
        for cb in cbs:
            cb.remove()
    cbs = []
    for i, axe in enumerate(axes):
        matrix = matrices[i]
        bounds, norm = get_bounds_and_norm(matrix, cmap)
        z = axe.matshow(matrix, cmap=cmap, norm=norm)
        cb = plt.colorbar(z, ax=axe, ticks=bounds)
        cbs.append(cb)
    return cbs

def set_title_to_axes(axes, titles):
    if len(axes) != len(titles):
        print("Number of axes and number of titles not matching")
        print("({} axes for {} titles)".format(len(axes), len(titles)))
        return 0
    for i, axe in enumerate(axes):
        axe.set_title(titles[i])

# Get the direction of the cartography via arguments
manip_dir = get_args()

# Create the matrices we want to print and give their title
manip = mm.manage_manip(manip_dir)
matrices = build_matrices(manip)
titles = ["Trace", "Faults (with reboot)", "Faults (without reboot)"]

# Create the figure and give it the title of the manipulation directory
fig = plt.figure(figsize=FIGSIZE)
fig.suptitle(manip_dir)

# Create axes, give their title and print the corresponding matrices
axes = get_axes(fig, len(matrices))
set_title_to_axes(axes, titles)
cbs = plot_in_axes(axes, matrices)

# Update (or not) the plot over time
if not TRACE:
    plt.show()
else:
    fig.show()
    while 1:
        matrices = build_matrices(manip)
        cbs = plot_in_axes(axes, matrices, cbs)
        fig.canvas.draw()
        time.sleep(0.2)
