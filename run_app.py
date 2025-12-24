#!/usr/bin/env python3

from submodules.Hub import MultipleApps

from GUIs.logger.data_log import Logger
from GUIs.plotter.plot_data import Plotter


MultipleApps(app_list={'Logger':Logger,'Plotter':Plotter}).init_start()
#AfmApp().init_start()
