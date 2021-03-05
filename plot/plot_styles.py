from plotter import PlotterType

tmp_style = {
    "x_ticklabels_fontsize": 28,
    "y_ticklabels_fontsize": 28,
    "x_label_fontsize": 28,
    "y_label_fontsize": 28,
    "legend_fontsize": 28,
    "colorbar_fontsize": 28,
    "colorbar_label_fontsize": 28,
}

def even_str(v):
    if v%2 == 0:
        return str(v)
    else:
        return ""

styles = {
    "bcm2711b0_layout":{
        "type": PlotterType.MATRIXSCATTER,
        "image": "chips/bcm2711b0/bcm2711b0_layout.jpg",
        "scale_to_image": True,
        "x_ticklabels": [i for i in range(7+1)],
        "x_ticklabels_position": [i*114 for i in range(7+1)],
        "y_ticklabels": [i for i in range(6+1)],
        "y_ticklabels_position": [i*117 for i in range(6+1)],
        "x_label": "X position (mm)",
        "y_label": "Y position (mm)"
    },
    "bcm2711b0_layout_bw":{
        "type": PlotterType.MATRIXSCATTER,
        "image": "chips/bcm2711b0/bcm2711b0_layout_bw.jpg",
        "scale_to_image": True,
        "x_ticklabels": [i for i in range(7+1)],
        "x_ticklabels_position": [i*114 for i in range(7+1)],
        "y_ticklabels": [i for i in range(6+1)],
        "y_ticklabels_position": [i*117 for i in range(6+1)],
        "x_label": "X position (mm)",
        "y_label": "Y position (mm)"
    },
    "intel_core_i3":{
        "type": PlotterType.MATRIXSCATTER,
        "image": "chips/i3-6100T/intel_core_i3_large.jpg",
        "scale_to_image": True,
        "x_ticklabels": [even_str(i) for i in range(29)],
        "x_ticklabels_position": [i*49.21 for i in range(29)],
        "y_ticklabels": [even_str(i) for i in range(29)],
        "y_ticklabels_position": [i*46.43 for i in range(29)],
        "x_label": "Position (mm)",
        "y_label": "Position (mm)"
    },
    "matrix":{
        "type": PlotterType.MATRIX
    },
    "matrixscatter":{
        "type": PlotterType.MATRIXSCATTER
    },
    "bcm2837": {
        "type": PlotterType.MATRIXSCATTER,
        "image": "chips/bcm2837/bcm2837_square_mirror.jpg",
        "scale_to_image": True,
        "x_ticklabels": reversed([str(i) for i in range(15)]),
        "x_ticklabels_position": [i*26.643 for i in range(15)],
        "y_ticklabels": [str(i) for i in range(15)],
        "y_ticklabels_position": [i*26.643 for i in range(15)],
        "x_label": "Position (mm)",
        "y_label": "Position (mm)",
        "revert_x_axis": True
    },
    "large_dist": {
        "type": PlotterType.BAR,
        "rotate_x_labels": True
    },
    "pie": {
        "type": PlotterType.PIE
    },
    "bar": {
        "type": PlotterType.BAR
    },
    "multibar": {
        "type": PlotterType.MULTIBAR
    },
    "marked_plot": {
        "type": PlotterType.PLOT,
        "marker": "-o"
    },
    "marked_multiplot": {
        "type": PlotterType.MULTIPLOT,
        "marker": "-o"
    },
    "multimatrixscatterbin": {
        "type": PlotterType.MULTIMATRIXSCATTERBIN
    },
    "multiscatter": {
        "type": PlotterType.MULTISCATTER
    },
    "bcm2711b0_layout_multimatrixbin": {
        "type": PlotterType.MULTIMATRIXSCATTERBIN,
        "image": "chips/bcm2711b0/bcm2711b0_layout_bw.jpg",
        "scale_to_image": True,
        "x_ticklabels": [i for i in range(7+1)],
        "x_ticklabels_position": [i*114 for i in range(7+1)],
        "y_ticklabels": [i for i in range(6+1)],
        "y_ticklabels_position": [i*117 for i in range(6+1)],
        "x_label": "X position (mm)",
        "y_label": "Y position (mm)"
    },
    "bcm2837_multimatrixbin": {
        "type": PlotterType.MULTIMATRIXSCATTERBIN,
        "image": "chips/bcm2837/bcm2837_square_mirror.jpg",
        "scale_to_image": True,
        "x_ticklabels": reversed([str(i) for i in range(15)]),
        "x_ticklabels_position": [i*26.643 for i in range(15)],
        "y_ticklabels": [str(i) for i in range(15)],
        "y_ticklabels_position": [i*26.643 for i in range(15)],
        "x_label": "Position (mm)",
        "y_label": "Position (mm)",
        "revert_x_axis": True
    },
}
