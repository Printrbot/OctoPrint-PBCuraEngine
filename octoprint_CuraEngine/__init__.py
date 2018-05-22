# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin

class CuraEnginePlugin(octoprint.plugin.StartupPlugin):

        def on_after_startup(self):
                self._logger.info("CuraEngine Plugin is running")

__plugin_name__ = "CuraEngine Plugin"

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = CuraEnginePlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {

	}

