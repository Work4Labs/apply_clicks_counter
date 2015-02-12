# -*- coding: utf-8 -*-
import logging
import os
from Queue import Empty
from subprocess import Popen
from time import sleep

from stoppable_thread import StoppableThread

PYTHON_ROOT = os.path.dirname(os.path.realpath(__file__))
COMMAND = "%s/display_text.app" % PYTHON_ROOT
TIME_TO_DISPLAY = 60


class DisplayThread(StoppableThread):
    """
    This thread is in charge of launching the C++ program
    stored in COMMAND during TIME_TO_DISPLAY seconds (60 by default).
    One thread for one display action so we pass the queue on initialisation
    and we wait (block=True) for a value to be pushed in that queue.
    If no value is available for more than 120 seconds then we timeout
    to not get stucked. Empty exception is caught and we safelly stop.
    """

    name = "DisplayThread"

    def __init__(self, queue, seconds=TIME_TO_DISPLAY):
        super(DisplayThread, self).__init__()
        self.prg = None
        self.seconds = seconds
        try:
            value = queue.get(block=True, timeout=120)
        except Empty:
            self.stop()
        self.command = [COMMAND, "-s", seconds, "-t", self.center(value)]

    def run(self):
        if not self.stopped():
            logging.info("Display On")
            logging.info(self.command)
            sleep(self.seconds)
            # self.prg = Popen(self.command, shell=False)
            logging.info("Display Off")

    @staticmethod
    def center(val, max_chars=13):
        """
        Currently the screen can only display 13 characters
        thus we cut the value and we center it to make things
        beautiful.
        """
        val = val[:max_chars]
        length = len(val)
        spaces = (max_chars-length)/2
        return " "*spaces + val
