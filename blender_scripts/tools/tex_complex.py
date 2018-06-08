import bpy
import mathutils

import inspect
import imp
from random import random
import math
import time
from copy import deepcopy

import constants
imp.reload(constants)
from constants import *

import helpers
imp.reload(helpers)
from helpers import *

import bobject
imp.reload(bobject)
from bobject import Bobject

import gesture
imp.reload(gesture)

import tex_bobject
imp.reload(tex_bobject)

class TexComplex(Bobject):
    """docstring for TexComplex."""
    def __init__(
        self,
        *subbobjects,
        centered = False,
        multiline = False,
        line_height = 1.2,
        **kwargs
    ):
        super().__init__(*subbobjects, **kwargs)
        self.centered = centered
        self.multiline = multiline
        self.line_height = line_height
        self.tex_bobjects = subbobjects
        self.annotations = []

    def add_to_blender(self, **kwargs):
        self.arrange_tex_bobjects()
        self.arrange_annotations()
        super().add_to_blender(**kwargs)

    def arrange_tex_bobjects(self, start_frame = None, end_frame = None, centered = None):
        t_bobjs = self.tex_bobjects

        #for t_bobj in t_bobjs:
        #    t_bobj.ref_obj.location[1] = 0

        if start_frame != None:
            bpy.context.scene.frame_set(start_frame)
            for t_bobj in t_bobjs:
                t_bobj.ref_obj.keyframe_insert(data_path = 'location', frame = start_frame)

        if end_frame != None:
            bpy.context.scene.frame_set(end_frame)

        next_align = 0
        if self.multiline == False:
            for i, t_bobj in enumerate(t_bobjs):
                #Align expression
                t_bobj_length = t_bobj.ref_obj.scale[0] * \
                        t_bobj.imported_svg_data[t_bobj.active_expression_path]['length']
                if t_bobj.centered == True:
                    t_bobj.ref_obj.location[0] = next_align + t_bobj_length / 2
                else:
                    t_bobj.ref_obj.location[0] = next_align
                expr_length = t_bobj_length
                next_align += expr_length + \
                             SPACE_BETWEEN_EXPRESSIONS * t_bobj.ref_obj.scale[0]

        else:
            num_newlines = len(t_bobjs) - 1
            vert_disp = num_newlines * self.line_height / 2
            for t_bobj in t_bobjs:
                t_bobj.ref_obj.location[1] = vert_disp
                vert_disp -= self.line_height
                if t_bobj.centered == True:
                    t_bobj.ref_obj.location[0] = 0

        if centered == None: centered = self.centered
        if centered == True and self.multiline == False:
            next_align -= SPACE_BETWEEN_EXPRESSIONS
            for t_bobj in t_bobjs:
                t_bobj.ref_obj.location[0] -= next_align / 2

        for t_bobj in t_bobjs:
            #If any annotations are targeting the current t_bobj, move them too
            for annotation in self.annotations:
                if annotation[1] == i:
                    annotation[0].ref_obj.location[0] = t_bobj.ref_obj.location[0]

        if end_frame != None:
            for t_bobj in t_bobjs:
                t_bobj.ref_obj.keyframe_insert(data_path = 'location', frame = end_frame)



    def add_annotation(
        self,
        targets = None,
        alignment = 'top',
        labels = None,
        angle = 0,
        length = 1.5
    ):
        #calc points from targets
        gesture_series = []
        tex_bobj = self.tex_bobjects[targets[0]]
        for target in targets[1]:
            path = tex_bobj.paths[target[0]]
            bobjs = []
            for i in range(target[1], target[2] + 1):
                bobjs.append(tex_bobj.imported_svg_data[path]['curves'][i])

            left_most = math.inf
            right_most = -math.inf
            y = 0
            for i, bobj in enumerate(bobjs):
                cur = bobj.objects[0]
                for spline in cur.data.splines:
                    for point in spline.bezier_points:
                        candidatex = cur.location[0] * cur.parent.scale[0] + \
                            cur.parent.location[0] * cur.parent.parent.scale[0] + \
                            point.co[0] * cur.scale[0]
                        if right_most < candidatex:
                            right_most = candidatex
                        if left_most > candidatex:
                            left_most = candidatex
                    for point in spline.bezier_points:
                        candidatey = cur.location[1] * cur.parent.scale[1] + \
                            cur.parent.location[1] * cur.parent.parent.scale[1] + \
                            point.co[1] * cur.scale[1]
                        if alignment == 'top':
                            if y < candidatey:
                                y = candidatey
                        elif alignment == 'bottom':
                            if y > candidatey:
                                y = candidatey

            if len(bobjs) > 1: #Bracket
                if alignment == 'top':
                    y += 0.2 * self.scale[1] * tex_bobj.scale[1]
                    annotation_point = ((right_most + left_most) / 2, y + length, 0)
                    left_point = (left_most, y, 0)
                    right_point = (right_most, y, 0)
                elif alignment == 'bottom':
                    y -= 0.2 * self.scale[1] * tex_bobj.scale[1]
                    annotation_point = ((right_most + left_most) / 2, y - length, 0)
                    left_point = [right_most, y, 0]
                    right_point = [left_most, y, 0]
                if i == 0:
                    label_anchor = list(annotation_point)
                gesture_series.append(
                    {
                        'type' : 'bracket',
                        'points' : {
                            'annotation_point' : annotation_point,
                            'left_point' : left_point,
                            'right_point' : right_point
                        }
                    }
                )

            else: #Arrow
                if alignment == 'top':
                    y += 0.4 * self.scale[1] * tex_bobj.scale[1]
                    head = ((right_most + left_most) / 2 + math.tan(angle) * 0.4,
                            y,
                            0)
                    tail = ((right_most + left_most) / 2 + math.tan(angle) * length,
                            y + length,
                            0)
                elif alignment == 'bottom':
                    y -= 0.4 * self.scale[1] * tex_bobj.scale[1]
                    head = ((right_most + left_most) / 2 - math.tan(angle) * 0.4,
                            y,
                            0)
                    tail = ((right_most + left_most) / 2 - math.tan(angle) * length,
                            y - length,
                            0)
                if i == 0:
                    label_anchor = list(tail)
                gesture_series.append(
                    {
                        'type' : 'arrow',
                        'points' : {
                            'head' : head,
                            'tail' : tail,
                        }
                    }
                )

        container = bobject.Bobject(name = 'annotation')

        gest = gesture.Gesture(gesture_series = gesture_series, color = 'color2')
        tex_bobj.annotations.append([container, targets[1], alignment])
        self.annotations.append([container, targets[0]])
        container.add_subbobject(gest)

        #Make TexComplex for the annotation_text
        t_bobj_count = 0
        for label in labels:
            t_bobj_count = max(len(label), t_bobj_count)
        for label in labels:
            while len(label) < t_bobj_count:
                label.append(None)
        t_bobjs = []
        for i in range(t_bobj_count):
            strings = []
            for label in labels:
                strings.append(label[i])
            t_bobj = tex_bobject.TexBobject(*strings, centered = True, color = 'color2')
            t_bobjs.append(t_bobj)

        scale = 0.67 #Smaller than text. Could do this in a more robust way
        line_height = 1.2 #Could make this a constant. It's already a default.
        dy = (1/2 + t_bobj_count) / 2 * line_height * scale
        if alignment == 'bottom':
            dy = -dy
        label_anchor[1] += dy

        label_text = TexComplex(
            *t_bobjs,
            multiline = True,
            centered = True,
            scale = 0.67,
            location = label_anchor
        )

        container.add_subbobject(label_text)
        self.add_subbobject(container)



    def arrange_annotations(self):
        pass
