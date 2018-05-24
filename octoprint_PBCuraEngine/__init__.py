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
import octoprint.slicing

class PBCuraEnginePlugin(octoprint.plugin.StartupPlugin,
                         octoprint.plugin.SettingsPlugin,
                         octoprint.plugin.BlueprintPlugin):

    """ 
    Using this for development right now to manually upload the slicing 
    profiles
    """
    @octoprint.plugin.BlueprintPlugin.route("/upload", methods=["POST"])
    def upload_slicing_profile(self):
        self._logger.info("Calling the profile upload page")
        
        import flask
        import json

        result = dict(
            found_file=False,
        )

        input_name = "file"
        keys = ("name", "size", "content_type", "path")
                
        # prove to ourselves that the file object doesn't exist
        # like flask says it should. 
        if 'file' not in flask.request.files:
            result["status"] = "No file found"
        else:
            result["status"] = "Found a file"

        # this is for debugging purposes, but I use the variables below.
        # fixme: clean this up.
        for key in keys:
            param = input_name + "." + key
            if param in flask.request.values:
                result["found_file"] = True
                result[key] = flask.request.values[param]

        self._logger.info(result)
        
        file_handle = open(result['path'], 'r')
        self._logger.info("Maybe we have a file")

        # convert the file to JSON
        slicer_settings = json.load(file_handle)
        self._logger.info(slicer_settings)
        self._logger.info(self._slicing_manager.registered_slicers)
        self._slicing_manager.save_profile("PBCuraEngine",
                                           "Test_One",
                                           slicer_settings,
                                           overrides=None,
                                           allow_overwrite=True,
                                           display_name=None,
                                           description="Slicer Test")

        self._logger.info(self._slicing_manager.get_slicer_profile_path("PBCuraEngine"))
                
        return flask.jsonify(result)


        #self._logger.info("one")
        # take a file in
        #file_name = flask.request.values[file.name]
        #self._logger.info("two")
        #file_path = flask.request.values[file.path]
        #self._logger.info("three")
        #file_handle = open(file_path, 'r')
        #self._logger.info("Maybe we have a file")
        
        # convert the file to JSON
        #slicer_settings = json.load(file_handle)
        #self._logger.info(slicer_settings)
        
        # save the profile with self._slicing_manager.save_profile()
                

    def is_slicer_configured(self):
        # fixme: actually do stuff here.
        return True

    def get_slicer_properties(self):
        return dict(type="PBCuraEngine",
                    name="Printrbot Cura Slicer",
                    same_device=True,
                    progress_report=False,
                    source_file_types=["stl"],
                    destination_extensions=["gcode"])


#        def get_slicer_default_profil(self):
#                profile_path = "./simple.json"
#                return self.get_slicer_profile(profile_path)
#
#        def get_slicer_profile(self, path):
#                file_handle = open(path, 'r')
#                slicer_settings = json_load(file_handle)
#                # fixme: I don't like this below
#                return octoprint.slicing.SlicingProfile("PBCuraEngine", "Test_One", slicer_settings, overrides=None, allow_overwrite=True, display_name=None  description="Slicer Test")
        
    def on_after_startup(self):
        self._logger.info("PBCuraEngine Plugin is running")
        self._logger.info(self._identifier)
        self._logger.info("Slicer list:")
        self._logger.info(self._slicing_manager.registered_slicers)
                
#        def do_slice(self, model_path, printer_profile, machinecode_path=None,
#                     profile_path=None, position=None, on_progress=None,
#                     on_progress_args=None, on_progress_kwargs=None):
#                
#                self._logger.info("We're starting a slice. Buckle up.")

                
                # we have our executable:
                # self._settings.get(["cura_engine"])

                # we will need to generate a slicing profile.
                # perhaps _slicing_manager helps with this.

                # get our additional args that are outside of the
                # printing profile, if we need this.

                # then run the thing.
                
                # self._slicing_manager.saved_profile() is a good one
                # http://docs.octoprint.org/en/master/modules/slicing.html#octoprint.slicing.SlicingManager

                # so, first todo here is to upload the simple.json
                # file to the profile. Even better would be to add a quality
                # setting, but let's not get ahead of ourselves. 
                
                
__plugin_name__ = "PBCuraEngine"

def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = PBCuraEnginePlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {

	}


        
