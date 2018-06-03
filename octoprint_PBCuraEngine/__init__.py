# coding=utf-8
from __future__ import absolute_import

""" 

These settings are required in config.yaml for this to work:

plugins:
  PBCuraEngine:
    cura_engine: /home/pi/CuraEngine/build/CuraEngine
    default_profile: /home/pi/.octoprint/slicingProfiles/PBCuraEngine/Test_One.profile


Additionally, the limitation with slicing profiles can be avoided by entering the following:

slicing:
  defaultProfiles:
    PBCuraEngine: Test_One

"""

import octoprint.plugin
# fixme: check if I use this
import octoprint.slicing
import subprocess
import os

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

        upload_name = flask.request.values.get("file.name", None)
        upload_path = flask.request.values.get("file.path", None)
        
        file_handle = open(upload_path, 'r')
        self._logger.info("Maybe we have a file")

        # convert the file to JSON
        slicer_settings = json.load(file_handle)
        self._logger.info(slicer_settings)
        self._logger.info(self._slicing_manager.registered_slicers)

        # fixme: need to generate profile_name from the file path
        # (or the json parameter) 
        
        self._slicing_manager.save_profile("PBCuraEngine",
                                           "Test_Three",
                                           slicer_settings,
                                           overrides=None,
                                           allow_overwrite=True,
                                           display_name=None,
                                           description=None)
        # Fixme: this should redirect to root.
        return flask.jsonify(result)

    def is_slicer_configured(self):
        # fixme: actually do stuff here.
        # note: this gets called every time UI renders. 
        # (so I'm putting a bunch of diagnostic printfs here)
        self._logger.info("Slicer configuration check")
        self._logger.info(self._slicing_manager.registered_slicers)
        self._logger.info("Profile List:")
        # fixme: this has stopped showing named profiles.
        self._logger.info(self._slicing_manager.all_profiles("PBCuraEngine"))
        return True

    def get_slicer_properties(self):
        return dict(type="PBCuraEngine",
                    name="Printrbot Cura Slicer",
                    same_device=True,
                    progress_report=False,
                    source_file_types=["stl"],
                    destination_extensions=["gcode"])


    def get_slicer_default_profile(self):
        # if this isn't specified in config.yaml, override with bundled file
        pr_path = self._settings.get(["default_profile"])
        if not pr_path:
            # fixme: maybe use a better name than Test_One.profile.
            pr_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                   "profiles", "Test_One.profile")
            
        return self.get_slicer_profile(pr_path)

    def get_slicer_profile(self, path):
        # this is called to populate the list of slicer profiles
        # based on the .profile files located in:
        # ~/.octoprint/slicingProfiles/<slicerName>/

        # there's a function in types.py, get_slicer_profiles, that
        # handles this for OctoPrint. 
        
        # This is going to open the file located in
        # ~/.octoprint/slicingProfiles/<slicerName>/profileName.profile

        self._logger.info("Getting slicer profile. Path:")
        self._logger.info(path)

        import json
        file_handle = open(path, 'r')
        slicer_settings = json.load(file_handle)        


        display_name = None
        description = None
        slicer_name = self.get_slicer_properties()["type"]
        profile_name = None
    
        # using Gina's convention to pass metadata
        if "_display_name" in slicer_settings:
            display_name = slicer_settings["_display_name"]
            del slicer_settings["_display_name"]
        if "_description" in slicer_settings:
            description = slicer_settings["_description"]
            del slicer_settings["_description"]

        # grab the profile name from the path
        # fixme: keep an eye if tempfile paths are provided here often. 
        # (this may not work if using tmpfile)
        p_path = os.path.splitext(path)
        profile_name = path[0]
        
        # Fixme:
        # I don't like the direct call to octoprint.slicing.SlicingProfile
        return octoprint.slicing.SlicingProfile(slicer_name,
                                                profile_name,
                                                slicer_settings,
                                                display_name,
                                                description)

    def save_slicer_profile(self, path, profile, allow_overwrite=True,
                            overrides=None):

        import json
        self._logger.info("We're saving a slicer profile")
        self._logger.info(path)
        # This is called when do_slicer is invoked. OctoPrint writes the
        # SlicingProfile to a temp file with this mechanism.

        # fixme: ignores overrides. These should be blended with
        # the profile.
        # fixme: no belts or suspenders here. Add error checking.
        file_handle = open(path, "w")
        json.dump(profile.data, file_handle)
        file_handle.close()
        
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
        self._logger.info("Here's the profile_path.")
        self._logger.info(profile_path)
        
        # we don't expect to be given a machinecode_path, so infer
        # from the model_path
        if not machinecode_path:
            m_path = os.path.splitext(model_path)
            machinecode_path=path[0] + ".gcode"
        
        # fixme: steps required are:
        # 1) make sure this code works properly with a known
        # good slicing file. [check] 
        # 2) use subprocess (or sarge) to properly thread the task
        # 3) add the ability to measure slicing progress
        # 4) add the abilty to cancel slicing in progress

        # We base the slicing on the fdmprinter.def.json that is packaged
        # with Cura (not CuraEngine) and then set PB-specific machine
        # overrides with the .profile.

        # nb: This could be incorrect! Maybe if I am specifying the
        # default printer in the config.yaml, that's easy to change. 
        
        # CuraEngine command line isn't happy without a printer.def.json
        # (and extruder.def.json) file fed to it. 

        # Cura Executable from config.yaml:
        cura_path = self._settings.get(["cura_engine"])
        self._logger.info(cura_path)

        # Grab settings.json from config.yaml (fallback to default)
        # This is the 'settings.json' file that curaEngine cmd line
        # wants (and is prefixed with -j). DO NOT confuse with
        # printer_profile which is stored in ~/.octoprint/slicingProfiles
        # and is a list of individual -s overrides. 
        # Fixme: confirm that the default AND config-specified both work.
        # Fixme: I'm bothered by the overloading of "profiles" here.
        # Path and profile are separate config settings. 
        settings_json_path = self._settings.get(["settings_json_path"])
        if not settings_json_path:
            settings_json_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "profiles")
        # Now the profile.
        settings_json = self._settings.get(["settings_json"])
        if not settings_json:
            settings_json = "fdmprinter.def.json"
        
        # Slicing Profile from system
        slice_vars = None
        if profile_path:
            #slice_profile = self.get_slicer_default_profile()
            slice_profile = self.get_slicer_profile(profile_path)
            slice_vars = slice_profile.data
            self._logger.info("Here are the slicing variables, recovered")
            self._logger.info(slice_vars)
        else:
            self._logger.info("we didn't get a profile path for do_slice")
            slice_profile = self.get_slicer_default_profile()
            slice_vars = slice_profile.data
        
        args = []
        args.append(cura_path)
        args.append("slice")

        # The settings.json profile we're going to use as the base.
        # Profiles can inherit settings from others, as long as they're
        # located in the same folder (settings_json_path).
        args.append("-j")
        args.append(os.path.join(settings_json_path, settings_json))

        # Turn on verbose (-v) and progress (-p) logging.
        args.append("-v")
        args.append("-p")
        
        # line width, and a few others, should be set based on nozzle size.
        # fixme: going to need more than just line_width.
        args.append("-s")
        args.append("line_width=0.3")

        if slice_vars:
            for key in slice_vars:
                args.append("-s")
                args.append(key + "=" + str(slice_vars[key]))
        
        args.append("-o")
        args.append(machinecode_path)
        args.append("-l")
        args.append(model_path)
        
        my_result = ""

        self._logger.info(args)
        
        # then run the thing.
        # fixme: this should be made more robust, and cancel-able.
        # in order to do that, we need to keep a finger on the thread.
        try:
            my_result = subprocess.check_output(args,
                                                stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            self._logger.info("Something went wrong with slicer")
            my_result = e.output

        self._logger.info(my_result)

        # fixme: need to return something, a dict with info about the
        # slicing job.

__plugin_name__ = "PBCuraEngine"

def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = PBCuraEnginePlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {

	}
