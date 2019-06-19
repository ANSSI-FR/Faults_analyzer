from plotter import Plotter
import numpy as np
import time

def build_test():
    matrix = np.random.random((100,100))
    matrix2 = np.random.random((100,100))
    scatter = [np.random.random(30), np.random.random(30)]
    scatter2 = np.random.random((50,50))
    hist = np.random.random(100)
    trace = np.random.random(1000)
    bar = np.random.random(5)

    to_plot = [{
        "title": "Test matrix",
        "type" : "matrix",
        "data" : matrix,
        "x_label": "Abscissa",
        "y_label": "Orderly",
        "legend": ["This is random"]
    },
    {
        "title": "Bars monitoring",
        "type" : "bar",
        "data" : bar,
        "x_label": "X axis",
        "y_label": None,
        "legend": ["Test"],
        "x_ticklabels": ["Naruto", "Sasuke", "Sakura", "Saï", "Kakashi"],
        "show_data_value": False
    },
    {
        "title": "Random scatter",
        "type": "scatter",
        "data": scatter,
        "x_label": None,
        "y_label": "Power level of Naruto over the time",
        "legend": ["chakra"],
        "colors": ["k"]
    },
    {
        "title": "Some histogram",
        "type": "histogram",
        "data": [hist, hist],
        "x_label": "The fucking X axis",
        "y_label": "Best devil fruit",
        "legend": ["The One Piece"],
        "colors": ["r","c"]
    },
    {
        "title": "Side channel",
        "type": "trace",
        "data": trace,
        "x_label": "Time",
        "y_label": "Hamming weight",
        "legend": ["STM32"]
    },
    {
        "title": "Scatter from matrix",
        "type": "scatter",
        "data": scatter2,
        "x_label": None,
        "y_label": None,
        "legend": [None]
    }]

    return to_plot

to_plot = build_test()
pl = Plotter(to_plot, figsuptitle="", nb_to_plot=len(to_plot))
pl.init_plot()
while 1:
    pl.set_to_plot(build_test())
    pl.show(blocking=False)
    time.sleep(0.2)
