import time

import octoprint.plugin

# initial mote import
try:
    from mote import Mote

    mote_type = "USB"

except ImportError:
    try:
        import motephat as mote

        mote_type = "PHAT"
    except ImportError:
        import sys

        sys.exit(-1)


# -----------------------------------------------------------------------
class MoteLightingControlPlugin(
    octoprint.plugin.SettingsPlugin,
    octoprint.plugin.AssetPlugin,
    octoprint.plugin.TemplatePlugin,
    octoprint.plugin.StartupPlugin,
    octoprint.plugin.EventHandlerPlugin,
):

    # -----------------------------------------------------------------------
    def __init__(self):
        self.mote = None
        self.mote_type = None
        self.colour = "#0000ff"
        self.lights_on = False

    # -----------------------------------------------------------------------
    def check_initialised(self):
        if self.mote is None:
            self.initialise_leds()

    # -----------------------------------------------------------------------
    def initialise_leds(self):
        if self.mote is not None:
            self._logger.warning("Attempting to initialise an already initialised mote system")
        self.mote_type = mote_type
        self._logger.info(f"Initialising Mote({self.mote_type}) Lighting")
        if self.mote_type == "USB":
            self.mote = Mote()
            # set up 4 channels
            for channel in range(1, 5):
                self.mote.configure_channel(channel=1, num_pixels=16, gamma_correction=False)
        else:
            self.mote = mote
        self.set_leds(self.lights_on, self.colour)

    # -----------------------------------------------------------------------
    def set_leds(self, lights_on: bool = True, colour: str = "#0000ff"):
        hex = colour.lstrip("#")
        red, green, blue = tuple(int(hex[i : i + 2], 16) for i in (0, 2, 4))
        if lights_on is False or (red == 0 and green == 0 and blue == 0):
            self._logger.info("Mote: setting LEDs off")
            self.lights_on = False
            self.mote.clear()
        else:
            self._logger.info(f"Mote: setting LEDs on to colour {colour}")
            self.lights_on = True
            self.colour = colour
            self.mote.set_all(r=red, g=green, b=blue, brightness=1.0)
        self.mote.show()

    # -----------------------------------------------------------------------
    def on_after_startup(self):
        self._logger.info("Startup of Mote Lighting")
        self.check_initialised()

    # -----------------------------------------------------------------------
    def on_event(self, event, payload):
        self.check_initialised()
        initial_lights_on = self.lights_on
        initial_colour = self.colour
        transitory = False
        lights_on = True
        colour = "#0000ff"  # deep blue - not used elsewhere
        if event == "Startup":
            colour = self._settings.get(["startup_colour"])
        elif event == "Connected":
            colour = self._settings.get(["connect_colour"])
        elif event == "Disconnected":
            colour = self._settings.get(["disconnect_colour"])
        elif event == "Upload":
            colour = self._settings.get(["upload_colour"])
            transitory = True
        elif event == "PrintStarted":
            colour = self._settings.get(["printing_colour"])
        elif event == "PrintFailed" or event == "Error":
            colour = self._settings.get(["error_colour"])
        elif event == "PrintDone":
            colour = self._settings.get(["done_colour"])
        elif event == "ClientOpened":
            colour = self._settings.get(["connect_colour"])
            transitory = True
        elif event == "ClientClosed":
            colour = self._settings.get(["error_colour"])
            transitory = True
        else:
            # not an event we handle... just return
            return

        self._logger.info(f"Mote: Setting lighting for event {event} to colour {colour}")
        self.set_leds(lights_on=lights_on, colour=colour)
        if transitory:
            time.sleep(4.0)
            self.set_leds(lights_on=initial_lights_on, colour=initial_colour)

    # -----------------------------------------------------------------------
    def get_settings_defaults(self):
        """Default settings for the plugin"""
        return dict(
            lights_on=False,  # lights currently off
            current_colour="#FFFFFF",  # current - white
            mote_type=mote_type,
            startup_colour="#94adff",  # startup - blue
            error_colour="#FF0000",  # error - red
            printing_colour="#FFFFFF",  # printing - white
            connect_colour="#96fa91",  # connect - green
            done_colour="#ff8cc9",  # completed - pink
            upload_colour="#ffff00",  # upload - yellow
            disconnect_colour="#000000",  # disconnect - black/off
        )

    # -----------------------------------------------------------------------
    def get_template_configs(self):
        return [dict(type="navbar", custom_bindings=False), dict(type="settings", custom_bindings=False)]

    # -----------------------------------------------------------------------
    def get_assets(self):
        # Define your plugin's asset files to automatically include in the
        # core UI here.
        return {
            "js": ["js/mote_lighting_control.js"],
            "css": ["css/mote_lighting_control.css"],
            "less": ["less/mote_lighting_control.less"],
        }

    # -----------------------------------------------------------------------
    def get_update_information(self):
        # Define the configuration for your plugin to use with the Software Update
        # Plugin here. See https://docs.octoprint.org/en/master/bundledplugins/softwareupdate.html
        # for details.
        return {
            "mote_lighting_control": {
                "displayName": "Mote_lighting_control Plugin",
                "displayVersion": self._plugin_version,
                # version check: github repository
                "type": "github_release",
                "user": "nigelm",
                "repo": "OctoPrint-MoteLightingControl",
                "current": self._plugin_version,
                # update method: pip
                "pip": "https://github.com/nigelm/OctoPrint-MoteLightingControl/archive/{target_version}.zip",
            },
        }


# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "Mote Lighting Control Plugin"
__plugin_pythoncompat__ = ">=3,<4"  # only python 3


def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = MoteLightingControlPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information,
    }
