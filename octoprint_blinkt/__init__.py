# coding=utf-8
from __future__ import absolute_import, division

from blinkt import set_pixel, set_brightness, show, clear, set_all
import colorlover as cl


import octoprint.plugin


class BlinktPlugin(octoprint.plugin.ProgressPlugin, octoprint.plugin.EventHandlerPlugin):
    def on_event(self, event, payload):

        self._logger.info("Received event " + event)

        clear()
        set_all(255, 255, 255, 1.0)
        show()

        if event == "CaptureStart":
            clear()
            set_all(255, 255, 255, 1.0)
            show()

        if event == "CaptureDone":
            clear()
            show()

    def on_print_progress(self, storage, path, progress):

        self._logger.info("Got progress")
        self._logger.info("On progress " + str(progress))
        clear()

        colors = cl.to_numeric( cl.scales['8']['div']['RdYlGn'] )

        ledNum = int(round((progress / 100) * 7))

        r = colors[ledNum][0]
        g = colors[ledNum][1]
        b = colors[ledNum][2]

        for i in range(0, ledNum):
            set_pixel(i, r, g, b)

        show()

__plugin_name__ = "Blinkt Progress"
__plugin_version__ = "1.0.0"
__plugin_description__ = "Show the print progress on a Pimoroni Blinkt"
__plugin_implementation__ = BlinktPlugin()
