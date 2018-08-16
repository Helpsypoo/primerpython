import bpy

import imp
from copy import deepcopy
import math

import bobject
imp.reload(bobject)
from bobject import *

import tex_bobject
imp.reload(tex_bobject)
import svg_bobject
imp.reload(svg_bobject)

class GraphBobject(Bobject):
    """docstring for GraphBobject."""
    def __init__(self,
        *functions,
        overlay_functions = False,
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
        high_res_curve_indices = [0], #by default, make the first curve high res
        **kwargs
    ):
        if 'name' not in kwargs:
            kwargs['name'] = 'graph'
        #Discrete functions usually use few points, but if they are animated
        #with highlight points, it's helpful to have more points.
        self.high_res_curve_indices = high_res_curve_indices
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
        self.tick_labels_x = []
        self.tick_bobjs_x = []
        self.tick_labels_y = []
        self.tick_bobjs_y = []

        #Calculate factor for converting from function space to draw space
        self.domain_scale_factor = self.width / (self.x_range[1] - self.x_range[0])
        self.range_scale_factor = self.height / (self.y_range[1] - self.y_range[0])

        self.arrows = arrows

        self.functions = list(functions)
        self.active_function_index = 0
        self.functions_coords = []
        if len(self.functions) > 0:
            for i in range(len(self.functions)):
                self.functions_coords.append(self.func_to_coords(func_index = i))

        self.curve_highlight_points = []
        self.functions_curves = [] #Filled in self.add_function_curve()
        self.overlay_functions = overlay_functions


        if 'scale' in kwargs:
            scale = kwargs['scale']
        else: scale = 1

        if centered == True:
            self.centered = True
            self.ref_obj.location[0] -= \
                (self.x_range[1] + self.x_range[0]) * self.domain_scale_factor / 2 * scale
            self.ref_obj.location[1] -= \
                (self.y_range[1] + self.y_range[0]) * self.range_scale_factor / 2 * scale

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
        #x_lab_container = tex_complex.TexComplex(x_lab, centered = True, name = 'x_lab_container')
        if self.x_label_pos == 'along':
            x_lab.ref_obj.location = ((self.x_range[1] + self.x_range[0]) * self.domain_scale_factor / 2, -2, 0)
        elif self.x_label_pos == 'end':
            x_lab.ref_obj.location = (self.x_range[1] * self.domain_scale_factor + GRAPH_PADDING + 1.5, 0, 0)
            x_lab.centered = False
        self.add_subbobject(x_lab)
        self.x_label_bobject = x_lab

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
        #y_lab_container = tex_complex.TexComplex(y_lab, centered = True, name = 'y_lab_container')
        if self.y_label_pos == 'along':
            y_lab.ref_obj.location = ( -2, self.y_range[1] * self.range_scale_factor / 2, 0)
        elif self.y_label_pos == 'end':
            y_lab.ref_obj.location = (0, self.y_range[1] * self.range_scale_factor + GRAPH_PADDING + 1.5, 0)
        if self.y_label_rot == True:
            y_lab.ref_obj.rotation_euler = (0, 0, math.pi / 2)
        self.add_subbobject(y_lab)
        self.y_label_bobject = y_lab


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

        if x_tick_step != None:
            current_tick = x_tick_step
            #Positive x ticks
            while current_tick <= self.x_range[1]:
                self.add_tick_x(current_tick)
                current_tick += x_tick_step

            #Negative x ticks
            current_tick = -x_tick_step
            while current_tick >= self.x_range[0]:
                self.add_tick_x(current_tick)
                current_tick -= x_tick_step

        if y_tick_step != None:
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
        tick_scale = min(self.width, self.height) / 20
        cyl_bobj = import_object('cylinder', 'primitives', name = 'x_tick')
        apply_material(cyl_bobj.objects[0], 'color2')
        self.add_subbobject(cyl_bobj)
        self.tick_bobjs_x.append(cyl_bobj)

        ref = cyl_bobj.ref_obj
        ref.location = (value * self.domain_scale_factor, 0, 0)
        ref.children[0].rotation_euler = (math.pi / 2, 0, 0)
        ref.children[0].scale = (AXIS_WIDTH / 2, AXIS_DEPTH / 2, tick_scale)

        label_scale = 0.5
        label = tex_bobject.TexBobject(
            str(value),
            #Scale label position based on tick length, but stay far enough
            #away to avoid overlap
            location = (
                value * self.domain_scale_factor,
                min(-label_scale, -2 * tick_scale),
                0
            ),
            centered = True,
            scale = label_scale
        )
        self.add_subbobject(label)
        self.tick_labels_x.append(label)

        return cyl_bobj, label

    def add_tick_y(self, value):
        tick_scale = min(self.width, self.height) / 20
        cyl_bobj = import_object('cylinder', 'primitives', name = 'y_tick')
        apply_material(cyl_bobj.objects[0], 'color2')
        self.add_subbobject(cyl_bobj)
        ref = cyl_bobj.ref_obj
        ref.location = (0, value * self.range_scale_factor, 0)
        ref.children[0].rotation_euler = (0, math.pi / 2, 0)
        ref.children[0].scale = (AXIS_DEPTH / 2, AXIS_WIDTH / 2, tick_scale)
        self.tick_bobjs_y.append(cyl_bobj)

        label_scale = 0.5
        label = tex_bobject.TexBobject(
            str(value),
            location = (
                min(-label_scale / 1.5, -2 * tick_scale),
                value * self.range_scale_factor,
                0
            ),
            centered = 'right',
            scale = label_scale
        )
        self.add_subbobject(label)
        self.tick_labels_y.append(label)

        #Only used when changing window, since in that case, the new bobjects
        #aren't added when add_to_blender() is called on the
        return cyl_bobj, label

    def change_window(
        self,
        start_time = None,
        end_time = None,
        new_x_range = None,
        new_y_range = None,
        new_tick_step = None
    ):
        #Only works properly when lower bounds are zero.
        #Or, more generally, when the mapping from old to new is simply a
        #scale factor

        if start_time == None:
            raise Warning('Must define start time for change_window()')
        start_frame = int(start_time * FRAME_RATE)

        if end_time == None:
            end_frame = start_frame + OBJECT_APPEARANCE_TIME
        else:
            end_frame = int(end_time * FRAME_RATE)


        if new_x_range == None:
            new_x_range = self.x_range
        if new_y_range == None:
            new_y_range = self.y_range
        if new_tick_step == None:
            new_tick_step = self.tick_step

        #Add new ticks
        tick_step = new_tick_step
        if tick_step == 'auto':
            num_steps_x = self.width / AUTO_TICK_SPACING_TARGET
            x_tick_step = math.floor((new_x_range[1] - new_x_range[0]) / num_steps_x)

            num_steps_y = self.height / AUTO_TICK_SPACING_TARGET
            y_tick_step = math.floor((new_y_range[1] - new_y_range[0]) / num_steps_y)

        else:
            if isinstance(tick_step, list):
                x_tick_step = tick_step[0]
                y_tick_step = tick_step[1]
            elif isinstance(tick_step, int) or isinstance(tick_step, float):
                x_tick_step = y_tick_step = tick_step
            else:
                raise Warning('Idk wtf to do with that tick step.')

        if x_tick_step != None:
            current_tick = x_tick_step
            #Positive x ticks
            while current_tick <= new_x_range[1]:
                stagger_frame = (new_x_range[1] - current_tick) / new_x_range[1] * OBJECT_APPEARANCE_TIME
                needed = True
                for existing_tick in self.tick_bobjs_x:
                    if int(round(existing_tick.ref_obj.location[0] / self.domain_scale_factor)) == current_tick:
                        needed = False
                if needed == True:
                    new_tick_bobjs = self.add_tick_x(current_tick)
                    for bobj in new_tick_bobjs:
                        bobj.add_to_blender(appear_frame = start_frame + OBJECT_APPEARANCE_TIME - stagger_frame)
                current_tick += x_tick_step

            #Negative x ticks
            current_tick = -x_tick_step
            while current_tick >= new_x_range[0]:
                stagger_frame = (current_tick - new_x_range[0]) / new_x_range[1] * OBJECT_APPEARANCE_TIME
                needed = True
                for existing_tick in self.tick_bobjs_x:
                    if int(round(existing_tick.ref_obj.location[0] / self.domain_scale_factor)) == current_tick:
                        needed = False
                if needed == True:
                    new_tick_bobjs = self.add_tick_x(current_tick)
                    for bobj in new_tick_bobjs:
                        bobj.add_to_blender(appear_frame = start_frame + OBJECT_APPEARANCE_TIME - stagger_frame)
                current_tick -= x_tick_step

        if y_tick_step != None:
            current_tick = y_tick_step
            #Positive y ticks
            while current_tick <= new_y_range[1]:
                stagger_frame = (new_y_range[1] - current_tick) / new_y_range[1] * OBJECT_APPEARANCE_TIME
                needed = True
                for existing_tick in self.tick_bobjs_y:
                    if int(round(existing_tick.ref_obj.location[0] / self.domain_scale_factor)) == current_tick:
                        needed = False
                if needed == True:
                    new_tick_bobjs = self.add_tick_y(current_tick)
                    for bobj in new_tick_bobjs:
                        bobj.add_to_blender(appear_frame = start_frame + OBJECT_APPEARANCE_TIME - stagger_frame)
                current_tick += y_tick_step

            #Negative y ticks
            current_tick = -y_tick_step
            while current_tick >= new_y_range[0]:
                stagger_frame = (current_tick - new_y_range[0]) / new_y_range[1] * OBJECT_APPEARANCE_TIME
                needed = True
                for existing_tick in self.tick_bobjs_y:
                    if int(round(existing_tick.ref_obj.location[0] / self.domain_scale_factor)) == current_tick:
                        needed = False
                if needed == True:
                    new_tick_bobjs = self.add_tick_y(current_tick)
                    for bobj in new_tick_bobjs:
                        bobj.add_to_blender(appear_frame = start_frame + OBJECT_APPEARANCE_TIME - stagger_frame)
                current_tick -= y_tick_step

        self.tick_step = new_tick_step

        #Make old ticks disappear
        #Move all ticks
        x_scale_factor = (self.x_range[1] - self.x_range[0]) / \
                       (new_x_range[1] - new_x_range[0])

        for bobj in self.tick_labels_x + self.tick_bobjs_x:
            #x = bobj.ref_obj.location[0]
            int_pos = int(round(bobj.ref_obj.location[0] / self.domain_scale_factor))
            if int_pos > 0:
                stagger_frame = (self.x_range[1] - int_pos) / self.x_range[1] * OBJECT_APPEARANCE_TIME
            elif int_pos < 0:
                stagger_frame = (int_pos - self.x_range[0]) / self.x_range[0] * OBJECT_APPEARANCE_TIME
            if int_pos % self.tick_step[0] != 0 or int_pos > new_x_range[1] or \
                                    int_pos < new_x_range[0]:
                bobj.disappear(disappear_frame = start_frame + stagger_frame)

            bobj.move_to(
                start_frame = start_frame,
                end_frame = end_frame,
                new_location = [
                    bobj.ref_obj.location[0] * x_scale_factor,
                    bobj.ref_obj.location[1],
                    bobj.ref_obj.location[2],
                ]
            )

        self.x_range = new_x_range
        self.domain_scale_factor = self.width / (self.x_range[1] - self.x_range[0])

        y_scale_factor = (self.y_range[1] - self.y_range[0]) / \
                       (new_y_range[1] - new_y_range[0])
        for bobj in self.tick_labels_y + self.tick_bobjs_y:
            int_pos = int(round(bobj.ref_obj.location[1] / self.range_scale_factor))
            if int_pos > 0:
                stagger_frame = (self.y_range[1] - int_pos) / self.y_range[1] * OBJECT_APPEARANCE_TIME
            elif int_pos < 0:
                stagger_frame = (int_pos - self.y_range[0]) / self.y_range[0] * OBJECT_APPEARANCE_TIME
            if int_pos % self.tick_step[1] != 0 or int_pos > new_y_range[1] or \
                                    int_pos < new_y_range[0]:
                bobj.disappear(disappear_frame = start_frame)

            bobj.move_to(
                start_frame = start_frame,
                end_frame = end_frame,
                new_location = [
                    bobj.ref_obj.location[0],
                    bobj.ref_obj.location[1] * y_scale_factor,
                    bobj.ref_obj.location[2],
                ]
            )


        self.y_range = new_y_range
        self.range_scale_factor = self.height / (self.y_range[1] - self.y_range[0])

        #Morph curve to fit new window
        #Add function to function list again.
        func = self.functions[self.active_function_index]
        self.functions.append(func)
        #Then make new coords set based on function.
        self.functions_coords.append(self.func_to_coords(func_index = -1))

        '''print()
        print()
        print()
        for j in range(len(self.functions_coords)):
            print(j, len(self.functions_coords[j]))
        print()
        print()
        print()'''

        #Morph curve to new function
        self.morph_curve(-1, start_time = start_time)

    def highlight_region(
        self,
        start_time = None,
        end_time = None,
        x_region = None,
        y_region = None,
        color = 'color7',
        highlight_direction = 'x'
    ):
        if start_time == None:
            raise Warning('Must define start time for change_window()')
        start_frame = int(start_time * FRAME_RATE)

        if end_time == None:
            #twice as long here to allow for appearance and disappearance
            end_frame = start_frame +  2 * OBJECT_APPEARANCE_TIME
        else:
            end_frame = int(end_time * FRAME_RATE)

        if x_region == None or y_region == None:
            raise Warning("Need to define region to highlight region in graph")

        x_region = [
            x_region[0] * self.domain_scale_factor,
            x_region[1] * self.domain_scale_factor
        ]
        y_region = [
            y_region[0] * self.range_scale_factor,
            y_region[1] * self.range_scale_factor
        ]

        bpy.ops.mesh.primitive_plane_add(location = [0, 0, 0])
        rect = bpy.context.object


        if highlight_direction == 'x':
            region = bobject.Bobject(
                objects = [rect],
                location = [
                    x_region[0],
                    (y_region[1] + y_region[0])/2,
                    0
                ],
                name = 'region',
                scale = [
                    0,
                    (y_region[1] - y_region[0])/2,
                    0
                ]
            )
            region.ref_obj.parent = self.ref_obj
            apply_material(rect, color)
            region.add_to_blender(appear_time = start_time)

            #expand region
            region.move_to(
                start_frame = start_frame,
                new_location = [
                    (x_region[1] + x_region[0])/2,
                    (y_region[1] + y_region[0])/2,
                    0
                ],
                new_scale = [
                    (x_region[1] - x_region[0])/2,
                    (y_region[1] - y_region[0])/2,
                    0
                ]
            )

            #close region
            region.move_to(
                end_frame = end_frame,
                new_location = [
                    x_region[1],
                    (y_region[1] + y_region[0])/2,
                    0
                ],
                new_scale = [
                    0,
                    (y_region[1] - y_region[0])/2,
                    0
                ]
            )

            region.disappear(disappear_frame = end_frame + OBJECT_APPEARANCE_TIME)
        if highlight_direction == 'y':
            region = bobject.Bobject(
                objects = [rect],
                location = [
                    (x_region[1] + x_region[0])/2,
                    y_region[0],
                    0
                ],
                name = 'region',
                scale = [
                    (x_region[1] - x_region[0])/2,
                    0,
                    0
                ]
            )
            region.ref_obj.parent = self.ref_obj
            apply_material(rect, color)
            region.add_to_blender(appear_time = start_time)

            #expand region
            region.move_to(
                start_frame = start_frame,
                new_location = [
                    (x_region[1] + x_region[0])/2,
                    (y_region[1] + y_region[0])/2,
                    0
                ],
                new_scale = [
                    (x_region[1] - x_region[0])/2,
                    (y_region[1] - y_region[0])/2,
                    0
                ]
            )

            #close region
            region.move_to(
                end_frame = end_frame,
                new_location = [
                    (x_region[1] + x_region[0])/2,
                    y_region[1],
                    0
                ],
                new_scale = [
                    (x_region[1] - x_region[0])/2,
                    0,
                    0
                ]
            )

            region.disappear(disappear_frame = end_frame + OBJECT_APPEARANCE_TIME)

    def add_function_curve(
        self,
        index = 0,
        color = 3,
        mat_modifier = None,
        z_shift = 0
    ):
        coords = self.functions_coords[index]

        data = bpy.data.curves.new(name = 'function_curve_data', type = 'CURVE')
        data.dimensions = '2D'
        data.resolution_u = 64
        data.render_resolution_u = 64

        if isinstance(self.functions[index], list):
            #Make bezier curve for discrete functions.
            #raise Warning("FUCK ALL Y'ALL")
            data.splines.new('BEZIER')
            points = data.splines[0].bezier_points
            points.add(len(coords) - 1) #Spline starts with one point
            for i in range(len(points)):
                point = points[i]
                point.handle_left_type = 'VECTOR'
                point.handle_right_type = 'VECTOR'

                x, y, z = coords[i]
                if i == 0 and mat_modifier != 'fade':
                    z = - 2 * CURVE_Z_OFFSET
                z += z_shift
                point.co = (x, y, z)

                if i > 0:
                    point.handle_left = coords[i - 1]
                else:
                    point.handle_left = coords[i]
                if i < len(points) - 1:
                    point.handle_right = coords[i + 1]
                else:
                    point.handle_right = coords[i]

        else:
            data.splines.new('NURBS')

            '''if mat_modifier == 'fade':
                #Reduce point density to allow more memory for more overlapping curves
                #Keeping the final point doesn't actually seem to work quite right,
                #but it looks good enough.
                final = deepcopy(coords[-1])
                #coords = coords[0::10]
                coords.append(final)
                pass'''

            #Add another coord to the beginning and end because NURBS curves
            #don't draw all the way to the exteme points.
            start_coord = [
                coords[0][0] - (coords[1][0] - coords[0][0]),
                coords[0][1] - (coords[1][1] - coords[0][1]),
                coords[0][2] - (coords[1][2] - coords[0][2])
            ]
            coords.insert(0, start_coord)
            end_coord = start_coord = [
                coords[-1][0] + (coords[-2][0] - coords[-1][0]),
                coords[-1][1] + (coords[-2][1] - coords[-1][1]),
                coords[-1][2] + (coords[-2][2] - coords[-1][2])
            ]
            coords.append(end_coord)

            points = data.splines[0].points
            points.add(len(coords) - 1) #Spline starts with one point
            for i in range(len(points)):
                x, y, z = coords[i]
                if i == 0 and mat_modifier != 'fade':
                    z = - 2 * CURVE_Z_OFFSET
                z += z_shift
                points[i].co = (x, y, z, 1)

        cur = bpy.data.objects.new(name = 'function_curve', object_data = data)

        if mat_modifier == None:
            mat_string = 'color' + str(color)
        elif mat_modifier == 'fade':
            mat_string = 'trans_color' + str(color)
        apply_material(cur, mat_string)

        bpy.ops.curve.primitive_bezier_circle_add()
        cross_section = bpy.context.object
        cross_section.scale = [CURVE_WIDTH, CURVE_WIDTH, 0]
        cross_section.parent = self.ref_obj
        cross_section.hide = True
        cross_section.hide_render = True
        #bpy.context.scene.objects.unlink(cross_section)

        cur.data.bevel_object = cross_section

        cur_bobj = bobject.Bobject(objects = [cur], name = 'function_curve_container')
        #cross_section.parent = cur_bobj.ref_obj
        self.add_subbobject(cur_bobj)
        self.functions_curves.append(cur_bobj)

        #Double check that the number of curves is in sync with the index given
        if index < 0: index += len(self.functions_curves) #In case index == -1
        if len(self.functions_curves) != index + 1:
            raise Warning('Function count and index are out of sync.')

    def add_all_function_curves(self, curve_colors = 'same'):
        if curve_colors == 'same':
            colors = [3] * len(self.functions)
            modifiers = [None] * len(self.functions)
            z_shift = [0] * len(self.functions)
        elif curve_colors == 'fade_secondary':
            colors = [3] * len(self.functions)
            modifiers = ['fade'] * len(self.functions)
            modifiers[0] = None
            z_shift = [-0.05] * len(self.functions)
            z_shift[0] = 0
        else:
            raise Warning('Have not implemented that color setting')
        for i in range(len(self.functions)):
            self.add_function_curve(
                index = i,
                color = colors[i],
                mat_modifier = modifiers[i],
                z_shift = z_shift[i]
            )

    def add_new_function_and_curve(
        self,
        func,
        curve_mat_modifier = None,
        z_shift = 0,
        color = 3
    ):
        self.functions.append(func)
        self.functions_coords.append(self.func_to_coords(func_index = -1))
        self.add_function_curve(
            index = -1,
            mat_modifier = curve_mat_modifier,
            z_shift = z_shift,
            color = color
        )
        self.functions_curves[-1].add_to_blender(appear_frame = 0)

    def animate_function_curve(
        self,
        start_time = None,
        end_time = None,
        start_frame = None,
        end_frame = None,
        uniform_along_x = False,
        index = 0
    ):
        if start_time != None:
            if start_frame != None:
                raise Warning("You defined both start frame and start time. " +\
                              "Just do one, ya dick.")
            start_frame = int(start_time * FRAME_RATE)
        if end_time != None:
            if end_frame != None:
                raise Warning("You defined both end frame and end time. " +\
                              "Just do one, ya dick.")
            end_frame = int(end_time * FRAME_RATE)

        if end_frame == None:
            raise Warning('Need end frame to animate function curve, ya dick.')

        print(self.functions_curves)
        data = self.functions_curves[index].ref_obj.children[0].data

        #Insert start and end keyframes for bevel_factor_end
        data.bevel_factor_end = 0
        data.keyframe_insert(data_path = 'bevel_factor_end', frame = start_frame)
        data.bevel_factor_end = 1
        data.keyframe_insert(data_path = 'bevel_factor_end', frame = end_frame)

        if uniform_along_x == True:
            make_animations_linear(data)

    def animate_all_function_curves(
        self,
        start_time = None,
        end_time = None,
        start_frame = None,
        end_frame = None,
        uniform_along_x = False,
        start_window = 0,
        skip = 0
    ):
        if start_time != None:
            if start_frame != None:
                raise Warning("You defined both start frame and start time. " +\
                              "Just do one, ya dick.")
            start_frame = int(start_time * FRAME_RATE)
        if end_time != None:
            if end_frame != None:
                raise Warning("You defined both end frame and end time. " +\
                              "Just do one, ya dick.")
            end_frame = int(end_time * FRAME_RATE)

        num_curves = len(self.functions_curves) - skip
        start_interval = (end_frame - start_frame) * start_window / num_curves

        for i in range(num_curves):
            print(i)
            self.animate_function_curve(
                start_frame = start_frame + start_interval * i,
                end_frame = start_frame + start_interval * i + \
                            (end_frame - start_frame) * (1 - start_window),
                uniform_along_x = uniform_along_x,
                index = i + skip
            )

    def evaluate_function(self, input = None, index = None):
        if input == None:
            raise Warning('Need input to evaluate function')
        if index == None:
            index = self.active_function_index

        try:
            func = self.functions[index]
        except:
            raise Warning("You might be trying to evaluate a non-existent " + \
                          "function. Make sure the graph bobject has a function.")

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

        #-1 is sometimes passed here, which doesn't allow it to be recognized in
        #self.high_res_curve_indices, so just wrap around to a positive version.
        if func_index < 0:
            func_index += len(self.functions)
        func = self.functions[func_index]
        coords = []
        if isinstance(func, list) and func_index not in self.high_res_curve_indices:
            #Discrete functions will be made from bezier curves
            #Assumes index can be treated as function input.
            condensed_func = []
            current_y = -math.inf
            for x, y in enumerate(func):
                if y != current_y:
                    condensed_func.append([x, y])
                    current_y = y

            for i, (x, y) in enumerate(condensed_func):
                #For value changes other than the first, add a point at the
                #previous y value to serve as base of the "step up" or the edge
                #of the "step down"
                if x != 0:
                    coords.append([
                        x * self.domain_scale_factor,
                        condensed_func[i -1][1] * self.range_scale_factor,
                        CURVE_Z_OFFSET
                    ])
                coords.append([
                    x * self.domain_scale_factor,
                    y * self.range_scale_factor,
                    CURVE_Z_OFFSET
                ])
                #Add final point at end of domain
                if i == len(condensed_func) - 1 and x < len(func) - 1:
                    coords.append([
                        (len(func) - 1) * self.domain_scale_factor,
                        y * self.range_scale_factor,
                        CURVE_Z_OFFSET
                    ])

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

            #Ensure last val in range is included.
            #Actually, don't, because this can lead to curves with different
            #numbers of points if the range changes, and the presence of the
            #last point doesn't really matter for (would-be) continuous functions
            #if x_vals[-1] < self.x_range[1]:
            #    x_vals.append(self.x_range[1])

            for x in x_vals:
                y = self.evaluate_function(input = x, index = func_index)
                '''try:
                    y = self.evaluate_function(input = x, index = func_index)
                except:
                    raise Warning("It seems like fixing that off-by-one error didn't work.")
                    #Graph draws point at end of the domain, but list functions
                    #don't include that last point
                    y = coords[-1][1] / self.range_scale_factor'''

                coords.append([
                    x * self.domain_scale_factor,
                    y * self.range_scale_factor,
                    CURVE_Z_OFFSET
                ])

        return coords

    def add_point_at_coord(self,
        appear_time = None,
        appear_frame = None,
        coord = [0, 0, 0],
        track_curve = None,
        axis_projections = False
    ):
        if appear_time != None:
            if appear_frame != None:
                raise Warning("You defined both appear frame and appear time. " +\
                              "Just do one, ya dick.")
            appear_frame = appear_time * FRAME_RATE
        elif appear_frame == None:
            appear_frame = 0

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
        #This used to be boolean, so adding a check to remind myself to change
        #old scenes.
        if isinstance(point.track_curve, bool):
            raise Warning("point.track_curve must be an int or None")
        if point.track_curve != None:
            self.curve_highlight_points.append(point)
            #Correct the y value
            point.coord[1] = self.evaluate_function(
                input = point.coord[0],
                index = point.track_curve
            )
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
        start_time = None,
        end_time = None,
        start_frame = None,
        end_frame = None,
        point = None,
        in_place = False,
        track_curve = True
    ):
        if start_time != None:
            if start_frame != None:
                raise Warning("You defined both start frame and start time. " +\
                              "Just do one, ya dick.")
            start_frame = int(start_time * FRAME_RATE)
        if end_time != None:
            if end_frame != None:
                raise Warning("You defined both end frame and end time. " +\
                              "Just do one, ya dick.")
            end_frame = int(end_time * FRAME_RATE)

        if point == None:
            point = self.add_point_at_coord(
            appear_frame = start_frame - OBJECT_APPEARANCE_TIME,
            coord = [0, 0, 0]
        )
        if end_coord == None:
            end_coord = point.coord
        if end_coord[0] > self.x_range[1]:
            pass
            #raise Warning("Moving point outside graph bounds." + \
            #"Feel free to comment out this warning if you did it on purpose.")
        if end_frame == None:
            end_frame = start_frame + OBJECT_APPEARANCE_TIME
            #raise Warning('Need end frame to animate a point in the graph. ' + \
            #              'You are a terrible person.')

        #This condition is a bit goofy but it allows points that normally track
        #the curve to deviate from the curve if desired, using this method's
        #track_curve parameter to confirm that a curve should be tracked.
        #(Defaults to True.)
        if point.track_curve == None or track_curve == False:
            point.ref_obj.keyframe_insert(
                data_path = 'location',
                frame = start_frame
            )
            point.coord = end_coord
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
            if in_place == True: #If point tracks curve and is just moving in
                                 #the y direction as the curve shifts.
                point.ref_obj.keyframe_insert(
                    data_path = 'location',
                    frame = start_frame
                )
                point.coord[1] = self.evaluate_function(
                    input = point.coord[0],
                    index = point.track_curve
                )
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
                        point.coord[1] = self.evaluate_function(
                            input = point.coord[0],
                            index = point.track_curve
                        )

    def multi_animate_point(
        self,
        point = None,
        start_time = None,
        start_frame = None,
        x_of_t = None,
        frames_per_time_step = 1,
        full_coords = False
    ):
        if start_time != None:
            if start_frame != None:
                raise Warning("You defined both start frame and start time. " +\
                              "Just do one, ya dick.")
            start_frame = int(start_time * FRAME_RATE)

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
                                  (x_of_t[i+1][0] - t) * frames_per_time_step)
            except: #Should only run for last element
                #Just use the timing from the previous transition, to make it
                #not look out of place.
                update_time = min(HIGHLIGHT_POINT_UPDATE_TIME,
                                  (t - x_of_t[i-1][0]) * frames_per_time_step)

            end_frame = start_frame + t * frames_per_time_step + update_time
            #Haven't tested this, but trying to making it so I can pass a list
            #of x values or a list of full coords as a denser way of animating
            #several movements of non-curve-constrained points.
            if full_coords == True:
                end_coord = x #Instead of just an x value,
                              #x could be a full spatial coord
            else:
                end_coord = [x, 0, 0]

            self.animate_point(
                point = point,
                start_frame = start_frame + t * frames_per_time_step,
                end_frame = end_frame,
                end_coord = end_coord
            )

    def morph_curve(
        self,
        to_curve_index,
        start_time = None,
        end_time = None,
        start_frame = None,
        end_frame = None
    ):
        if start_time != None:
            if start_frame != None:
                raise Warning("You defined both start frame and start time. " +\
                              "Just do one, ya dick.")
            start_frame = int(start_time * FRAME_RATE)
        if end_time != None:
            if end_frame != None:
                raise Warning("You defined both end frame and end time. " +\
                              "Just do one, ya dick.")
            end_frame = int(end_time * FRAME_RATE)


        if start_frame == None:
            if end_frame == None:
                raise Warning('Need start frame and/or end frame for move_to')
            else:
                start_frame = end_frame - OBJECT_APPEARANCE_TIME

        if end_frame == None:
            end_frame = start_frame + OBJECT_APPEARANCE_TIME

        self.active_function_index = to_curve_index

        curve_object = self.functions_curves[0].ref_obj.children[0]
        bpy.context.scene.objects.active = curve_object
        #bpy.ops.object.mode_set(mode = 'OBJECT')
        #If absolute shape keys exist, set eval_time to zero
        try:
            curve_object.data.shape_keys.eval_time = 0
        except:
            pass
        bpy.ops.object.shape_key_add(from_mix = False)
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
        print(len(final_coords))
        #Add another coord to the beginning and end because NURBS curves
        #don't draw all the way to the exteme points.
        start_coord = [
            final_coords[0][0] - (final_coords[1][0] - final_coords[0][0]),
            final_coords[0][1] - (final_coords[1][1] - final_coords[0][1]),
            final_coords[0][2] - (final_coords[1][2] - final_coords[0][2])
        ]
        final_coords.insert(0, start_coord)
        end_coord = start_coord = [
            final_coords[-1][0] + (final_coords[-2][0] - final_coords[-1][0]),
            final_coords[-1][1] + (final_coords[-2][1] - final_coords[-1][1]),
            final_coords[-1][2] + (final_coords[-2][2] - final_coords[-1][2])
        ]
        final_coords.append(end_coord)

        for j in range(len(self.functions_coords)):
            print(j, len(self.functions_coords[j]))

        bpy.ops.object.mode_set(mode = 'EDIT')
        for j in range(len(curve_object.data.splines[0].points)):
            print(j)
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

    def add_to_blender(self, curve_colors = 'same', **kwargs):
        self.add_axes()
        if len(self.functions) > 0:
            if self.overlay_functions == True:
                self.add_all_function_curves(curve_colors = curve_colors)
            else:
                self.add_function_curve(index = 0)
        super().add_to_blender(**kwargs)

    def move_to(
        self,
        **kwargs
    ):
        if 'new_location' in kwargs and self.centered == True:
            #Likely more complicated than it needs to be, but currently, the
            #ref_obj is situated in a way doesn't take padding into account.

            if 'new_scale' in kwargs:
                scale = kwargs['new_scale']
                if isinstance(scale, (float, int)):
                    scale = [scale] * 3
            else: scale = self.ref_obj.scale

            kwargs['new_location'] = list(kwargs['new_location'])
            kwargs['new_location'][0] -= (self.x_range[1] + self.x_range[0]) * \
                        self.domain_scale_factor * scale[0] / 2
            kwargs['new_location'][1] -= (self.y_range[1] + self.y_range[0]) * \
                        self.range_scale_factor * scale[1] / 2

        super().move_to(**kwargs)
