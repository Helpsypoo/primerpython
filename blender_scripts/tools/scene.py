import imp
import constants
imp.reload(constants)
from constants import *

class Scene(object):
    def __init__(self):
        self.duration = DEFAULT_SCENE_DURATION

    def play_from_frame(self, frame):
        self.scene_begin = frame
        pass
        #To be extended by subclass
