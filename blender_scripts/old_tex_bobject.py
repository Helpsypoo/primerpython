import bpy
import mathutils

import collections
import sys
import os
import imp

import svg_bobject
imp.reload(svg_bobject)
from svg_bobject import *

import constants
imp.reload(constants)
from constants import *

import helpers
imp.reload(helpers)
from helpers import *

class TexBobject(SVGBobject):
    def __init__(self, *expressions, **kwargs):
        super().__init__(**kwargs)
        #list of expressions. Could be a small list used for a few keyframes
        #or could be a list with one expression per frame, for sim-dependent
        #text
        #Scale to be manipulated during animations
        self.size = self.get_from_kwargs('size', 1)
        #Text size in blender units used when adding svgs
        self.centered = self.get_from_kwargs('centered', False)

        #This seems complicated, but TexBobjects can contain multiple expressions
        #in case they are updated during animation.
        #Each expression needs a set of curves because of how blender works.
        #So self.expressions is a list of dictionaries, one dictionary for each
        #expression, and each dictionary contains a string, which is the
        #expression, and a list, which will contain the blender curve objects
        self.expressions = []
        if len(expressions) > 0:
            self.add_expression(*expressions)

        self.lazy_morph = self.get_from_kwargs('lazy_morph', True)
        self.min_length = self.get_from_kwargs('min_length', 1)

        #This stuff is for avoiding having to add points to a bunch of extra
        #curves. It doesn't seem to do much in terms of speed, actually.
        data = bpy.data.curves.new(name = 'reuseable_curve_data', type = 'CURVE')
        self.reusable_empty_curve = bpy.data.objects.new(name = 'reuseable_curve', object_data = data)
        self.reusable_curves = []

    def add_expression(self, *expressions):
        #Each expression consists of a set of curves inside blender
        #So self.expressions is a list of dictionaries, one dictionary for each
        #expression. Each dictionary contains a 'string', which is the
        #expression's TeX string, and a 'curves' list, which will contain
        #the blender curve objects for that expression. The actual blender
        #curves are added in the add_to_blender method
        for expr in expressions:
            expression_curves_dict = {
                'string' : expr,
                'curves' : [],
                'length' : None,
                'center' : None
            }
            self.expressions.append(expression_curves_dict)
        if self.name == None:
            self.name = self.expressions[0]['string']

        self.active_expression_index = 0
        self.lookup_table = []

    def to_svg_by_index(self, index = 0):
        if self.expressions[index]['string'] == '':
            raise Warning("Cannot create svg of empty expression")
        else:
            return tex_to_svg_file(
                        self.expressions[index]['string'],
                        TEMPLATE_TEX_FILE
                        )

    def to_svg_by_expression(self, expression):
        if expression['string'] == '':
            raise Warning("Cannot create svg of empty expression")
        else:
            return tex_to_svg_file(
                        expression['string'],
                        TEMPLATE_TEX_FILE
                        )

    def move_to(self, **kwargs):
        super().move_to(**kwargs)

        self.calc_centers_and_lengths()

        #Possible todo: This makes it so start_frame and end_frame are needed,
        #instead of going with a default value. The start and end frames are
        #the main things to specify, so maybe this is fine.
        if isinstance(self.superbobject, tex_complex.TexComplex):
            self.superbobject.arrange_tex_bobjects(
                start_frame = kwargs['start_frame'],
                end_frame = kwargs['end_frame']
            )

    def add_to_blender(
        self,
        color = 'color5', #2 is the slot for text colors that contrast with bg
        appear_frame = 0,
        animate = False,
        center = False
    ):
        super().add_to_blender(
            appear_frame = appear_frame,
            animate = animate
        )
        #self.reusable_empty_curve.add_to_blender(appear_frame = appear_frame)
        bpy.context.scene.objects.link(self.reusable_empty_curve)

        for expression in self.expressions:
            #Import svg and get list of new curves in Blender
            previous_curves = [obj for obj in bpy.data.objects if obj.type == 'CURVE']
            imported_strings = {} #Keep track of previously imported strings
                                  #To avoid importing the same number many times
                                  #for one counter that fluctuates.
            if expression['string'] != '':
                if expression['string'] not in imported_strings.keys():
                    path = self.to_svg_by_expression(expression)
                    bpy.ops.import_curve.svg(filepath = path)
                    new_curves = [obj for obj in bpy.data.objects if obj.type == 'CURVE' and \
                                                                    obj not in previous_curves]

                    #Add new curves to tex_object's curve list
                    curves = expression['curves']
                    for curve in new_curves:
                        curves.append(curve)

                    #Arrange new curves relative to tex object's ref_obj
                    LOCAL_SCALE_UP = 260 #Value that makes line height about 1 Blender Unit
                    scale_up = LOCAL_SCALE_UP * self.size

                    for i, curve in enumerate(curves):
                        apply_material(curve, color)

                        for spline in curve.data.splines:
                            for point in spline.bezier_points:
                                point.handle_left_type = 'FREE'
                                point.handle_right_type = 'FREE'

                        #This needs to be in a separate loop because moving points before
                        #they're all 'Free' type makes the shape warp.
                        #It makes a cool "disappear in the wind" visual, though.
                        for spline in curve.data.splines:
                            for point in spline.bezier_points:
                                for i in range(len(point.co)):
                                    point.co[i] *= scale_up
                                    point.handle_left[i] *= scale_up
                                    point.handle_right[i] *= scale_up

                        if curve == curves[0]:
                            origin_to_lower_right(curve)
                        else:
                            bpy.ops.object.select_all(action='DESELECT')
                            curve.select = True
                            bpy.ops.object.origin_set(type = "ORIGIN_GEOMETRY")
                            curve.select = False

                    #Now that points/origins have been given initial positions for each char,
                    #define parent relationship to reference H character.
                    for i, curve in enumerate(curves):
                        if curve == curves[0]:
                            pass
                        else:
                            curve.parent = curves[0]
                            curve.matrix_parent_inverse = curve.parent.matrix_world.inverted()
                    #parent H character to ref_obj of the relevant tex object
                    curves[0].parent = self.ref_obj
                    curves[0].location = (0, 0, 0)

                    imported_strings[expression['string']] = curves
                else:
                    curves = expression['curves']
                    for curve in imported_strings[expression['string']]:
                        dup = curve.copy()
                        dup.data = curve.data.copy()
                        curves.append(dup)
                        bpy.context.scene.objects.link(dup)

                        #Fix parenting relationships for duplicated objects
                        #But apparently, that doesn't need to happen.
                        for i, curve in enumerate(curves):
                            if curve == curves[0]:
                                pass
                            else:
                                pass
                                #curve.parent = curves[0]
                                #curve.matrix_parent_inverse = curve.parent.matrix_local.inverted()
                        #parent H character to ref_obj of the relevant tex object
                        curves[0].parent = self.ref_obj
                        curves[0].location = (0, 0, 0)

                #Make imported curve objects into bobjects and unlink them so
                #they'll be added as part of add_to_blender()
                for i in range(1, len(expression['curves'])):
                    curve = expression['curves'][i]
                    curve_bobj = bobject.Bobject()
                    curve_bobj.ref_obj.matrix_local = deepcopy(curve.matrix_local)
                    curve_bobj.ref_obj.parent = expression['curves'][0]
                    curve.parent = curve_bobj.ref_obj
                    curve.location = [0, 0, 0]
                    #curve.matrix_parent_inverse = curve.parent.matrix_world.inverted()
                    curve_bobj.objects.append(curve)
                    self.subbobjects.append(curve_bobj)
                    curve_bobj.superbobject = self
                    #if expression == self.expressions[0]:
                    bpy.context.scene.objects.unlink(curve)
                    curve_bobj.add_to_blender(appear_frame = appear_frame, animate = False)
                    if expression != self.expressions[0]:
                        curve_bobj.disappear(disappear_frame = appear_frame, animate = False)
                    expression['curves'][i] = curve_bobj

        #Add chars, splines, and points to prep for morphing
        #but mostly to help alignment.
        if RENDER_QUALITY == 'medium' or RENDER_QUALITY == 'high':
            execute_and_time(
                'Make chains',
                self.make_morph_chains()
            )
            self.make_lookup_table()
            execute_and_time(
                'Prep chains',
                self.prep_chars_in_chains(
                    color = color, #2 is the slot for text colors that contrast with bg
                    appear_frame = appear_frame,
                    animate = animate,
                    center = center
                )
            )

        #Updates matrix_world, maybe other things.
        #Needed if we want to do calculations with object positions, which we do
        self.calc_centers_and_lengths()
        if self.centered == True:
            self.align_to_center()
        bpy.context.scene.update()
        self.hide_invisible_chars()

    def reduce_chars(self):
        pass

    def prep_chars_in_chains(self,
        color = 'color5', #2 is the slot for text colors that contrast with bg
        appear_frame = 0,
        animate = False,
        center = False
    ):
        for i, chain in enumerate(self.char_morph_chains):
            print('Preparing chars in chain ' + str(i + 1) + ' of ' + str(len(self.char_morph_chains)))
            max_spline_count = 0
            for link in chain:
                if len(link.objects[0].data.splines) > max_spline_count:
                    max_spline_count = len(link.objects[0].data.splines)

            #TODO: Make this part faster, possibly by transferring object
            #data directly for curves that are the same. The key is to cut
            #down on the number of times bpy.ops.curve.subdivide() is called.
            for link in chain:
                reused = False
                for reusable in self.reusable_curves:
                    if are_chars_same(link.objects[0], reusable[0]):
                        #super = link.superbobject

                        link.objects[0] = reusable[1].copy()
                        link.objects[0].data = reusable[1].data.copy()
                        link.objects[0].location = (0, 0, 0)
                        bpy.context.scene.objects.link(link.objects[0])

                        '''bobj = bobject.Bobject(
                            objects = [link.objects[0]],
                            name = 'reusable',
                            #location = (1000, 0, 0)
                        )'''
                        #self.add_subbobject(bobj)
                        #link.add_to_blender(appear_frame = appear_frame)
                        reused = True
                        break
                if reused == False:
                    unprepped = link.objects[0].copy()
                    unprepped.data = link.objects[0].data.copy()
                    equalize_spline_count(link.objects[0], max_spline_count)
                    add_points_to_curve_splines(link.objects[0], CONTROL_POINTS_PER_SPLINE)
                    prepped = link.objects[0].copy()
                    prepped.data = link.objects[0].data.copy()
                    self.reusable_curves.append([unprepped, prepped])
                    '''bobj = bobject.Bobject(
                        objects = [unprepped, prepped],
                        name = 'reusable',
                        location = (1000, 0, 0)
                    )
                    self.add_subbobject(bobj)
                    bobj.add_to_blender(appear_frame = appear_frame)'''

    def calc_centers_and_lengths(self):
        for expr in self.expressions:
            right_most_x = -math.inf
            #ref_H = expr['curves'][0]
            curves = expr['curves'][1:]
            for char in curves:
                #char is a bobject, so reassign to the contained curve
                char = char.objects[0]
                for spline in char.data.splines:
                    for point in spline.bezier_points:
                        candidate = char.matrix_local.translation[0] + \
                            char.parent.matrix_local.translation[0] + \
                            point.co[0] * char.scale[0]
                        if right_most_x < candidate:
                            right_most_x = candidate

            left_most_x = math.inf
            for char in curves:
                char = char.objects[0]
                for spline in char.data.splines:
                    for point in spline.bezier_points:
                        candidate = char.matrix_local.translation[0] + \
                            char.parent.matrix_local.translation[0] + \
                            point.co[0] * char.scale[0]
                        if left_most_x > candidate:
                            left_most_x = candidate

            length = right_most_x - left_most_x
            center = left_most_x + length / 2

            expr['length'] = length * self.scale[0]
            expr['center'] = center

    def align_to_center(self):
        for expr in self.expressions:
            expr['curves'][0].location[0] -= expr['center']
            #H.location[0] -= self.center

    def hide_invisible_chars(self):
        #Hide reference H at the beginning of the first expressions
        self.expressions[0]['curves'][0].hide = True
        self.expressions[0]['curves'][0].hide_render = True

        for i in range(1, len(self.expressions)): #don't hide first expression
            chars = self.expressions[i]['curves']
            #Each char is a blender curve object
            for char in chars:
                if RENDER_QUALITY != 'low': # or char == chars[0]
                    char.hide = True
                    char.hide_render = True
                if char == chars[0]:
                    hide_self_and_descendants(char)
                    #char.hide = True
                    #char.hide_render = True
                    #char.keyframe_insert(data_path="hide", frame = 0)
                    #char.keyframe_insert(data_path="hide_render", frame = 0)

    def morph_expression(
        self,
        final_index,
        start_frame = 0,
        duration = DEFAULT_MORPH_TIME
    ):
        end_frame = start_frame + DEFAULT_MORPH_TIME
        morph_pairs = []

        if RENDER_QUALITY == 'medium' or RENDER_QUALITY == "high":
            #As of writing this comment, the code in the if block below results
            #in weird artifacts in the tex_objects. But it's also much faster.
            #The artifacts are tolerable on 'medium' quality, so using this
            #block and a corresponding block in add_to_blender to speed up the
            #'medium' setting for counters (in drawn_world)
            if RENDER_QUALITY == 'medium' and self.lazy_morph == False:
                initial = self.expressions[0]['curves']
                final = self.expressions[final_index]['curves']
                #equalize_char_count(initial, final)
                for char1, char2 in list(zip(initial, final))[1:]:
                    morph_pairs.append([char1, char2])
            #The better way to do it.
            else:
                #if self.lazy_morph == True:
                for chain in self.char_morph_chains:
                    morph_pairs.append([chain[0], chain[final_index]])



            for char1, char2 in morph_pairs:
                char1 = char1.objects[0]
                char2 = char2.objects[0]
                morph_char(char1, char2)
                #Keyframes
                #Character location relative to parent
                #This ensures preservation of overall expression arrangement
                char1.parent.keyframe_insert(data_path = "location", frame = start_frame)
                char1.parent.matrix_local = char2.parent.matrix_local
                char1.parent.keyframe_insert(data_path = "location", frame = end_frame)

                #Shape keys
                eval_time = char1.data.shape_keys.key_blocks[-2].frame
                char1.data.shape_keys.eval_time = eval_time
                char1.data.shape_keys.keyframe_insert(
                    data_path = 'eval_time',
                    frame = start_frame
                )

                eval_time = char1.data.shape_keys.key_blocks[-1].frame
                char1.data.shape_keys.eval_time = eval_time
                char1.data.shape_keys.keyframe_insert(
                    data_path = 'eval_time',
                    frame = end_frame
                )
                char1.data.shape_keys.eval_time = 0

        #Low quality setting
        else:
            for expression in self.expressions:
                for i in range(1, len(expression['curves'])):
                    curve = expression['curves'][i].objects[0]
                    curve.keyframe_insert(data_path="hide", frame = start_frame - 1)
                    curve.keyframe_insert(data_path="hide_render", frame = start_frame - 1)
                    curve.hide = True
                    curve.hide_render = True
                    curve.keyframe_insert(data_path="hide", frame = start_frame)
                    curve.keyframe_insert(data_path="hide_render", frame = start_frame)
            final = self.expressions[final_index]['curves']
            for i in range(1, len(final)):
                curve = final[i].objects[0]
                curve.keyframe_insert(data_path="hide", frame = start_frame - 1)
                curve.keyframe_insert(data_path="hide_render", frame = start_frame - 1)
                curve.hide = False
                curve.hide_render = False
                curve.keyframe_insert(data_path="hide", frame = start_frame)
                curve.keyframe_insert(data_path="hide_render", frame = start_frame)
        if RENDER_QUALITY == 'high':
            print('Expression morphed')

        #Move the first expression, which is the one that morphs and is actually
        #shown, based on the change in center position
        if self.centered == True:
            ref = self.expressions[0]['curves'][0]
            prev_active_index = self.active_expression_index
            prev_center = self.expressions[prev_active_index]['center']
            new_center = self.expressions[final_index]['center']

            #expr['curves'][0].location[0] -= expr['center']
            ref.keyframe_insert(data_path="location", frame = start_frame)
            ref.location[0] += prev_center - new_center
            ref.keyframe_insert(data_path="location", frame = start_frame + duration)

        self.active_expression_index = final_index

        #This code messes up the counters, making the numbers all wobbly.
        #I don't fully get why, but it has something to do with the fact that
        #the counters morph over 3 frames rather than the standard 10.
        #For now, this just checks whether the superbobject TexComplex is a
        #counter, and then skips if so.
        if isinstance(self.superbobject, tex_complex.TexComplex) \
            and 'sim_counter' not in self.superbobject.name:
            self.superbobject.arrange_tex_bobjects(
                start_frame = start_frame,
                end_frame = start_frame + duration
            )

    def make_morph_chains(self):
        self.char_morph_chains = []
        for i in range(1, len(self.expressions)):
            print("Adding chars to morph chains for expression " + str(i) + " of " + str(len(self.expressions)))
            #print()
            #print('######################################################')
            #print('### Morph chains round  ' + str(i) + ' ####################')
            #print('######################################################')
            #print()
            initial = self.expressions[i - 1]['curves'][1:]
            final = self.expressions[i]['curves'][1:]

            if self.lazy_morph == True:
                destinations = self.find_lazy_morph_plan(initial, final)
            else:
                destinations = range(len(final))
            #For convenience, get inverse of destinations, caleed 'sources',
            #which is from the perspective of the 'final' expression.
            sources = []
            for j in range(len(final)):
                if j in destinations:
                    sources.append(destinations.index(j))
                else:
                    sources.append(None)

            #print('Destinations and sources before pairing:')
            #print(' Destinations', destinations)
            #print(' Sources', sources)
            #print()


            for j, (cur, dest) in enumerate(zip(initial, destinations)):
                if dest != None:
                    self.add_to_or_make_morph_chain(i, cur, final[dest])
                else:
                    k = j
                    #curves without a destination will look forward to try to
                    #pair with a curve that has no source, but won't jump past
                    #other curves with destinations.
                    while k < len(sources):
                        #Don't jump past a char with a destination
                        if k < len(destinations): #Doing this so the next line works
                            if destinations[k] != None: break
                        if sources[k] == None:
                            self.add_to_or_make_morph_chain(i, cur, final[k])
                            sources[k] = j
                            dest = destinations[j] = k
                            break
                        k += 1

            #print('Destinations and sources after dest -> source match:')
            #print(' Destinations', destinations)
            #print(' Sources', sources)
            #print()


            for j, (cur, src) in enumerate(zip(final, sources)):
                if src == None:
                    k = j
                    #curves without a destination will look forward to try to
                    #pair with a curve that has no source, but won't jump past
                    #other curves with destinations.
                    #max_index = min(len(destinations), len(sources))
                    while k < len(destinations):
                        #Don't jump past a char with a destination
                        if k < len(sources): #Doing this so the next line works
                            if sources[k] != None: break
                        if destinations[k] == None:
                            self.add_to_or_make_morph_chain(i, initial[k], cur)
                            sources[j] = k
                            dest = destinations[k] = j
                            break
                        k += 1
                bpy.context.scene.update()

            #print('Destinations and sources after source -> dest match:')
            #print(' Destinations', destinations)
            #print(' Sources', sources)
            #print()


            #If dest is still None after trying to pair it with a source,
            #just insert a zero-size curve for cur to morph to.
            #This section is pretty hacky
            for j, dest in enumerate(destinations):
                if dest == None:
                    cur = initial[j]
                    if j > 0:
                        k = j
                        while k >= len(final):
                            k -= 1
                        loc_cur = final[k - 1]
                    else:
                        try:
                            loc_cur = final[j + 1]
                        except:
                            loc_cur = final[j]
                    null_curve = new_null_curve(
                        parent = final[0].ref_obj.parent,
                        matrix_local = deepcopy(loc_cur.ref_obj.matrix_local),
                        reuse_object = self.reusable_empty_curve
                    )
                    self.add_to_or_make_morph_chain(i, cur, null_curve)
            #If sources[j] is still None after trying to pair final[j] with
            #a source, just insert a zero-size curve for final[j] to morph from.
            for j, src in enumerate(sources):
                if src == None:
                    cur = final[j]
                    if j > 0:
                        k = j
                        while k >= len(initial):
                            k -= 1
                        loc_cur = initial[k - 1]
                    else:
                        loc_cur = initial[j]

                    #Make the null curve if i == 1, because that means the curve
                    #to morph from is one that is actually rendered. Otherwise,
                    #reuse the reusable empty curve.
                    if i == 1:
                        reuse = None
                    else:
                        reuse = self.reusable_empty_curve
                    null_curve = new_null_curve(
                        parent = initial[0].ref_obj.parent,
                        matrix_local = deepcopy(loc_cur.ref_obj.matrix_local),
                        reuse_object = reuse
                    )
                    #self.expressions[0]['curves'].append(null_curve)
                    self.add_to_or_make_morph_chain(i, null_curve, cur)

            #Make sure all the chains are the same length. Relevant, e.g., if
            #a char in the first expression disappears in the second expression,
            #and a third expression exists. We need to extend the chain of
            #zero-size curves to keep later functions from tripping.
            for chain in self.char_morph_chains:
                while len(chain) < i + 1:
                    null_curve = new_null_curve(
                        parent = final[0].ref_obj.parent,
                        matrix_local = deepcopy(chain[-1].ref_obj.matrix_local),
                        reuse_object = self.reusable_empty_curve
                    )
                    self.add_to_or_make_morph_chain(i, chain[-1], null_curve)

            '''for chain in self.char_morph_chains:
                for link in chain:
                    if 'no_curve' in link.name:
                        for spline in link:
                            for point in spline:'''

            '''for chain in self.char_morph_chains:
                print(chain)'''

    def add_to_or_make_morph_chain(self, index, char1, char2):
        for chain in self.char_morph_chains:
            if char1 in chain:
                chain.append(char2)
                return
        #If that doesn't exit the function, we have a new chain
        new_chain = []
        for i in range(1, index): #Just a range with (index - 1) elements
            #If theres a new chain when index >1, a new curve is appearing
            null_curve = new_null_curve(
                parent = self.expressions[0]['curves'][0],
                matrix_local = deepcopy(char1.ref_obj.matrix_local),
                reuse_object = self.reusable_empty_curve
            )
            new_chain.append(null_curve)
        new_chain.append(char1)
        new_chain.append(char2)
        self.char_morph_chains.append(new_chain)

    def find_lazy_morph_plan(self, expr1, expr2, min_length = None):
        #max length of substring we bother keeping
        #Increments if shared is still too long
        if min_length == None:
            min_length = self.min_length #Default = 1

        max_shared = 10 #8! is 40320

        shared = get_shared_substrings(expr1, expr2)

        for i in range(len(shared)):
            if shared[-i][2] < min_length:
                shared[-i] = None
        shared = [sub for sub in shared if sub != None]

        while len(shared) > max_shared:
            min_length += 1
            removed = 0
            for i in range(len(shared)):
                if len(shared) - removed <= max_shared:
                    break
                if shared[-i][2] <= min_length:
                    shared[-i] = None
                    removed += 1

            shared = [sub for sub in shared if sub != None]
        #raise Warning("Shit's cray")
        combos = get_substring_combos(shared)

        best_option = [[0, 0, 0]]
        highest_total = 0
        for combo in combos:
            total = 0
            for substring in combo:
                total += substring[2] ** 2
            if total > highest_total:
                highest_total = total
                best_option = combo

        destinations = []
        for j in range(len(expr1)):
            destination = None
            for plan in best_option:
                if j in range(plan[0], plan[0] + plan[2]):
                    destination = j + plan[1] - plan[0]

            destinations.append(destination)

        #print(best_option)
        #print("Here's the plan:")
        #print(destinations)

        return destinations

    def make_lookup_table(self):
        #This function helps characters in non-intial expressions find the null
        #curve they need to morph from. The null curves at the beginning of
        #morph chains aren't in expr['curves'].
        self.lookup_table = []
        for expr in self.expressions:
            self.lookup_table.append([])
            for cur in expr['curves']:
                #Find the morph chain where cur appears and add the bobj at the
                #beginning of that chain to self.lookup_table[-1]. The bobjects
                #at the beginning of the morph chains are the ones that are
                #actually rendered.
                for chain in self.char_morph_chains:
                    if cur in chain:
                        self.lookup_table[-1].append(chain[0])
                        break

