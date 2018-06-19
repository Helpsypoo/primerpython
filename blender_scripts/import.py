#This script is a place for me to run random code with the script runner addon
#https://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/Import-Export/Script_Runner

import sys
sys.path.append('C:\\Users\\justi\\Documents\\CodeProjects\\Primer\\blender_scripts')
sys.path.append('C:\\Users\\justi\\Documents\\CodeProjects\\Primer\\blender_scripts\\tools')

import imp

import helpers
imp.reload(helpers)
from helpers import *
from constants import *
import tex_bobject
imp.reload(tex_bobject)
import gesture
imp.reload(gesture)
import svg_bobject
imp.reload(svg_bobject)

#reddit = import_object('logo')

#initialize_blender

bracket = gesture.Gesture(
    gesture_series = [
        {
            'type': 'arrow',
            'points': {
                'tail': (0, -2, 0),
                'head': (2, 0, 0)
            }
        }
    ]
)
bracket.add_to_blender(appear_frame = 0)

reddit = import_object(
    'reddit', 'svgblend',
    scale = 1,
    location = (0, 0, 0)
)

#define_materials()

#yt = tex_bobject.TexBobject(
#    '\\xcancel{B} + N \\times R = N \\times D'
#)
#yt.add_to_blender(appear_frame = 0)
