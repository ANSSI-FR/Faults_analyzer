from plotter import PlotterType

class CartoResult():

    title = ""
    data = ""
    label = ""

    def __init__(self, title, data, label):
        self.title = title
        self.data = data
        self.label = label

    def __str__(self):
        ret = self.title + "\n"
        ret += str(self.data)
        return ret

    def get_to_plot(self, to_plot_params):
        to_plot = {}
        if (to_plot_params["type"] == PlotterType.MATRIX) or (to_plot_params["type"] == "matrix"):
            to_plot = self.result_to_matrix(to_plot_params)
        if (to_plot_params["type"] == PlotterType.MATRIXSCATTER) or (to_plot_params["type"] == "matrixscatter"):
            to_plot = self.result_to_matrixscatter(to_plot_params)
        if "plot_style" in to_plot_params:
            to_plot.update(to_plot_params["plot_style"])
        return to_plot

    def result_to_matrix(self, to_plot_params):
        to_plot = {
            "data": self.data,
            "type": PlotterType.MATRIX,
        }
        return to_plot

    def result_to_matrixscatter(self, to_plot_params):
        to_plot = {
            "data": self.data,
            "type": PlotterType.MATRIXSCATTER,
        }
        return to_plot

######### TEST ###########
import numpy as np
from plotter import Plotter

if __name__ == "__main__":
    res = {
        "title": "Test",
        "data": np.random.randint(0, 10, (50,50)),
        "label": "The label"
    }

    r = CartoResult(**res)
    print(r)

    to_plot_params_list = [
        {
            "type": PlotterType.MATRIX,
        },
        {
            "type": PlotterType.MATRIXSCATTER,
            "plot_style": {
                "image": "bcm2837_square.jpg",
                "scale_to_image": True
            }
        }
    ]

    to_plot = []
    for to_plot_params in to_plot_params_list:
        to_plot.append(r.get_to_plot(to_plot_params))
    pl = Plotter(to_plot)
    pl.show()
