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
# fixme: check if I use this
import octoprint.slicing
import subprocess

class PBCuraEnginePlugin(octoprint.plugin.StartupPlugin,
                         octoprint.plugin.SettingsPlugin,
                         octoprint.plugin.BlueprintPlugin,
                         octoprint.plugin.SlicerPlugin):

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

        # This currently fails. I reported to Gina via:
        # https://github.com/foosel/OctoPrint/issues/2664

        self._slicing_manager.save_profile("PBCuraEngine",
                                           "Test_One",
                                           slicer_settings,
                                           overrides=None,
                                           allow_overwrite=True,
                                           display_name=None,
                                           description=None)
        return flask.jsonify(result)

    def is_slicer_configured(self):
        # fixme: actually do stuff here.
        self._logger.info("Slicer configuration check")
        return True

    def get_slicer_properties(self):
        return dict(type="PBCuraEngine",
                    name="Printrbot Cura Slicer",
                    same_device=True,
                    progress_report=False,
                    source_file_types=["stl"],
                    destination_extensions=["gcode"])


    def get_slicer_default_profile(self):
        profile_path = "./simple.json"
        return self.get_slicer_profile(profile_path)

    def get_slicer_profile(self, path):
        file_handle = open(path, 'r')
        slicer_settings = json_load(file_handle)
        # fixme: Below is a hack. Gina embeds the metadata in the profile.
        # I also don't like the direct call to octoprint.slicing.SlicingProfile
        return octoprint.slicing.SlicingProfile("PBCuraEngine",
                                                "Test_One",
                                                slicer_settings,
                                                overrides=None,
                                                allow_overwrite=True,
                                                display_name=None,
                                                description="Slicer Test")
        
    def on_after_startup(self):
        self._logger.info("PBCuraEngine Plugin is running")
        self._logger.info(self._identifier)
        self._logger.info("Slicer list:")
        self._logger.info(self._slicing_manager.registered_slicers)
        self._slicing_manager.initialize()
        
    def do_slice(self, model_path, printer_profile, machinecode_path=None,
                 profile_path=None, position=None, on_progress=None,
                 on_progress_args=None, on_progress_kwargs=None):
                
        self._logger.info("We're starting a slice. Buckle up.")

                
        # we have our executable:
        cura_path = self._settings.get(["cura_engine"])
        self._logger.info(cura_path)

        # we will need to generate a slicing profile.
        # this should be handled via get_slicer_default_profile
        slicing_profile = self.get_slicer_default_profile()
        self._logger.info(slicing_profile)

        # get our additional args that are outside of the
        # printing profile, if we need this.
        args = []
        args.append(cura_path)
        args.append("slice")
        my_result = ""
        
        # then run the thing.
        try:
            my_result = subprocess.check_output(args,
                                                stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            self._logger.info("Something went wrong with slicer")
            my_result = e.output

        self._logger.info(my_result)
        
        # self._slicing_manager.saved_profile() is a good one
        # http://docs.octoprint.org/en/master/modules/slicing.html#octoprint.slicing.SlicingManager

                
__plugin_name__ = "PBCuraEngine"

def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = PBCuraEnginePlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {

	}
