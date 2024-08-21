#!/usr/bin/env python3

from AppHub.Hub import MultipleApps

from GUIs.logger.data_log import Logger


MultipleApps(app_list={'Logger':Logger}).init_start()
#AfmApp().init_start()
