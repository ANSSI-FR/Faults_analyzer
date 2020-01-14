from plotter import PlotterType

tmp_style = {
}

def even_str(v):
    if v%2 == 0:
        return str(v)
    else:
        return ""

styles = {
    "intel_core_i3":{
        "type": PlotterType.MATRIXSCATTER,
        "image": "chips/intel_core_i3_large.jpg",
        "scale_to_image": True,
        "x_ticklabels": [even_str(i) for i in range(29)],
        "x_ticklabels_position": [i*49.21 for i in range(29)],
        "y_ticklabels": [even_str(i) for i in range(29)],
        "y_ticklabels_position": [i*46.43 for i in range(29)],
        "x_label": "Position (mm)",
        "y_label": "Position (mm)",
        "ticklabels_fontsize": 16,
        "x_label_fontsize": 16,
        "y_label_fontsize": 16,
        "colorbar_fontsize": 16,
    },
    "matrix":{
        "type": PlotterType.MATRIX
    },
    "bcm2837": {
        "type": PlotterType.MATRIXSCATTER,
        "image": "chips/bcm2837_square_mirror.jpg",
        "scale_to_image": True,
        "x_ticklabels": reversed([str(i) for i in range(15)]),
        "x_ticklabels_position": [i*26.643 for i in range(15)],
        "y_ticklabels": [str(i) for i in range(15)],
        "y_ticklabels_position": [i*26.643 for i in range(15)],
        "x_label": "Position (mm)",
        "y_label": "Position (mm)",
        "ticklabels_fontsize": 16,
        "x_label_fontsize": 16,
        "y_label_fontsize": 16,
        "colorbar_fontsize": 16,
        "revert_x_axis": True
    },
    "large_dist": {
        "type": PlotterType.BAR,
        "rotate_x_labels": True,
        "y_ticklabels_fontsize": 20,
        "x_ticklabels_fontsize": 20,
        "x_label_fontsize": 20,
        "y_label_fontsize": 20,
        "legend_fontsize": 20
    },
    "pie": {
        "type": PlotterType.PIE,
        "labels_fontsize": 16
    },
    "bar": {
        "type": PlotterType.BAR,
        "x_ticklabels_fontsize": 16,
        "y_ticklabels_fontsize": 16,
        "x_label_fontsize": 16,
        "y_label_fontsize": 16,
        "legend_fontsize": 16
    },
    "multibar": {
        "type": PlotterType.MULTIBAR,
        "x_ticklabels_fontsize": 16,
        "y_ticklabels_fontsize": 16,
        "x_label_fontsize": 16,
        "y_label_fontsize": 16,
        "legend_fontsize": 16
    }
}