def new_null_curve(
    parent = None,
    matrix_local = None,
    color = 'color5',
    reuse_object = None
):
    #if reuse_object == None:
    data = bpy.data.curves.new(name = 'no_curve_data', type = 'CURVE')
    obj = bpy.data.objects.new(name = 'no_curve', object_data = data)
    #else:
    #    print('Reusing object!!!!!!')
    #    obj = reuse_object

    bobj = bobject.Bobject()
    obj.parent = bobj.ref_obj
    bobj.objects.append(obj)

    bobj.ref_obj.parent = parent
    bobj.ref_obj.matrix_local = matrix_local
    #bpy.context.scene.objects.link(new_null)
    if reuse_object == None:
        bobj.add_to_blender(animate = False)

    apply_material(obj, color)
    bpy.data.scenes[0].update()

    return bobj

def are_chars_same(char1, char2):
    splines1 = char1.data.splines
    splines2 = char2.data.splines

    for spline1, spline2 in zip(splines1, splines2):
        points1 = spline1.bezier_points
        points2 = spline2.bezier_points
        for point1, point2 in zip(points1, points2):
            for coord1, coord2 in zip(point1.co, point2.co):
                if round(coord1, 3) == round(coord2, 3):
                    #When the svg is imported, coords are stored to many decimal
                    #points. Even in characters we'd call equivalent, there is
                    #some fluctuation in the less significant digits, so
                    #rounding here yields the desired behavior.
                    pass
                else:
                    return False
    return True

