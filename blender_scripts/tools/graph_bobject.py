import bpy

import imp
from copy import deepcopy
import math

import bobject
imp.reload(bobject)
from bobject import *

import tex_bobject
imp.reload(tex_bobject)

class GraphBobject(Bobject):
    """docstring for GraphBobject."""
    def __init__(self,
        *functions,
        x_range = 10,
        x_label = 'x',
        x_label_pos = 'along',
        y_range = 10,
        y_label = 'y',
        y_label_pos = 'along',
        y_label_rot = False,
        width = 10,
        height = 10,
        tick_step = 'auto',
        arrows = True,
        centered = False,
        **kwargs
    ):
        if 'name' not in kwargs:
            kwargs['name'] = 'graph'
        super().__init__(**kwargs)
        if isinstance(x_range, int) or isinstance(x_range, float):
            x_range = [0, x_range]
        self.x_range = x_range
        self.x_label = x_label
        self.x_label_pos = x_label_pos

        if isinstance(y_range, int) or isinstance(y_range, float):
            y_range = [0, y_range]
        self.y_range = y_range
        self.y_label = y_label
        self.y_label_pos = y_label_pos
        self.y_label_rot = y_label_rot

        self.width = width - 2 * GRAPH_PADDING
        self.height = height - 2 * GRAPH_PADDING
        self.tick_step = tick_step #Either 'auto' or a list

        #Calculate factor for converting from function space to draw space
        self.domain_scale_factor = self.width / (self.x_range[1] - self.x_range[0])
        self.range_scale_factor = self.height / (self.y_range[1] - self.y_range[0])

        self.arrows = arrows

        self.functions = functions
        self.active_function_index = 0
        self.functions_coords = []
        for i in range(len(self.functions)):
            self.functions_coords.append(self.func_to_coords(func_index = i))

        self.curve_highlight_points = []

        if centered == True:
            self.ref_obj.location[0] -= \
                (self.x_range[1] + self.x_range[0]) * self.domain_scale_factor / 2
            self.ref_obj.location[1] -= \
                (self.y_range[1] + self.y_range[0]) * self.range_scale_factor / 2

    def add_axes(self):
        #x axis
        cyl_bobj = import_object('one_side_cylinder', 'primitives')
        apply_material(cyl_bobj.objects[0], 'color2')
        self.add_subbobject(cyl_bobj)
        ref = cyl_bobj.ref_obj
        ref.location = (self.x_range[0] * self.domain_scale_factor - GRAPH_PADDING, 0, 0)
        ref.children[0].rotation_euler = (0, math.pi / 2, 0)
        ref.children[0].scale = (AXIS_DEPTH, AXIS_WIDTH, self.width / 2 + GRAPH_PADDING)

        if self.arrows == 'positive' or self.arrows == True:
            con_bobj = import_object('arrow_head', name = 'arrow_ref')
            apply_material(con_bobj.objects[0], 'color2')
            self.add_subbobject(con_bobj)
            ref = con_bobj.ref_obj
            #con.parent = self.ref_obj
            ref.location = (self.x_range[1] * self.domain_scale_factor + GRAPH_PADDING, 0, 0)
            ref.children[0].rotation_euler = (0, math.pi / 2, 0)
            ref.children[0].scale = ARROW_SCALE

            if self.arrows == True:
                con_bobj = import_object('arrow_head', name = 'arrow_ref')
                apply_material(con_bobj.objects[0], 'color2')
                self.add_subbobject(con_bobj)
                ref = con_bobj.ref_obj
                ref.location = (self.x_range[0] * self.domain_scale_factor - GRAPH_PADDING, 0, 0)
                ref.children[0].rotation_euler = (0, -math.pi / 2, 0)
                ref.children[0].scale = ARROW_SCALE

        #x axis label
        x_lab = tex_bobject.TexBobject(self.x_label, name = 'x_lab', centered = True)
        #x_lab_container = bobject.TexComplex(x_lab, centered = True, name = 'x_lab_container')
        if self.x_label_pos == 'along':
            x_lab.ref_obj.location = ((self.x_range[1] + self.x_range[0]) * self.domain_scale_factor / 2, -2, 0)
        elif self.x_label_pos == 'end':
            x_lab.ref_obj.location = (self.x_range[1] * self.domain_scale_factor + GRAPH_PADDING + 1.5, 0, 0)
            x_lab.centered = False
        self.add_subbobject(x_lab)

        #y axis
        cyl_bobj = import_object('one_side_cylinder', 'primitives')
        apply_material(cyl_bobj.objects[0], 'color2')
        #cyl_bobj.ref_obj.parent = self.ref_obj
        self.add_subbobject(cyl_bobj)
        ref = cyl_bobj.ref_obj
        ref.location = (0, self.y_range[0] * self.range_scale_factor - GRAPH_PADDING, 0)
        ref.children[0].rotation_euler = (-math.pi / 2, 0, 0)
        ref.children[0].scale = (AXIS_WIDTH, AXIS_DEPTH, self.height / 2 + GRAPH_PADDING)

        if self.arrows == 'positive' or self.arrows == True:
            con_bobj = import_object('arrow_head', name = 'arrow_ref')
            apply_material(con_bobj.objects[0], 'color2')
            self.add_subbobject(con_bobj)
            ref = con_bobj.ref_obj
            ref.location = (0, self.y_range[1] * self.range_scale_factor + GRAPH_PADDING, 0)
            ref.children[0].rotation_euler = (-math.pi / 2, 0, 0)
            ref.children[0].scale = ARROW_SCALE

            if self.arrows == True:
                con_bobj = import_object('arrow_head', name = 'arrow_ref')
                apply_material(con_bobj.objects[0], 'color2')
                self.add_subbobject(con_bobj)
                ref = con_bobj.ref_obj
                ref.location = (0, self.y_range[0] * self.range_scale_factor - GRAPH_PADDING, 0)
                ref.rotation_euler = (math.pi / 2, 0, 0)
                ref.children[0].scale = ARROW_SCALE

        #y axis label
        y_lab = tex_bobject.TexBobject(self.y_label, name = 'y_lab', centered = True)
        #y_lab_container = bobject.TexComplex(y_lab, centered = True, name = 'y_lab_container')
        if self.y_label_pos == 'along':
            y_lab.ref_obj.location = ( -2.5, (self.y_range[1] + self.y_range[0]) * self.range_scale_factor / 2, 0)
        elif self.y_label_pos == 'end':
            y_lab.ref_obj.location = (0, self.y_range[1] * self.range_scale_factor + GRAPH_PADDING + 1.5, 0)
        if self.y_label_rot == True:
            y_lab.ref_obj.rotation_euler = (0, 0, math.pi / 2)
        self.add_subbobject(y_lab)


        tick_step = self.tick_step
        if tick_step == 'auto':
            num_steps_x = self.width / AUTO_TICK_SPACING_TARGET
            x_tick_step = math.floor((self.x_range[1] - self.x_range[0]) / num_steps_x)

            num_steps_y = self.height / AUTO_TICK_SPACING_TARGET
            y_tick_step = math.floor((self.y_range[1] - self.y_range[0]) / num_steps_y)

        else:
            if isinstance(tick_step, list):
                x_tick_step = tick_step[0]
                y_tick_step = tick_step[1]
            elif isinstance(tick_step, int) or isinstance(tick_step, float):
                x_tick_step = y_tick_step = tick_step
            else:
                raise Warning('Idk wtf to do with that tick step.')

        #Positive x ticks
        current_tick = x_tick_step
        while current_tick <= self.x_range[1]:
            self.add_tick_x(current_tick)
            current_tick += x_tick_step

        #Negative x ticks
        current_tick = -x_tick_step
        while current_tick >= self.x_range[0]:
            self.add_tick_x(current_tick)
            current_tick -= x_tick_step

        #Positive y ticks
        current_tick = y_tick_step
        while current_tick <= self.y_range[1]:
            self.add_tick_y(current_tick)
            current_tick += y_tick_step

        #Negative y ticks
        current_tick = -y_tick_step
        while current_tick >= self.y_range[0]:
            self.add_tick_y(current_tick)
            current_tick -= y_tick_step

    def add_tick_x(self, value):
        cyl_bobj = import_object('cylinder', 'primitives', name = 'x_tick')
        apply_material(cyl_bobj.objects[0], 'color2')
        self.add_subbobject(cyl_bobj)
        ref = cyl_bobj.ref_obj
        ref.location = (value * self.domain_scale_factor, 0, 0)
        ref.children[0].rotation_euler = (math.pi / 2, 0, 0)
        ref.children[0].scale = (AXIS_WIDTH / 2, AXIS_DEPTH / 2, min(self.width, self.height) / 20)

        label = tex_bobject.TexBobject(
            str(value),
            location = (value * self.domain_scale_factor, - min(self.width, self.height) / 10, 0),
            centered = True,
            scale = 0.5
        )
        self.add_subbobject(label)

    def add_tick_y(self, value):
        cyl_bobj = import_object('cylinder', 'primitives', name = 'y_tick')
        apply_material(cyl_bobj.objects[0], 'color2')
        self.add_subbobject(cyl_bobj)
        ref = cyl_bobj.ref_obj
        ref.location = (0, value * self.range_scale_factor, 0)
        ref.children[0].rotation_euler = (0, math.pi / 2, 0)
        ref.children[0].scale = (AXIS_DEPTH / 2, AXIS_WIDTH / 2, min(self.width, self.height) / 20)

        label = tex_bobject.TexBobject(
            str(value),
            location = (- min(self.width, self.height) / 10, value * self.range_scale_factor, 0),
            centered = 'right',
            scale = 0.5
        )
        self.add_subbobject(label)

    def add_function_curve(self):
        #Makes a curve object with the 0th function

        data = bpy.data.curves.new(name = 'function_curve_data', type = 'CURVE')
        data.dimensions = '3D'
        data.resolution_u = 64
        data.render_resolution_u = 64
        data.splines.new('NURBS')

        coords = self.functions_coords[0]

        points = data.splines[0].points
        points.add(len(coords) - 1) #Spline starts with one point
        for i in range(len(coords)):
            x, y, z = coords[i]
            if i == 0: z = -CURVE_Z_OFFSET
            points[i].co = (x, y, z, 1)

        #Old Bezier stuff. Might delete if NURBS seems to be working out
        '''
        data.splines.new('BEZIER')
        points = data.splines[0].bezier_points

        for i in range(len(coords)):
            #Splines start with one point in them, and for some reason, there's
            #no straighforward way to delete them. (The blender-side data
            #structures aren't python lists). So check whether the number of
            #points is already right before adding one.
            coord = coords[i]
            if len(points) < i + 1:
                points.add()
            point = points[-1]
            point.co = coord
            point.handle_left_type = 'FREE'
            point.handle_right_type = 'FREE'

            #Most of this is probably unneeded for the number of points that are
            #going to be plotted in these graphs.

            #For non-endpoints, set local slope to secant line between adjacent
            #points. For endpoints, just put handles on top of main point
            if i - 1 >= 0 and i + 1 < len(coords):
                point_to_left = coords[i - 1]
                point_to_right = coords[i + 1]

                #if point is local max or min, set slope to zero to avoid
                #conspicuously wrong shape.
                if (point_to_left[1] >= coord[1] and point_to_right[1] >= coord[1]) or \
                    (point_to_right[1] <= coord[1] and point_to_left[1] <= coord[1]):
                    slope = 0
                else:
                    slope = (point_to_right[1] - point_to_left[1]) / \
                        (point_to_right[0] - point_to_left[0])

                nudge_x_left = (point_to_left[0] - coord[0]) / 2 #negative
                nudge_x_right = (point_to_right[0] - coord[0]) / 2

                point.handle_left = [
                    coord[0] + abs(nudge_x_left) * math.cos(math.atan2(nudge_x_left * slope, nudge_x_left)),
                    coord[1] + abs(nudge_x_left) * math.sin(math.atan2(nudge_x_left * slope, nudge_x_left)),
                    0
                ]

                point.handle_right = [
                    coord[0] + abs(nudge_x_right) * math.cos(math.atan2(nudge_x_right * slope, nudge_x_right)),
                    coord[1] + abs(nudge_x_right) * math.sin(math.atan2(nudge_x_right * slope, nudge_x_right)),
                    0
                ]
            else:
                point.handle_left = coord
                point.handle_right = coord'''


        cur = bpy.data.objects.new(name = 'function_curve', object_data = data)
        apply_material(cur, 'color3')

        bpy.ops.curve.primitive_bezier_circle_add()
        cross_section = bpy.context.object
        cross_section.scale = [CURVE_WIDTH, CURVE_WIDTH, 0]
        bpy.context.scene.objects.unlink(cross_section)


        cur.data.bevel_object = cross_section


        cur_bobj = bobject.Bobject(objects = [cur], name = 'function_curve_container')
        #cross_section.parent = cur_bobj.ref_obj
        self.add_subbobject(cur_bobj)
        self.function_curve = cur_bobj

    def animate_function_curve(self,
        start_frame = 0,
        end_frame = None,
        uniform_along_x = False
    ):
        if end_frame == None:
            raise Warning('Need end frame to animate function curve, ya dick.')

        data = self.function_curve.ref_obj.children[0].data

        #Insert start and end keyframes for bevel_factor_end
        data.bevel_factor_end = 0
        data.keyframe_insert(data_path = 'bevel_factor_end', frame = start_frame)
        data.bevel_factor_end = 1
        data.keyframe_insert(data_path = 'bevel_factor_end', frame = end_frame)

        if uniform_along_x == False:
            pass
        else:
            make_animations_linear(data)

    def evaluate_function(self, input = None, index = None):
        if input == None:
            raise Warning('Need input to evaluate function')
        if index == None:
            index = self.active_function_index

        func = self.functions[index]

        if isinstance(func, list):
            try:
                y = func[math.floor(input)]
            except:
                #We're graphing inclusive ranges, so flooring the very last
                #value doesn't get you in the domain.
                y = func[math.floor(input) - 1]
        else:
            y = func(input)

        return y

    def func_to_coords(self, func_index = 0):
        if len(self.functions) == 0:
            print("Graph bobject has no function defined, which might be cool, idk.")
            return
        else:
            points_per_drawn_x_unit = PLOTTED_POINT_DENSITY * self.scale[0]
            num_drawn_points = self.width * points_per_drawn_x_unit

            self.x_step = (self.x_range[1] - self.x_range[0]) / num_drawn_points
            x_step = self.x_step

            x = self.x_range[0]
            x_vals = []
            while x <= self.x_range[1]:
                x_vals.append(x)
                x += x_step

            coords = []
            for x in x_vals:
                y = self.evaluate_function(input = x, index = func_index)
                try:
                    y = self.evaluate_function(input = x, index = func_index)
                except:
                    #Graph draws point at end of the domain, but list functions
                    #don't include that last point
                    y = coords[-1][1] / self.range_scale_factor

                coords.append([
                    x * self.domain_scale_factor,
                    y * self.range_scale_factor,
                    CURVE_Z_OFFSET
                ])

            return coords

    def add_point_at_coord(self,
        appear_frame = 0,
        coord = [0, 0, 0],
        track_curve = False,
        axis_projections = False
    ):
        draw_space_coord = [
            coord[0] * self.domain_scale_factor,
            coord[1] * self.range_scale_factor,
            coord[2]
        ]
        point = import_object(
            'goodicosphere', 'primitives',
            location = draw_space_coord,
            scale = CURVE_WIDTH * 5
        )

        point.coord = coord
        point.track_curve = track_curve
        if point.track_curve == True:
            self.curve_highlight_points.append(point)
            #Correct the y value
            point.coord[1] = self.evaluate_function(input = point.coord[0])
            point.ref_obj.location[1] = point.coord[1] * self.range_scale_factor
        apply_material(point.ref_obj.children[0], 'color4')
        point.add_to_blender(appear_frame = appear_frame)
        self.add_subbobject(point)



        if axis_projections == True:
            x_tracker = import_object('one_side_cylinder', 'primitives', name = 'x_tracker')
            apply_material(x_tracker.objects[0], 'color2')
            ref = x_tracker.ref_obj
            point_ref = point.ref_obj
            ref.location = point_ref.location
            ref.children[0].rotation_euler = (math.pi / 2, 0, 0)
            ref.children[0].scale = (AXIS_DEPTH / 4, AXIS_DEPTH / 4, ref.location[1] / 2)

            y_tracker = import_object('one_side_cylinder', 'primitives', name = 'y_tracker')
            apply_material(y_tracker.objects[0], 'color2')
            ref = y_tracker.ref_obj
            point_ref = point.ref_obj
            ref.location = point_ref.location
            ref.children[0].rotation_euler = (0, - math.pi / 2, 0)
            ref.children[0].scale = (AXIS_DEPTH / 4, AXIS_DEPTH / 4, ref.location[0] / 2)

            x_tracker.add_to_blender(appear_frame = appear_frame)
            self.add_subbobject(x_tracker)
            y_tracker.add_to_blender(appear_frame = appear_frame)
            self.add_subbobject(y_tracker)
            point.axis_projections = [x_tracker, y_tracker]

        return point

    def animate_point(
        self,
        end_coord = None,
        start_frame = 0,
        end_frame = None,
        point = None,
        in_place = False
    ):
        if point == None:
            point = self.add_point_at_coord(
            appear_frame = start_frame - OBJECT_APPEARANCE_TIME,
            coord = [0, 0, 0]
        )
        if end_coord == None:
            end_coord = point.coord
        if end_frame == None:
            end_frame = start_frame + OBJECT_APPEARANCE_TIME
            #raise Warning('Need end frame to animate a point in the graph. ' + \
            #              'You are a terrible person.')

        if point.track_curve == False:
            point.ref_obj.keyframe_insert(
                data_path = 'location',
                frame = start_frame
            )
            point.coord = end_coord
            point.ref_obj.location = [
                point.coord[0] * self.domain_scale_factor,
                point.coord[1] * self.range_scale_factor,
                point.coord[2]
            ]
            point.ref_obj.keyframe_insert(
                data_path = 'location',
                frame = end_frame
            )
        else:
            if in_place == True:
                point.ref_obj.keyframe_insert(
                    data_path = 'location',
                    frame = start_frame
                )
                point.coord[1] = self.evaluate_function(input = point.coord[0])
                drawn_coord = [
                    point.coord[0] * self.domain_scale_factor,
                    point.coord[1] * self.range_scale_factor,
                    point.coord[2]
                ]
                point.ref_obj.location = drawn_coord
                point.ref_obj.keyframe_insert(
                    data_path = 'location',
                    frame = end_frame
                )

                if hasattr(point, 'axis_projections'):
                    x_tracker = point.axis_projections[0].ref_obj
                    x_tracker.keyframe_insert(
                        data_path = 'location',
                        frame = start_frame
                    )
                    x_tracker.location = drawn_coord
                    x_tracker.keyframe_insert(
                        data_path = 'location',
                        frame = end_frame
                    )
                    x_tracker.children[0].keyframe_insert(
                        data_path = 'scale',
                        frame = start_frame
                    )
                    x_tracker.children[0].scale[2] = drawn_coord[1] / 2
                    x_tracker.children[0].keyframe_insert(
                        data_path = 'scale',
                        frame = end_frame
                    )

                    y_tracker = point.axis_projections[1].ref_obj
                    y_tracker.keyframe_insert(
                        data_path = 'location',
                        frame = start_frame
                    )
                    y_tracker.location = drawn_coord
                    y_tracker.keyframe_insert(
                        data_path = 'location',
                        frame = end_frame
                    )
                    y_tracker.children[0].keyframe_insert(
                        data_path = 'scale',
                        frame = start_frame
                    )
                    y_tracker.children[0].scale[2] = drawn_coord[0] / 2
                    y_tracker.children[0].keyframe_insert(
                        data_path = 'scale',
                        frame = end_frame
                    )
            else:
                x_distance = end_coord[0] - point.coord[0]
                num_frames = end_frame - start_frame + 1
                x_step = x_distance / num_frames
                for i in range(num_frames + 1):
                    drawn_coord = [
                        point.coord[0] * self.domain_scale_factor,
                        point.coord[1] * self.range_scale_factor,
                        point.coord[2],
                    ]
                    point.ref_obj.location = drawn_coord
                    point.ref_obj.keyframe_insert(
                        data_path = 'location',
                        frame = start_frame + i
                    )

                    if hasattr(point, 'axis_projections'):
                        x_tracker = point.axis_projections[0].ref_obj
                        x_tracker.location = drawn_coord
                        x_tracker.keyframe_insert(
                            data_path = 'location',
                            frame = start_frame + i
                        )
                        x_tracker.children[0].scale[2] = drawn_coord[1] / 2
                        x_tracker.children[0].keyframe_insert(
                            data_path = 'scale',
                            frame = start_frame + i
                        )

                        y_tracker = point.axis_projections[1].ref_obj
                        y_tracker.location = drawn_coord
                        y_tracker.keyframe_insert(
                            data_path = 'location',
                            frame = start_frame + i
                        )
                        y_tracker.children[0].scale[2] = drawn_coord[0] / 2
                        y_tracker.children[0].keyframe_insert(
                            data_path = 'scale',
                            frame = start_frame + i
                        )

                    #Set up for next loop
                    #Skip on last time through. Could probably just construct
                    #the loop more thoughtfully. ¯\_(ツ)_/¯
                    if i < num_frames:
                        point.coord[0] += x_step
                        point.coord[1] = self.evaluate_function(input = point.coord[0])

    def multi_animate_point(
        self,
        point = None,
        start_frame = 0,
        x_of_t = None,
        full_coords = False
    ):
        #Handle defaults
        if point == None:
            raise Warning('Need point for multi_animate_point')

        #condense x_of_t to only contain points where x changes
        if isinstance(x_of_t[0], int):
            condensed_x_of_t = []
            current_x = -math.inf
            for t, x in enumerate(x_of_t):
                if x != current_x:
                    condensed_x_of_t.append([t, x])
                    current_x = x
            x_of_t = condensed_x_of_t

        for i, (t, x) in enumerate(x_of_t):
            try:
                update_time = min(HIGHLIGHT_POINT_UPDATE_TIME,
                                  x_of_t[i+1][0] - t)
            except: #Should only run for last element
                update_time = HIGHLIGHT_POINT_UPDATE_TIME

            end_frame = start_frame + t + update_time
            #Haven't tested this, but trying to making it so I can pass a list
            #of x values or a list of full coords as a denser way of animating
            #several movements of non-curve-constrained points.
            if full_coords == True:
                end_coord = x
            else:
                end_coord = [x, 0, 0]

            self.animate_point(
                point = point,
                start_frame = start_frame + t,
                end_frame = end_frame,
                end_coord = end_coord
            )




    def morph_curve(self, to_curve_index, start_frame = None, end_frame = None):
        if start_frame == None:
            if end_frame == None:
                raise Warning('Need start frame and/or end frame for move_to')
            else:
                start_frame = end_frame - OBJECT_APPEARANCE_TIME

        if end_frame == None:
            end_frame = start_frame + OBJECT_APPEARANCE_TIME

        self.active_function_index = to_curve_index

        curve_object = self.function_curve.ref_obj.children[0]
        bpy.context.scene.objects.active = curve_object
        #bpy.ops.object.mode_set(mode = 'OBJECT')
        #If absolute shape keys exist, set eval_time to zero
        try:
            curve_object.data.shape_keys.eval_time = 0
        except:
            pass
        bpy.ops.object.shape_key_add(from_mix=False)
        curve_object.data.shape_keys.use_relative = False
        #For some reason, the default 'CARDINAL' interpolation setting caused
        #bouncing, which would occasionally enlarge splines that should have
        #been size zero, messing with the fill.
        curve_object.data.shape_keys.key_blocks[-1].interpolation = 'KEY_LINEAR'

        #If there's only one shape key, it's the basis shape key.
        if len(curve_object.data.shape_keys.key_blocks) == 1:
            #We should add another shape key, which will get a keyframe
            bpy.ops.object.shape_key_add(from_mix=False)
            curve_object.data.shape_keys.key_blocks[-1].interpolation = 'KEY_LINEAR'

        final_coords = self.functions_coords[to_curve_index]

        bpy.ops.object.mode_set(mode = 'EDIT')
        for j in range(len(curve_object.data.splines[0].points)):
            x, y, z = final_coords[j]
            curve_object.data.splines[0].points[j].co = (x, y, z, 1)
        bpy.ops.object.mode_set(mode = 'OBJECT')


        #Animate through shape keys
        eval_time = curve_object.data.shape_keys.key_blocks[-2].frame
        curve_object.data.shape_keys.eval_time = eval_time
        curve_object.data.shape_keys.keyframe_insert(
            data_path = 'eval_time',
            frame = start_frame
        )

        eval_time = curve_object.data.shape_keys.key_blocks[-1].frame
        curve_object.data.shape_keys.eval_time = eval_time
        curve_object.data.shape_keys.keyframe_insert(
            data_path = 'eval_time',
            frame = end_frame
        )
        curve_object.data.shape_keys.eval_time = 0


        for point in self.curve_highlight_points:
            self.animate_point(
                start_frame = start_frame,
                end_frame = end_frame,
                point = point,
                in_place = True
            )


    def add_to_blender(self, **kwargs):
        self.add_axes()
        self.add_function_curve()
        super().add_to_blender(**kwargs)
