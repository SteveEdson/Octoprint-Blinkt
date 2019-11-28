# coding=utf-8
from __future__ import absolute_import, division

from blinkt import set_pixel, set_brightness, show, clear, set_all
import colorlover as cl


import octoprint.plugin


class BlinktPlugin(octoprint.plugin.ProgressPlugin, octoprint.plugin.EventHandlerPlugin):
    def on_event(self, event, payload):

        self._logger.info("Received event " + event)

        if event == "CaptureStart":
            clear()
            set_all(255, 255, 255, 1.0)
            show()

        if event == "CaptureDone":
            clear()
            # Restore the progress
            self._set_progress(self._blinkt_progress)
            show()

        if event == "PrintDone":
            clear()
            show()

    def on_print_progress(self, storage, path, progress):

        self._logger.info("Got progress")
        self._logger.info("On progress " + str(progress))
        self._blinkt_progress = progress
        self._set_progress(progress)

    def _set_progress(self, progress):
        clear()

        colors = cl.to_numeric( cl.scales['100']['div']['RdYlGn'] )

        ledNum = int(round((progress / 100) * 7))

        self._blinkt_r = int(colors[ledNum][0])
        self._blinkt_g = int(colors[ledNum][1])
        self._blinkt_b = int(colors[ledNum][2])

        for i in range(0, ledNum):
            self._logger.info("Setting " + str(i) + " to " + str(self._blinkt_r) + "," + str(self._blinkt_g) + "," + str(self._blinkt_b))
            set_pixel(i, self._blinkt_r, self._blinkt_g, self._blinkt_b)

        show()

__plugin_name__ = "Blinkt Progress"
__plugin_version__ = "1.0.0"
__plugin_description__ = "Show the print progress on a Pimoroni Blinkt"
__plugin_implementation__ = BlinktPlugin()
