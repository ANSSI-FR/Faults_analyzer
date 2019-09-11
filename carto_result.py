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
