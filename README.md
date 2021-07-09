# OctoPrint-MoteLightingControl

Version: `0.2.0`

Control a set of [Pimoroni Mote]
(https://shop.pimoroni.com/products/mote) lights - with different OctoPrint
conditions causing changes in the lighting colour and state.

In theory the code will support both the USB and Phat (Pi Zero hat) versions
of the Mote controllers, however I have only tested it with USB, and a Pi
Zero is not suitable for running OctoPrint, so is not likely to be used.

## Setup

Install via the bundled [Plugin Manager](https://docs.octoprint.org/en/master/bundledplugins/pluginmanager.html)
or manually using this URL:

    https://github.com/nigelm/OctoPrint-MoteLightingControl/archive/main.zip


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

This plugin draws very heavily on
[`OctoPrintMote`](https://github.com/topshed/OctoPrintMote) by
[Richard Hayler](https://github.com/topshed)

Additionally some code was used from
[`OctoLight`](https://plugins.octoprint.org/plugins/octolight/)
(the API handling code and js), and
[`TP-Link Smartplug`](https://plugins.octoprint.org/plugins/tplinksmartplug/).

Unfortunately the plugin documentation is insufficiently complete to make sole
use of - so inspecting other plugins is the only option.