def get_shared_substrings(expr1, expr2):
    #not actually strings, but a series of curves that represent letters, mostly
    curves1 = expr1
    curves2 = expr2

    shared = []
    for i in range(len(curves1)):
        j = 0
        for j in range(len(curves2)):
            length = 0
            length = get_match_length(length, i, j, curves1, curves2)

            if length > 0:
                candidate = [i, j, length]

                #Check whether candidate is redundant with a substring we
                #already found. E.g., without this, comparing '01' with '012'
                #would find the '01' and '1' substrings. We just want the longer
                #one.
                redundant = False
                '''
                #Actually, think we want redundancy, at least until speed becomes
                #an issue. Without redundancy, morphing '123' to '1223' would
                #result in the shared '3' being discarded, since it's redundant
                #with the shared '23'. This is usually good, but because the
                #original '2' is in two shared substrings, one (the '23') is
                #discarded. In this case, the '3' won't be captured, even though
                #it's not redundant with any substring that actually gets used.
                #The truly redundant substrings will get tossed later when
                #choosing the highest-scoring set to actually morph.
                #Only smaller redundant substrings toward the right of larger
                #substrings will be preserved. That's okay, because when
                #substrings overlap, the left-most overlapping string is used.
                #Since the left-most strings are never tossed, no redundancy is
                #needed for backup.
                '''
                '''
                Aaaaaaaactually, fuck redundancy. Things got slow.
                '''

                for substring in shared:
                    start1_diff = candidate[0] - substring[0]
                    start2_diff = candidate[1] - substring[1]
                    length_diff = candidate[2] - substring[2]
                    if start1_diff == start2_diff == -length_diff:
                        redundant = True


                if redundant == False:
                    shared.append(candidate)

    return(shared)

