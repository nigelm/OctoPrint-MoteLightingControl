import time

import octoprint.plugin
from flask import jsonify
from mote import Mote

mote_type = "USB"  # this is the only possible type now
MAX_MOTE_CHANNELS = 4
MAX_PIXELS_PER_CHANNEL = 16


# -----------------------------------------------------------------------
class MoteLightingControlPlugin(
    octoprint.plugin.SettingsPlugin,
    octoprint.plugin.AssetPlugin,
    octoprint.plugin.TemplatePlugin,
    octoprint.plugin.StartupPlugin,
    octoprint.plugin.EventHandlerPlugin,
    octoprint.plugin.SimpleApiPlugin,
    octoprint.plugin.RestartNeedingPlugin,
):

    # -----------------------------------------------------------------------
    def __init__(self):
        self.mote = None
        self.mote_type = None
        self.colour = "#0000ff"
        self.lights_on = False

    # -----------------------------------------------------------------------
    def check_initialised(self) -> bool:
        if self.mote is None:
            self.initialise_leds()

        return False if self.mote is None else True

    # -----------------------------------------------------------------------
    def initialise_leds(self):
        if self.mote is not None:
            self._logger.warning("Attempting to initialise an already initialised mote system")
        self.mote_type = mote_type
        self._logger.info(f"Initialising Mote({self.mote_type}) Lighting")
        if self.mote_type == "USB":
            try:
                self.mote = Mote()
                # set up 4 channels
                for channel in range(1, MAX_MOTE_CHANNELS + 1):
                    self.mote.configure_channel(
                        channel=channel,
                        num_pixels=MAX_PIXELS_PER_CHANNEL,
                        gamma_correction=False,
                    )
            except OSError as err:
                self._logger.error(f"Error initialising Mote({self.mote_type}) - {err}")
                self.mote = None
        else:
            self._logger.error(f"Unable to initialisw Mote({self.mote_type})")
            self.mote = None

        if self.mote:
            self.set_leds(self.lights_on, self.colour)

    # -----------------------------------------------------------------------
    def set_leds(self, lights_on: bool = True, colour: str = "#0000ff"):
        hex = colour.lstrip("#")
        red, green, blue = tuple(int(hex[i : i + 2], 16) for i in (0, 2, 4))
        if lights_on is False or (red == 0 and green == 0 and blue == 0):
            self._logger.debug("Mote: setting LEDs off")
            self.lights_on = False
            self.mote.clear()
        else:
            self._logger.debug(f"Mote: setting LEDs on to colour {colour}")
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
        if self.check_initialised():
            if self._settings.get_boolean(["on_events"]):
                initial_lights_on = self.lights_on
                initial_colour = self.colour
                transitory = False
                lights_on = True
                colour = "#0000ff"  # deep blue - not used elsewhere
                if event == "Startup" and self._settings.get_boolean(["on_event_startup"]):
                    colour = self._settings.get(["startup_colour"])
                elif event == "Connected" and self._settings.get_boolean(["on_event_connect"]):
                    colour = self._settings.get(["connect_colour"])
                elif event == "Disconnected" and self._settings.get_boolean(["on_event_disconnect"]):
                    colour = self._settings.get(["disconnect_colour"])
                elif event == "Upload" and self._settings.get_boolean(["on_event_upload"]):
                    colour = self._settings.get(["upload_colour"])
                    transitory = True
                elif event == "PrintStarted" and self._settings.get_boolean(["on_event_printing"]):
                    colour = self._settings.get(["printing_colour"])
                elif (event == "PrintFailed" or event == "Error") and self._settings.get_boolean(["on_event_error"]):
                    colour = self._settings.get(["error_colour"])
                elif event == "PrintDone" and self._settings.get_boolean(["on_event_done"]):
                    colour = self._settings.get(["done_colour"])
                elif event == "ClientOpened" and self._settings.get_boolean(["on_event_connect"]):
                    colour = self._settings.get(["connect_colour"])
                    transitory = True
                elif event == "ClientClosed" and self._settings.get_boolean(["on_event_startup"]):
                    colour = self._settings.get(["startup_colour"])
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
    def on_api_get(self, request):
        if self.check_initialised():
            if self.lights_on:
                self.set_leds(lights_on=False)
            else:
                self.set_leds(lights_on=True, colour=self._settings.get(["manual_colour"]))

            self._plugin_manager.send_plugin_message(self._identifier, dict(isLightOn=self.lights_on))
            return jsonify(status="ok")
        else:
            return jsonify(status="unitialised")

    # -----------------------------------------------------------------------
    def get_settings_defaults(self):
        """Default settings for the plugin"""
        return dict(
            lights_on=False,  # lights currently off
            current_colour="#ffffff",  # current - white
            mote_type=mote_type,
            manual_colour="#ffffff",  # manual colour - white
            on_events=True,  # change colour on events
            on_event_startup=True,  # change colour on startup event
            startup_colour="#3030ff",  # startup - blue
            on_event_error=True,  # change colour on error event
            error_colour="#ff0000",  # error - red
            on_event_printing=True,  # change colour on printing event
            printing_colour="#ffffff",  # printing - white
            on_event_connect=True,  # change colour on connect event
            connect_colour="#30ff30",  # connect - green
            on_event_done=True,  # change colour on done event
            done_colour="#ff30ff",  # completed - pink
            on_event_upload=True,  # change colour on upload event
            upload_colour="#ffff00",  # upload - yellow
            on_event_disconnect=False,  # change colour on disconnect event
            disconnect_colour="#000000",  # disconnect - black/off
        )

    # -----------------------------------------------------------------------
    def get_settings_version(self):
        return 2

    # -----------------------------------------------------------------------
    def on_settings_migrate(self, target, current=None):
        if current is None or current < 1:
            # Reset settings to defaults.
            self._logger.debug("Resetting all Mote settings.")
            for (item, value) in self.get_settings_defaults().items():
                self._settings.set([item], value)
        if current == 1:
            for item in ("startup", "error", "printing", "connect", "done", "upload"):
                self._settings.set([item], True)
            self._settings.set(["disconnect"], False)

    # -----------------------------------------------------------------------
    def on_settings_save(self, data):
        manual_colour = self._settings.get(["manual_colour"])
        if manual_colour == "#000000":
            # setting manual colour to black confuses me...
            self._logger.info("Resetting manual colour to non-black")
            self._settings.set(["manual_colour"], "#ffffff")
        octoprint.plugin.SettingsPlugin.on_settings_save(self, data)

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
                "displayName": "Mote Lighting Control Plugin",
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
__plugin_name__ = "Mote Lighting Control"
__plugin_pythoncompat__ = ">=3,<4"  # only python 3


def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = MoteLightingControlPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information,
    }
