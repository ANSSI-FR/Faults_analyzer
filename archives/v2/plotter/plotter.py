import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


class Plotter:
    def __init__(self,
                 to_plot=None,
                 nb_to_plot=0,
                 figsuptitle="Title",
                 cmap=plt.cm.jet,
                 figsize=(20, 20)):
        self.figsize = figsize
        self.figsuptitle = figsuptitle
        self.fig = None
        self.to_plot = to_plot
        if self.to_plot is None:
            self.nb_to_plot = nb_to_plot
        else:
            self.nb_to_plot = len(self.to_plot)
        self.axes = None
        self.cmap = cmap
        self.colorbars = None
        self.fig_shown = False
        self.scatters = None
        self.histograms = None
        self.traces = None
        self.bars = None
        self.texts = None

    def set_colormap(self, cmap):
        self.cmap = cmap

    def get_figsize(self):
        return self.figsize

    def set_figsize(self, figsize):
        self.figsize = figsize

    def get_figsuptitle(self):
        return self.figsuptitle

    def set_figsuptitle(self, suptitle):
        self.figsuptitle = suptitle

    def init_fig(self):
        self.fig = plt.figure(figsize=self.figsize)
        self.fig.suptitle(self.figsuptitle)

    def set_to_plot(self, to_plot):
        self.to_plot = to_plot
        self.nb_to_plot = len(to_plot)

    def init_axes(self):
        if self.nb_to_plot < 1:
            print("Error nothing to plot")
            exit(1)
        self.axes = []
        nb_cols = np.ceil(np.sqrt(self.nb_to_plot))
        nb_rows = np.ceil(self.nb_to_plot / nb_cols)
        for i in range(self.nb_to_plot):
            axe = self.fig.add_subplot(nb_rows, nb_cols, i + 1)
            self.axes.append(axe)

    def set_titles(self):
        for i, axe in enumerate(self.axes):
            if "title" in self.to_plot[i]:
                axe.set_title(self.to_plot[i]["title"])

    def set_labels(self):
        for i, axe in enumerate(self.axes):
            if "x_label" in self.to_plot[i]:
                axe.set_xlabel(self.to_plot[i]["x_label"])
            if "y_label" in self.to_plot[i]:
                axe.set_ylabel(self.to_plot[i]["y_label"])

    def set_legends(self):
        for i, axe in enumerate(self.axes):
            if "legend" in self.to_plot[i]:
                axe.legend(self.to_plot[i]["legend"], loc="upper right")

    def set_ticklabels(self):
        for i, axe in enumerate(self.axes):
            if "x_ticklabels" in self.to_plot[i]:
                ind = np.arange(1, len(self.to_plot[i]["x_ticklabels"])+1)
                axe.set_xticks(ind)
                axe.set_xticklabels(self.to_plot[i]["x_ticklabels"])

    def get_bounds_and_norm(self, matrix):
        if matrix.min() != matrix.max():
            bounds = np.linspace(
                int(matrix.min()), int(matrix.max()),
                int(matrix.max() - matrix.min()) + 1)
            norm = mpl.colors.BoundaryNorm(
                np.arange(matrix.min() - 0.5,
                          matrix.max() + 1 + 0.5, 1), self.cmap.N)
            return bounds, norm
        else:
            bounds = np.linspace(matrix.min() - 1, matrix.min() + 1, 3)
            norm = mpl.colors.BoundaryNorm(
                np.arange(matrix.min() - 0.5 - 1,
                          matrix.max() + 1 + 0.5 + 1, 1), self.cmap.N)
            return bounds, norm

    def remove_colorbars(self):
        if not self.colorbars is None:
            for cb in self.colorbars:
                cb.remove()
        self.colorbars = []

    def remove_scatters(self):
        if not self.scatters is None:
            for sc in self.scatters:
                sc.remove()
        self.scatters = []

    def remove_histograms(self):
        if not self.histograms is None:
            for bars in self.histograms:
                for bar in bars:
                    bar.remove()
        self.histograms = []

    def remove_traces(self):
        if not self.traces is None:
            for trace in self.traces:
                l = trace.pop(0)
                l.remove()
        self.traces = []

    def remove_bars(self):
        if not self.bars is None:
            for bars in self.bars:
                for bar in bars:
                    bar.remove()
        self.bars = []

    def remove_texts(self):
        if not self.texts is None:
            for text in self.texts:
                text.remove()
        self.texts = []

    def get_colors(self, to_plot, default):
        if "colors" in to_plot:
            return to_plot["colors"]
        else:
            return default

    def plot_matrix(self, matrix, axe):
        bounds, norm = self.get_bounds_and_norm(matrix)
        z = axe.matshow(matrix, cmap=self.cmap, norm=norm)
        cb = plt.colorbar(z, ax=axe, ticks=bounds)
        self.colorbars.append(cb)

    def plot_scatter(self, to_plot, axe):
        values = to_plot["data"]
        colors = self.get_colors(to_plot, "b")
        sc = axe.scatter(values[0], values[1], s=10, color=colors)
        self.scatters.append(sc)

    def plot_histogram(self, to_plot, axe):
        data = to_plot["data"]
        colors = self.get_colors(to_plot, "b")
        counts, bins, bars = axe.hist(data, bins=50, edgecolor="white", color=colors)
        self.histograms.append(bars)

    def plot_trace(self, to_plot, axe):
        data = to_plot["data"]
        colors = self.get_colors(to_plot, "b")
        tr = axe.plot(data, color=colors)
        self.traces.append(tr)

    def plot_bar(self, to_plot, axe):
        data = to_plot["data"]
        colors = self.get_colors(to_plot, "b")
        ind = np.arange(1, len(data)+1)
        bars = axe.bar(ind, data, color=colors)
        self.bars.append(bars)
        show_data_value = False
        if "show_data_value" in to_plot:
            show_data_value = to_plot["show_data_value"]
        if show_data_value: #TODO: dedicated function
            data_value_color = self.get_color(to_plot["data_value_color"], "w")
            for i, d in enumerate(data):
                t = axe.text(i+1, d/2, str(d), horizontalalignment="center", verticalalignment="center", color=data_value_color, fontsize=12)
                self.texts.append(t)

    def clean_plot(self):
        self.remove_colorbars()
        self.remove_scatters()
        self.remove_histograms()
        self.remove_traces()
        self.remove_bars()
        self.remove_texts()

    def set_informations(self):
        self.set_titles()
        self.set_labels()
        self.set_legends()
        self.set_ticklabels()

    def plot_data(self):
        self.clean_plot()
        self.set_informations()
        for i, axe in enumerate(self.axes):
            to_plot = self.to_plot[i]
            if to_plot["type"] == "matrix":
                self.plot_matrix(to_plot["data"], axe)
            elif to_plot["type"] == "scatter":
                self.plot_scatter(to_plot, axe)
            elif to_plot["type"] == "histogram":
                self.plot_histogram(to_plot, axe)
            elif to_plot["type"] == "trace":
                self.plot_trace(to_plot, axe)
            elif to_plot["type"] == "bar":
                self.plot_bar(to_plot, axe)
                plt.tight_layout()

    def show(self, blocking=True):
        if blocking:
            self.plot_data()
            plt.show()
        else:
            if not self.fig_shown:
                self.fig.show()
                self.fig_shown = True
            self.plot_data()
            self.fig.canvas.draw()

    def init_plot(self):
        self.init_fig()
        self.init_axes()