def get_match_length(length, char1_index, char2_index, curves1, curves2):
    if are_chars_same(curves1[char1_index].objects[0], curves2[char2_index].objects[0]):
        length += 1
        char1_index += 1
        char2_index += 1

        try:
            length = get_match_length(length, char1_index, char2_index, curves1, curves2)

            return length
        except:
            return length
    else:
        if length > 0:
            pass
        return length

def get_substring_combos(substrings):
    combos = []
    combo_in_progress = []
    combos = add_non_overlapping_substrings(combo_in_progress, combos, substrings)

    return combos

def add_non_overlapping_substrings(combo_in_progress, combos, substrings):
    if len(combo_in_progress) > 0:
        #Start checking substrings with the one after the last one added.
        starting_index = substrings.index(combo_in_progress[-1]) + 1
        #starting_index = 0
    else:
        starting_index = 0

    for i in range(starting_index, len(substrings)):
        #check if substring works
        candidate = substrings[i]
        no_overlap = True
        #check if substring overlaps with any substring alredy
        #in combo_in_progress. If so, don't add it to combos.
        for sub in combo_in_progress:
            #E.g., sub = [0, 0, 1] and candidate = [3, 0, 1] overlap
            no_overlap_in_1 = candidate[0] >= sub[0] + sub[2] or \
                              candidate[0] + candidate[2] <= sub[0]
            no_overlap_in_2 = candidate[1] >= sub[1] + sub[2] or \
                              candidate[1] + candidate[2] <= sub[1]

            no_overlap = (no_overlap_in_1 and no_overlap_in_2)

            if no_overlap == False:
                break

        if no_overlap == True:
            new_combo = deepcopy(combo_in_progress)
            new_combo.append(candidate)
            combos.append(new_combo)
            combos = add_non_overlapping_substrings(new_combo, combos, substrings)

    return combos

