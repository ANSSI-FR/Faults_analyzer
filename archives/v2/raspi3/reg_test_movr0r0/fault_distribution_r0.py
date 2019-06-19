import sys

sys.path.append("/media/nas/projects/Fault_attacks/EM/Raspi3/NEW_MANIP/liblsc")

from ManipUtils.plotter import Plotter

fault_dist = [16,2,2,1,2,2,1]
fault_labels = ["Fixed value", "Other reg", "Comp of other reg", "Close to other reg", "all 0", "all 1", "all flip"]

to_plot = [{
    "title": "Fault distribution on r0",
    "type" : "bar",
    "data" : fault_dist,
    "x_ticklabels": fault_labels,
    "show_data_value": True,
    "data_value_fontsize": 16
}]

pl = Plotter(to_plot)
pl.init_plot()
pl.show()
