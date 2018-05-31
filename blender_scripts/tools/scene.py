import imp
import constants
imp.reload(constants)
from constants import *

class Scene(object):
    def __init__(self):
        try:
            total_duration = 0
            for sub, attrs in self.subscenes.items():
                total_duration += attrs['duration']

            self.duration = total_duration
        except:
            raise Warning('Must define self.subscenes in subclass of Scene')

        self.set_subscene_timing()

    def set_subscene_timing(self):
        start = 0
        for sub, attrs in self.subscenes.items():
            attrs['start'] = start
            attrs['end'] = start + attrs['duration']
            start = attrs['end']

    def play(self):
        pass
        #To be extended by subclass
