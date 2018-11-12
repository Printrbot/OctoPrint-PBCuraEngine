# OctoPrint-PBCuraEngine

PBCuraEngine is a plugin that adds the 'latest' CuraEngine slicer to
OctoPrint running on a Raspberry Pi.

We use the "PB" prefix because Cura is a pretty overloaded term, but
to be super-clear, this plugin uses "vanilla" CuraEngine with no modifications/enhancements. 

## Setup

Install via the bundled [Plugin Manager](https://github.com/foosel/OctoPrint/wiki/Plugin:-Plugin-Manager)
or manually using this URL:

      https://github.com/Printrbot/OctoPrint-PBCuraEngine/archive/master.zip

To use this plugin, you must have [CuraEngine](https://github.com/Ultimaker/CuraEngine/blob/master/README.md)
and its dependencies installed on your system. This plugin was
originally integrated with the version 3.x CuraEngine code.

## Configuration

Under plugins->PBCuraEngine, you can set the following options:

      default_profile: The default OctoPrint slicer profile.
      setting_json: The default Cura setting.json (printer profile).
      setting_json_path: Location of the setting.json config files.
      cura_engine: Location of the CuraEngine executable.

## Slicer Settings

Slicer Settings are controlled via three "layers" of settings.

(helpful image goes here)

### Cura Settings.json

Cura is designed to use .json "printer profiles" that describe
printer-specific slicing settings.

If you have a Printbot Simple, there is a simple.json file installed
in the app. This .json file inherits most of its settings from the
generic profile "fdmprinter.def.json". This generic profile in turn
uses a generic extruder profile "fdmextruder.def.json".

As the Cura developers add new slicer settings to the app, they add
reasonable default values to them as part of the generic profile, so
you don't have to constantly update your printer-specific profile.

These profiles are required by command-line CuraEngine, but the files
aren't bundled with the CuraEngine code (they are in the Cura
frontend, project.) We're including default and some Printrbot
profiles as part of the slicer project files right now, but you can
easily add others if you with.

TODO: Right now there isn't a way to manually or automatically change
the printer profile used except editing the config.yaml file. This
will eventually be added to the UI.

### Octoprint Slicer Profile

OctoPrint has a built-in idea of slicing profiles. There are the
slicer settings options that are available in the default slicer UI in
OctoPrint.

We intend to ship with a few pre-defined profiles that allow the user
to select between different levels of print quality. This will be
similar to Cura's Fine/Draft/Coarse slider.

### Material Override

Based on the print material you have selected, you'll want to adjust
bed temperature, hotend temperature and maybe other variables. TODO:
Eventually, the plugin will also deliver these adjustments to the
slicer profile when you trigger a slice.
