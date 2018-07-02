import collections
import math

import imp
import scene
imp.reload(scene)
from scene import Scene

import svg_bobject
imp.reload(svg_bobject)
import tex_bobject
imp.reload(tex_bobject)
import creature
imp.reload(creature)
import drawn_world
imp.reload(drawn_world)
import population
imp.reload(population)
import gesture
imp.reload(gesture)
import graph_bobject
imp.reload(graph_bobject)
import tex_complex
imp.reload(tex_complex)

import helpers
imp.reload(helpers)
from helpers import *

"""Is there smoother way to organize scene structure and timing?
- Objects that are defined and persist from one scene to the next, eliminating
the need to copy parameters or positions from one scene to the next. This would
also make it easier to make shorter scenes, which would render faster, since
they have fewer objects on overage.
- This would mean bobjects are defined outside of the scene. The scene would just
manipulate them and add keyframes.

Object types and thoughts:
- svg/tex. Scripts might take a while to run if a long chain of morphs needs to
be prepared. Probably just eat this cost for now and maybe alter add_to_blender
later on to only use a subset of the figures/expressions if it seems worthwhile.
Hmm. Except initializing one of these objects does interact with blender.
For now...?
- Generic bobjects. Might need to keep track of position and other parameters
more carefully on the python side, since I can't depend on blender when using
this workflow.
- DrawnWorld. The sims can be saved, so this should be fine. I don't think I'll
ever want to split a sim over several scenes, though."""




#'''
class Extinction(Scene):
    def __init__(self):
        self.subscenes = collections.OrderedDict([
            ('graph', {'duration': 6}),
            ('ntgraph', {'duration': 19.5}),
        ])
        super().__init__()

    def play(self):
        super().play()
        cues = self.subscenes
        scene_end = self.duration

        def func(x):
            return 1 + 0.1 * x

        def func2(x):
            return 0.1 * x

        graph = graph_bobject.GraphBobject(
            func, func2,
            x_range = [0, 10],
            y_range = [-1, 2],
            tick_step = [5, 1],
            width = 10,
            height = 10,
            x_label = 'N',
            x_label_pos = 'end',
            y_label = '\\Delta',
            y_label_pos = 'end',
            location = (-7.5, -1, 0),
            centered = True,
            arrows = True,
        )


        graph.add_to_blender(appear_time = cues['graph']['start'] - 0.5)

        graph.morph_curve(1, start_time = cues['graph']['start'])




        #Prep for next scene
        #to_disappear = [equation, graph, sim2, graph2]
        #for thing in to_disappear:
        #    thing.disappear(disappear_time = cues['ntgraph']['end'])
#'''

def play_scenes():
    ext = Extinction()
    ext.play()
