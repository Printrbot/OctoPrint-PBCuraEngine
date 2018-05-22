# coding=utf-8
from __future__ import absolute_import

""" 

These settings are required in config.yaml for this to work:

plugins:
  PBCuraEngine:
    simple_profile: simple.json
    cura_engine: /home/pi/CuraEngine/build/CuraEngine
 
"""

import octoprint.plugin

class PBCuraEnginePlugin(octoprint.plugin.StartupPlugin,
                         octoprint.plugin.SettingsPlugin):

        def on_after_startup(self):
                self._logger.info("PBCuraEngine Plugin is running")

        def do_slice(self, model_path, printer_profile, machinecode_path=None,
                     profile_path=None, position=None, on_progress=None,
                     on_progress_args=None, on_progress_kwargs=None):
                
                self._logger.info("We're starting a slice. Buckle up.")

                
                # we have our executable:
                # self._settings.get(["cura_engine"])

                # we will need to generate a slicing profile.
                # perhaps _slicing_manager helps with this.

                # get our additional args that are outside of the
                # printing profile, if we need this.

                # then run the thing.
                
                # self._slicing_manager.saved_profile() is a good one
                # http://docs.octoprint.org/en/master/modules/slicing.html#octoprint.slicing.SlicingManager

                
                
__plugin_name__ = "PBCuraEngine"

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = PBCuraEnginePlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {

	}


        
