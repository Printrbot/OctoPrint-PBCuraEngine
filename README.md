# OctoPrint-PBCuraEngine

**TODO:** Describe what your plugin does.

## Setup

Install via the bundled [Plugin Manager](https://github.com/foosel/OctoPrint/wiki/Plugin:-Plugin-Manager)
or manually using this URL:

    https://github.com/BDFife/OctoPrint-PBCuraEngine/archive/master.zip

**TODO:** Describe how to install your plugin, if more needs to be done than just installing it via pip or through
the plugin manager.

## Configuration

**TODO:** Describe your plugin's configuration options (if any).

## Slicer Profiles

Cura is designed to use .json profiles that describe printer-specific
slicing settings.

If you have a Printbot Play, there would be a Play.json file installed
in the app. This .json file inherits most of its settings from the
generic profile "fdmprinter.def.json". This generic profile in turn
uses a generic extruder profile "fdmextruder.def.json".

As the Cura developers add new slicer settings to the app, they add
reasonable default values to them as part of the generic profile, so
you don't have to constantly update your printer-specific profile.

Unfortunately, even though these profiles are required by command-line
CuraEngine, the files aren't bundled with the CuraEngine code (they
are in the Cura, frontend, project.) We're including the standard
profiles as part of the slicer project files right now.