def tex_title(expression, template_tex_file):
    name = expression
    to_delete = ['/', '\\', '{', '}', ' ', ':', '~', '%', '\'', '\"']
    #Replace these rather than deleting them. These are characters that I've
    #wanted as lone expressions. (Which are also off limits in file names)
    to_replace = {
        '<' : 'lessthan',
        '>' : 'greaterthan',
        '?' : 'questionmark'
    }
    for char in name:
        if char in to_delete:
            name = name.replace(char, "")
    for char in name:
        if char in to_replace.keys():
            name = name.replace(char, to_replace[char])
    #name = str(name) + '_'

    return str(name)

def tex_to_svg_file(expression, template_tex_file):
    '''
    Commenting this out because it seems redundant with the checks for existence
    in the other functions called here.
    '''
    image_dir = os.path.join(
        TEX_DIR,
        tex_title(expression, template_tex_file)
    ) + ".svg"
    if os.path.exists(image_dir):
        return image_dir

    tex_file = generate_tex_file(expression, template_tex_file)
    dvi_file = tex_to_dvi(tex_file)
    return dvi_to_svg(dvi_file)

def generate_tex_file(expression, template_tex_file):
    result = os.path.join(
        TEX_DIR,
        tex_title(expression, template_tex_file)
    ) + ".tex"
    if not os.path.exists(result):
        print("Writing \"%s\" to %s"%(
            "".join(expression), result
        ))
        with open(template_tex_file, "r") as infile:
            body = infile.read()
            #I add an H to every expression to give a common reference point
            #for all expressions, then hide the H character. This is necessary
            #for consistent alignment of tex curves in blender, because
            #blender's import svg function sets the object's origin depending
            #on the expression itself, not according to a typesetting reference
            #frame.
            expression = '\\text{H} ' + expression
            body = body.replace(TEX_TEXT_TO_REPLACE, expression)
        with open(result, "w") as outfile:
            outfile.write(body)
    return result

