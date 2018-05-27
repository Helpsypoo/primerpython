import imp
from copy import deepcopy

import bobject
imp.reload(bobject)
from bobject import *


class SVGBobject(Bobject):
    """docstring for ."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.file_name = self.get_from_kwargs('file_name', None)

    #Once I actually do stuff with svgs, implement these functions for
    #non-tex svgs and make tex_bobject extend to tex-specific things
    def add_to_blender(self, **kwargs):
        super().add_to_blender(**kwargs)

        '''
        Pretty hacky due to the fact that the TexBobject class was created
        before the SVGBobject class, despite inheritance going the other direction
        '''

        appear_frame = kwargs['appear_frame']
        try:
            name = self.file_name
            path = os.path.join(
                SVG_DIR,
                name
            ) + ".svg"
            #print(path)

            previous_curves = [obj for obj in bpy.data.objects if obj.type == 'CURVE']
            bpy.ops.import_curve.svg(filepath = path)
            new_curves = [obj for obj in bpy.data.objects if obj.type == 'CURVE' and \
                                                            obj not in previous_curves]
            print(new_curves)
            LOCAL_SCALE_UP = 260 #Value that makes line height about 1 Blender Unit
            scale_up = LOCAL_SCALE_UP #* self.size

            for i, curve in enumerate(new_curves):
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

                curve.select = True
                bpy.ops.object.origin_set(type = "ORIGIN_GEOMETRY")
                curve.select = False

                #for i, curve in enumerate(new_curves):
                #    curve.parent = self.ref_obj
                #    curve.matrix_parent_inverse = curve.parent.matrix_world.inverted()

            for curve in new_curves:
                #curve = expression['curves'][i]
                curve_bobj = bobject.Bobject()
                print('making bobject')
                curve_bobj.ref_obj.matrix_local = deepcopy(curve.matrix_local)
                curve_bobj.ref_obj.parent = self.ref_obj
                curve.parent = curve_bobj.ref_obj
                curve.location = [0, 0, 0]
                #curve.matrix_parent_inverse = curve.parent.matrix_world.inverted()
                curve_bobj.objects.append(curve)
                self.subbobjects.append(curve_bobj)
                curve_bobj.superbobject = self
                #if expression == self.expressions[0]:
                bpy.context.scene.objects.unlink(curve)
                curve_bobj.add_to_blender(appear_frame = appear_frame, animate = False)

        except:
            print('No SVG file')


    def hide_invisible_chars(self): pass
    def morph_expression(self): pass

'''
Spline manipulation functions

I wrote these functions thinking I couldn't copy blender data types.
It turns out you can copy blender data blocks using, e.g., obj.data.copy().
This could likely simplify some of the code below significantly.
'''

def reindex_to_top_point(spline):
    #Make it so the highest control point is at index 0
    #This eliminates net rotation of points around the curve as they transition
    #from the starting char to the target char
    #Rotation would be fine, but they actually just go in a straight line,
    #causing the curve to sometimes fold on itself
    points = spline.bezier_points
    #Find index of highest point in curve
    index_highest = 0
    for i in range(len(points)):
        if points[i].co[1] > points[index_highest].co[1]: #Compare y values
            index_highest = i
    #copy point data to lists
    positions = []
    left_handles = []
    right_handles = []
    for point in points:
        positions.append(deepcopy(point.co))
        left_handles.append(deepcopy(point.handle_left))
        right_handles.append(deepcopy(point.handle_right))
    #re-index copied lists
    for i in range(index_highest):
        positions.append(positions.pop(0))
        left_handles.append(left_handles.pop(0))
        right_handles.append(right_handles.pop(0))
        #Would just do this:
        #   points.append(points.pop(0))
        #but points has type bpy_prop_collection, which is doesn't have
        #list methods and is immutable
    #assign values to blender bezier points
    for i in range(len(points)):
        points[i].co = positions[i]
        points[i].handle_left = left_handles[i]
        points[i].handle_right = right_handles[i]

def add_points_to_curve_splines(curve, total_points = CONTROL_POINTS_PER_SPLINE):
    #if len(curve.data.splines[0].bezier_points) < total_points:
    was_hidden = False
    if curve.hide:
        was_hidden = True
    curve.hide = False
    bpy.context.scene.objects.active = curve
    bpy.ops.object.mode_set(mode = 'EDIT')
    #Use subdivides to make control points that don't affect shape
    for spline in curve.data.splines:
        points = spline.bezier_points
        while len(spline.bezier_points) < total_points:
            #find longest segment to subdivide, ignores curvature
            longest = 0
            start_index = 0
            end_index = 1
            for j in range(len(points)):
                k = (j + 1) % len(points)
                sep = points[k].co - points[j].co
                if sep.length > longest:
                    start_index = j
                    end_index = k
                    longest = sep.length

            #subdivide longest segments
            points[start_index].select_control_point = True
            points[end_index].select_control_point = True
            #execute_and_time("Get ready to subdivide")
            #execute_and_time(
            #    "Subdivide",
            bpy.ops.curve.subdivide()
            #)
            for point in points:
                point.select_control_point = False

    bpy.ops.object.mode_set(mode = 'OBJECT')
    if was_hidden:
        curve.hide = True

def get_spline_length(spline):
    points = spline.bezier_points
    length = 0
    for j in range(len(points)):
        k = (j + 1) % len(points)
        sep = points[k].co - points[j].co
        length += sep.length
    return length

def get_spline_length_from_points(points):
    length = 0
    for j in range(len(points)):
        k = (j + 1) % len(points)
        sep = points[k].co - points[j].co
        length += sep.length
    return length

def get_list_of_spline_length_ranks(curve):
    splines = curve.data.splines
    curve_splines_ranked_by_length = []

    #get a list of splines and sort them by length
    #we have to do this because 'splines' is a bpy_prop_collection, not a list
    #meaning it doesn't have list methods.
    for spline in splines:
        curve_splines_ranked_by_length.append(spline)
    curve_splines_ranked_by_length.sort(key = lambda x: get_spline_length(x), \
                                                                reverse=True)

    list_of_length_ranks = []
    for spline in splines:
        rank = curve_splines_ranked_by_length.index(spline)
        list_of_length_ranks.append(rank)

    return list_of_length_ranks

#TODO: Stagger animation of splines to avoid overlap
#Order could be to shrink splines corresponding to holes in the char,
#then animate the transition of the outer edge, then grow the holes back
def add_morph_shape_keys(initial, final):
    if len(initial.data.splines) != len(final.data.splines):
        raise Warning(initial.name + " and " + final.name + \
            " do not have the same number of splines")

    was_hidden = False
    if initial.hide:
        was_hidden = True
    initial.hide = False
    bpy.context.scene.objects.active = initial
    bpy.ops.object.mode_set(mode = 'OBJECT')
    #If absolute shape keys exist, set eval_time to zero
    try:
        initial.data.shape_keys.eval_time = 0
    except:
        pass
    bpy.ops.object.shape_key_add(from_mix=False)
    initial.data.shape_keys.use_relative = False
    #For some reason, the default 'CARDINAL' interpolation setting caused
    #bouncing, which would occasionally enlarge splines that should have
    #been size zero, messing with the fill.
    initial.data.shape_keys.key_blocks[-1].interpolation = 'KEY_LINEAR'
    #bpy.ops.object.shape_key_retime()

    #If there's only one shape key, it's the basis shape key.
    if len(initial.data.shape_keys.key_blocks) == 1:
        #We should add another shape key, which will get a keyframe
        bpy.ops.object.shape_key_add(from_mix=False)
        initial.data.shape_keys.key_blocks[-1].interpolation = 'KEY_LINEAR'
        #initial.data.shape_keys.use_relative = False
        #bpy.ops.object.shape_key_retime()

    bpy.ops.object.mode_set(mode = 'EDIT')

    #This might be a bit confusing, caused by the fact that I was mixed up
    #length rank and index in my original names and implementation.
    #Could probably reimplement or at least change names.
    initial_spline_length_ranks = get_list_of_spline_length_ranks(initial)
    final_spline_length_ranks = get_list_of_spline_length_ranks(final)
    for i in range(len(initial.data.splines)):
        #Get the points of the ith spline
        initial_points = initial.data.splines[i].bezier_points

        #Okay, before we get the final points, we need to find the index of
        #the spline with the same length rank as the ith initial spline.

        #In the initial char, what is the length rank of the ith spline?
        initial_length_rank = initial_spline_length_ranks[i]
        #In the final char, what is the index of the corresponding length rank?
        final_index = final_spline_length_ranks.index(initial_length_rank)

        #Get the points of the final spline with the right length index
        final_points = final.data.splines[final_index].bezier_points

        #Double check that the splines have the same number of points
        if len(initial_points) != len(final_points):
            raise Warning(str(initial.name) + " and " + str(final.name) + \
            " do not have the same number of points in all splines")

        #Assign final_points values to initial_points
        for j in range(len(initial_points)):
            initial_points[j].co = final_points[j].co
            initial_points[j].handle_left = final_points[j].handle_left
            initial_points[j].handle_right = final_points[j].handle_right


    bpy.ops.object.mode_set(mode = 'OBJECT')
    if was_hidden:
        initial.hide = True

def equalize_spline_count(curve1, target):
    splines1 = curve1.data.splines

    if isinstance(target, int):
        spline_count = target
    else:
        splines2 = target.data.splines
        spline_count = max(len(splines1), len(splines2))

    while len(splines1) < spline_count:
        new_spline = splines1.new('BEZIER')
        new_spline.bezier_points.add(count = 2)
        new_spline.use_cyclic_u = True
    if not isinstance(target, int):
        while len(splines2) < spline_count:
            new_spline = splines2.new('BEZIER')
            new_spline.bezier_points.add(count = 2)
            new_spline.use_cyclic_u = True


def morph_char(initial, final):
    equalize_spline_count(initial, final)

    char_set = [initial, final]
    for char in char_set:
        for spline in char.data.splines:
            reindex_to_top_point(spline)
        add_points_to_curve_splines(char, CONTROL_POINTS_PER_SPLINE)
    add_morph_shape_keys(initial, final)

def equalize_char_count(expression1, expression2):
    #Each expression arg is a list of curve objects
    while len(expression1) < len(expression2):
        new_curve = bpy.data.curves.new(name = 'no_curve', type = 'CURVE')
        new_curve = \
            bpy.data.objects.new(name = 'no_curve', object_data = new_curve)
        bpy.context.scene.objects.link(new_curve)
        try:
            last_char = expression1[-1]
        except:
            #This should never happen, because all expressions have an H
            #prepended for alignment purposes
            try:
                last_char = expression2[0]
            except:
                raise Warning("Seems like both expressions are empty")

        new_curve.parent = last_char.parent
        new_curve.matrix_local = last_char.matrix_local
        bpy.data.scenes[0].update()

        new_curve.data.materials.append(last_char.active_material)
        expression1.append(new_curve)

    while len(expression2) < len(expression1):
        new_curve = bpy.data.curves.new(name = 'no_curve', type = 'CURVE')
        new_curve = \
            bpy.data.objects.new(name = 'no_curve', object_data = new_curve)
        bpy.context.scene.objects.link(new_curve)
        try:
            last_char = expression2[-1]
        except:
            #This should never happen, because all expressions have an H
            #prepended for alignment purposes
            try:
                last_char = expression1[0]
            except:
                raise Warning("Seems like both expressions are empty")

        new_curve.parent = last_char.parent
        new_curve.matrix_local = last_char.matrix_local
        bpy.data.scenes[0].update()

        new_curve.data.materials.append(last_char.active_material)
        expression2.append(new_curve)

def origin_to_lower_right(curve):
    #This function is plagued by some strange componding of scale inheritance
    #from parent to child object.

    lower_rightness = None
    low_rightest_point = None
    for spline in curve.data.splines:
        for point in spline.bezier_points:
            #Essentially a new coord in the lower-right direction, x - y
            l_rness = point.co[0] - point.co[1]
            if lower_rightness == None or lower_rightness < l_rness:
                lower_rightness = l_rness
                low_rightest_point = point

    vec = deepcopy(low_rightest_point.co)

    #Move points relative to origin
    for spline in curve.data.splines:
        for point in spline.bezier_points:
            point.co -= mathutils.Vector(vec)
            point.handle_left -= mathutils.Vector(vec)
            point.handle_right -= mathutils.Vector(vec)

    #Move origin so points are back where they started, with a new origin
    curve.location += mathutils.Vector(vec)
