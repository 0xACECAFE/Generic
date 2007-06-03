#!/usr/bin/env python
""" This stuff is under GPL, as always"""

class ColorTerm:
    def __init__(self, Mono = False):
        pass

    def __get_tput_color_value__(colorcode):
        from commands import getoutput
        return getoutput('tput setaf ' + colorcode)

    BLACK_FG =  __get_tput_color_value__('0')
    RED_FG =            __get_tput_color_value__('1')
    GREEN_FG =  __get_tput_color_value__('2')
    YELLOW_FG =         __get_tput_color_value__('3')
    BLUE_FG =           __get_tput_color_value__('4')
    MAGENTA_FG =        __get_tput_color_value__('5')
    CYAN_FG =           __get_tput_color_value__('6')
    WHITE_FG =  __get_tput_color_value__('7')

    def black(self, msg):
        return self.BLACK_FG + msg + self.BLACK_FG

    def red(self, msg):
        return self.RED_FG + msg + self.BLACK_FG

    def green(self, msg):
        return self.GREEN_FG + msg + self.BLACK_FG

    def yellow(self, msg):
        return self.YELLOW_FG + msg + self.BLACK_FG

    def blue(self, msg):
        return self.BLUE_FG + msg + self.BLACK_FG

    def magenta(self, msg):
        return self.MAGENTA_FG + msg + self.BLACK_FG

    def cyan(self, msg):
        return self.CYAN_FG + msg + self.BLACK_FG

    def white(self, msg):
        return self.WHITE_FG + msg + self.BLACK_FG


