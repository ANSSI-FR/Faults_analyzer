from plotter import PlotterType

temp = {
}

styles = {
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
        "y_ticklabels_fontsize": 16,
        "x_label_fontsize": 16,
        "y_label_fontsize": 16,
        "legend_fontsize": 16
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
