---
layout: plugin

id: mote_lighting_control
title: OctoPrint-MoteLightingControl
description: >
  Control a set of [Pimoroni Mote]
  (https://shop.pimoroni.com/products/mote) lights - with different OctoPrint
  conditions causing changes in the lighting colour and state.
authors:
- Nigel Metheringham
license: AGPLv3

# TODO
date: 2021-07-09

homepage: https://github.com/nigelm/OctoPrint-MoteLightingControl
source: https://github.com/nigelm/OctoPrint-MoteLightingControl
archive: https://github.com/nigelm/OctoPrint-MoteLightingControl/archive/main.zip

# TODO
# Set this to true if your plugin uses the dependency_links setup parameter to include
# library versions not yet published on PyPi. SHOULD ONLY BE USED IF THERE IS NO OTHER OPTION!
#follow_dependency_links: false

# TODO
tags:
- a list
- of tags
- that apply
- to your plugin
- (take a look at the existing plugins for what makes sense here)

# TODO
screenshots:
- url: url of a screenshot, /assets/img/...
  alt: alt-text of a screenshot
  caption: caption of a screenshot
- url: url of another screenshot, /assets/img/...
  alt: alt-text of another screenshot
  caption: caption of another screenshot
- ...

# TODO
featuredimage: url of a featured image for your plugin, /assets/img/...

# TODO
# You only need the following if your plugin requires specific OctoPrint versions or
# specific operating systems to function - you can safely remove the whole
# "compatibility" block if this is not the case.

compatibility:
  # Python 3 only so we restrict octoprint too.  Allow windows, but don't realistically
  # expect it to work there!
  octoprint:
  - 1.4.0
  os:
  - linux
  - windows
  - macos
  - freebsd
  python: ">=3,<4"

---

Control a set of [Pimoroni Mote]
(https://shop.pimoroni.com/products/mote) lights - with different OctoPrint
conditions causing changes in the lighting colour and state.

In theory the code will support both the USB and Phat (Pi Zero hat) versions
of the Mote controllers, however I have only tested it with USB, and a Pi
Zero is not suitable for running OctoPrint, so is not likely to be used.

## Configuration

The configuration allows you to select the colours used for each OctoPrint state.
The selectable states, and their default colours are:-

- *On OctoPrint Startup* - Blue
- *Printer Connected* - Green
- *Printer Disconnected* - Black (lights off)
- *File Uploaded* - Yellow for a few seconds
- *Active Printing* - White
- *Print Finished* - Pink
- *Error* or *Print Failed* - Red

## Credits

This plugin draws very heavily on [`OctoPrintMote`]
(https://github.com/topshed/OctoPrintMote) by [Richard Hayler]
(https://github.com/topshed)

Additionally some code was used from [`OctoLight`]
(https://plugins.octoprint.org/plugins/octolight/) (the API handling code and
js), and [`TP-Link Smartplug`]
(https://plugins.octoprint.org/plugins/tplinksmartplug/).  Unfortunately the
plugin documentation is insufficiently complete to make sole use of - so
inspecting other plugins is the only option.
