# coding=utf-8
from __future__ import absolute_import

""" 

These settings are required in config.yaml for this to work:

plugins:
  PBCuraEngine:
    simple_profile: simple.json
    cura_engine: /home/pi/CuraEngine/build/CuraEngine

Additionally, the limitation with slicing profiles can be avoided by entering the following:

slicing:
  defaultProfiles:
    PBCuraEngine: Test_One

To get this code running, you also need to have a Test_One.profile resident
in the ~/.octoprint/slicingProfiles/PBCuraEngine/ directory. 

Test_One is a special file built from the parameters set in the simple.json 
file used by the printrbot.cloud. 


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

        # I suspect there are two layers of issues - first, the glitch
        # in the logic that I reported.
        # Second, my assumption was that "save profile" would actually
        # put the data in the filesystem (under ~/.octoprint) and so far,
        # it does not, for me. 

        # I can manually work around this for now. 
        # It looks like Gina's plug-in does use save_profile.
        
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
        # note: this gets called every time UI renders. 
        # (so I'm putting a bunch of diagnostic printfs here)
        self._logger.info("Slicer configuration check")
        self._logger.info(self._slicing_manager.registered_slicers)
        self._logger.info("Profile List:")
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
        # Fixme: obviously, hardcoded path.
        #profile_path =
        #"/home/pi/OctoPrint-PBCuraEngine/octoprint_PBCuraEngine//simple.json"
        profile_path = "/home/pi/.octoprint/slicingProfiles/PBCuraEngine/Test_One.profile"
        return self.get_slicer_profile(profile_path)

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

        # fixme: Below is a hack. Gina embeds the metadata in the profile.
        # but I'm not doing that yet. 
        # I also don't like the direct call to octoprint.slicing.SlicingProfile

        # one of the challenges we'll need to deal with is that Cura likes
        # to use a slicing config file (.json) that inherits other profile
        # data, (typically fdmprinter.def.json) *and* also inherits extruder
        # specific data from fdmextruder.def.json or something similar.

        # in order to make this work elegantly with Cura, we should contain
        # all the slicing settings within a single file. 

        # Cura, to the best of my knowledge, doesn't do much to make this
        # easy for people, the most straightforward way to grab all the
        # slicing settings used is to copy all the -s parameters from
        # the Cura log when a slice is prepared. (I'm not blaming them
        # this is not a core use-case for the team)

        # One way to make this easy for users would be to have our slicing
        # profile just capture all those settings and spit them back.

        # No matter what we do, we're going to have to develop some helper
        # scripts, I think to manage the complexity. 

        # I tried to take all the -s commands and bundle them in the Cura
        # settings, but it still wanted to see a fdmprinter and fdmextruder
        # json file. So, current thinking is that we should use the defaults
        # and then use cmd-line settings to override these.
        
        return octoprint.slicing.SlicingProfile("PBCuraEngine",
                                                "Test_One",
                                                slicer_settings,
                                                display_name="Test One",
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

        # we don't expect to be given a machinecode_path.
        if not machinecode_path:
            m_path = os.path.splitext(model_path)
            machinecode_path=path[0] + ".gcode"
        
        # fixme: steps required are:
        # 1) make sure this code works properly with a known
        # good slicing file. 
        # 2) use subprocess (or sarge) to properly thread the task
        # 3) add the ability to measure slicing progress
        # 4) add the abilty to cancel slicing in progress

        # We base the slicing on the fdmprinter.def.json that is packaged
        # with Cura (not CuraEngine) and then set PB-specific machine
        # overrides with the .profile.

        # CuraEngine command line isn't happy without a printer.def.json
        # (and extruder.def.json) file fed to it. 

        # Cura Executable from config.yaml:
        cura_path = self._settings.get(["cura_engine"])
        self._logger.info(cura_path)
        
        # Slicing Profile from system
        # Fixme: this is horribly broken, doesn't use provided path.
        slice_vars = None
        if profile_path:
            slice_profile = self.get_slicer_default_profile()
            slice_vars = slice_profile.data
            self._logger.info("Here are the slicing variables, recovered")
            self._logger.info(slice_vars)
            
            
        else:
            self._logger.info("we didn't get a profile path for do_slice")
        
        
        args = []
        args.append(cura_path)
        args.append("slice")
        args.append("-j")
        # fixme: obviously, this is hardcoded, problematic.
        # put this in settings. 
        args.append("/home/pi/OctoPrint-PBCuraEngine/octoprint_PBCuraEngine/fdmprinter.def.json")
        # line width, and a few others, should be set based on nozzle size.
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
        try:
            my_result = subprocess.check_output(args,
                                                stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            self._logger.info("Something went wrong with slicer")
            my_result = e.output

        self._logger.info(my_result)
        

__plugin_name__ = "PBCuraEngine"

def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = PBCuraEnginePlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {

	}