def tex_to_dvi(tex_file):
    result = tex_file.replace(".tex", ".dvi")
    if not os.path.exists(result):
        commands = [
            "latex",
            "-interaction=batchmode",
            "-halt-on-error",
            "-output-directory=" + TEX_DIR,
            tex_file#,
            #">",
            #get_null()
        ]
        exit_code = os.system(" ".join(commands))
        if exit_code != 0:
            latex_output = ''
            log_file = tex_file.replace(".tex", ".log")
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    latex_output = f.read()
            raise Exception(
                "Latex error converting to dvi. "
                "See log output above or the log file: %s" % log_file)
    return result

def get_null():
    if os.name == "nt":
        return "NUL"
    return "/dev/null"

def dvi_to_svg(dvi_file):
    """
    Converts a dvi, which potentially has multiple slides, into a
    directory full of enumerated pngs corresponding with these slides.
    Returns a list of PIL Image objects for these images sorted as they
    where in the dvi
    """
    result = dvi_file.replace(".dvi", ".svg")
    if not os.path.exists(result):
        commands = [
            "dvisvgm",
            dvi_file,
            "-n",
            "-v",
            "3",
            "-o",
            result
            #Not sure what these are for, and it seems to work without them
            #so commenting out for now
            #,
            #">",
            #get_null()
        ]
        os.system(" ".join(commands))
    return result

#For testing
def main():
    exprs = []
    for i in range(3):
        exprs.append('\\frac {' + str(i) + '}{3}')
    obj = TexBobject(*exprs)
    print(obj.expressions)

if __name__ == "__main__":
    main()
