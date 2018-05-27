import bpy
import mathutils

import inspect
import imp
from random import random
import math
import time

import constants
imp.reload(constants)
from constants import *

import helpers
imp.reload(helpers)
from helpers import *

#Blender Object
class Bobject(object):
    """docstring for ."""
    def __init__(self, **kwargs):
        super().__init__()
        self.kwargs = kwargs #This is used in the set_from_kwargs() method

        self.name = self.get_from_kwargs('name', 'empty')

        #Would be cleaner elsewhere to override the setter to update
        #self.ref_obj.scale when self.scale is updated
        #(similarly for any attribute that's actually on the ref_obj)
        self.scale = self.get_from_kwargs('scale', 1)
        self.appear_frame = self.get_from_kwargs('appear_frame', 0)

        ref_obj = bpy.data.objects.new(name = "empty", object_data = None)
        ref_obj.location = self.get_from_kwargs('location', (0, 0, 0) )
        ref_obj.scale = (self.scale, self.scale, self.scale)
        ref_obj.name = self.name
        self.ref_obj = ref_obj
        #Hide until full bobject added to Blender.
        #Speeds up render by not paying attention to zero-size objects.
        #Commented out because it cause some weird behavior on first try. Need
        #to refactor all the hide stuff. The trouble seems to come from keyframing
        '''hide_self_and_descendants(
            self.ref_obj,
            hide = True,
            keyframes = True,
            frame = 0
        )'''

        self.subbobjects = []
        self.superbobject = None

        self.series = self.get_from_kwargs('series', [])
        self.particle_controller = None

    def get_from_kwargs(self, kwarg_str, default):
        if kwarg_str in self.kwargs:
            return self.kwargs[kwarg_str]
        else:
            return default

    def add_subbobject_to_series(self, subbobject):
        for child in self.ref_obj.children:
            is_from_bobject = False
            for thing in self.series:
                if thing.ref_obj == child:
                    is_from_bobject = True
            if is_from_bobject == False:
                raise Warning('This bobject already has children not in the series.')
        if not isinstance(subbobject, Bobject):
            raise Warning('Subbobjects in series should be bobjects, else Justin gets confused.')

        self.series.append(subbobject)
        subbobject.ref_obj.parent = self.ref_obj

    def add_to_blender(self,
        appear_frame = 0,
        disappear_frame = None,
        animate = True,
        subbobject_timing = 'start'
    ):
        obj = self.ref_obj
        bpy.context.scene.objects.link(obj)
        link_descendants(obj) #Useful for multi-part imports from .blend files
        '''hide_self_and_descendants(
            obj,
            hide = False,
            keyframes = True,
            frame = appear_frame
        )'''

        if animate == True:
            obj.scale = mathutils.Vector((0, 0, 0))
            obj.keyframe_insert(data_path="scale", frame = appear_frame)
            obj.scale = mathutils.Vector((self.scale, self.scale, self.scale))
            obj.keyframe_insert(data_path="scale", frame = appear_frame + OBJECT_APPEARANCE_TIME)

            if disappear_frame != None:
                obj.scale = mathutils.Vector((self.scale, self.scale, self.scale))
                obj.keyframe_insert(data_path="scale", frame = disappear_frame - OBJECT_APPEARANCE_TIME)
                obj.scale = mathutils.Vector((0, 0, 0))
                obj.keyframe_insert(data_path="scale", frame = disappear_frame)
                #Need to put the scale back to original so morphing works properly
                obj.scale = mathutils.Vector((self.scale, self.scale, self.scale))
        else:
            hide_self_and_descendants(obj, hide = False, keyframes = True, frame = appear_frame)
            if disappear_frame != None:
                hide_self_and_descendants(obj, keyframes = True, frame = disappear_frame)


        #Add subbobjects. Doing this here so the above unhiding
        #won't interfere with the hiding of characters in tex_bobjects that are
        #subbobjects
        if animate == False:
            sub_disapp_frame = disappear_frame
        else:
            sub_disapp_frame = None

        if subbobject_timing == 'start':
            for bobj in self.subbobjects:
                bobj.add_to_blender(animate = False, disappear_frame = sub_disapp_frame)
                bobj.ref_obj.parent = self.ref_obj
        elif subbobject_timing == 'flurry':
            timing = OBJECT_APPEARANCE_TIME / len(self.subbobjects)
            for i, bobj in enumerate(self.subbobjects):
                bobj.add_to_blender(
                    appear_frame = appear_frame + i * timing,
                    disappear_frame = sub_disapp_frame, #Will just disappear with the parent
                    animate = True
                )
                bobj.ref_obj.parent = self.ref_obj
        elif isinstance(subbobject_timing, int):
            for i, bobj in enumerate(self.subbobjects):
                bobj.add_to_blender(
                    appear_frame = appear_frame + i * subbobject_timing,
                    disappear_frame = sub_disapp_frame, #Will just disappear with the parent
                    animate = True
                )
                bobj.ref_obj.parent = self.ref_obj
        elif isinstance(subbobject_timing, list):
            if len(subbobject_timing) != len(self.subbobjects):
                print("Subbobject list and timing list are mismatched.")
            for frame, bobj in zip(subbobject_timing, self.subbobjects):
                bobj.add_to_blender(
                    appear_frame = appear_frame + frame,
                    disappear_frame = sub_disapp_frame, #Will just disappear with the parent
                    animate = True
                )
                bobj.ref_obj.parent = self.ref_obj
        else:
            raise Warning("So many types are accepted for subbobject_timing, "
                          "but you still managed to give an invalid value.")

        #if animate == False and disappear_frame != None:
        #    hide_self_and_descendants(obj, keyframes = True, frame = disappear_frame)

        #Hide all but initial bobjects in morph series
        for subbobject in self.series:
            if subbobject == self.series[0]:
                pass
            else:
                hide_self_and_descendants(subbobject.ref_obj)

    def morph_bobject(self, initial_index, final_index, start_frame, end_frame):
        initial_meshes = []
        for child in self.series[initial_index].ref_obj.children:
            initial_meshes.append(child)
            append_descendants(child, initial_meshes)
        final_meshes = []
        for child in self.series[final_index].ref_obj.children:
            final_meshes.append(child)
            append_descendants(child, final_meshes)


        if RENDER_QUALITY == 'medium' or RENDER_QUALITY == "high":
            if self.particle_controller == None:
                controller_bobj = import_object('icosphere', 'primitives')
                controller_ref = controller_bobj.ref_obj
                controller_ref.name = 'TRASH_PILE'
                controller_ref.location = (1000, 0, 0) #This should never be seen
                controller_ref.parent = self.ref_obj
                bpy.context.scene.objects.link(controller_ref)
                link_descendants(controller_ref)
                controller = controller_ref.children[0]
                controller.name = "CONTROLLER"
                self.particle_controller = controller

            #TODO: Change when looping through objects to morph
            #first = initial.children[0]
            #last = final.children[0]
            for first in initial_meshes:
                for last in final_meshes:
                    self.morph_mesh_to_mesh(first, last, start_frame, end_frame)


        else:
            for bobj in self.series:
                for child in bobj.ref_obj.children:
                    if child.hide == False:
                        hide_self_and_descendants(
                            child,
                            keyframes = True,
                            frame = start_frame
                        )
            for mesh in final_meshes:
                hide_self_and_descendants(
                    mesh,
                    hide = False,
                    keyframes = True,
                    frame = start_frame
                )
        if RENDER_QUALITY == 'high':
            print('Bobject morphed')

    def morph_mesh_to_mesh(self, first, last, start_frame, end_frame):
        self.add_morph_particles(first, start_frame, end_frame)
        self.add_morph_particles(last, end_frame - 1, end_frame)
        #Above is a hacky way of making the particles live only at the end frame
        #which allows particles to aim for where the target mesh will be.
        self.key_particles(first, last, start_frame, end_frame)

        #Hide original object once particles have departed
        '''first.hide = False
        first.hide_render = False
        first.keyframe_insert(data_path = 'hide', frame = start_frame + PARTICLE_APPEARANCE_TIME - 1)
        first.keyframe_insert(data_path = 'hide_render', frame = start_frame + PARTICLE_APPEARANCE_TIME - 1)
        first.hide = True
        first.hide_render = True
        first.keyframe_insert(data_path = 'hide', frame = start_frame + PARTICLE_APPEARANCE_TIME)
        first.keyframe_insert(data_path = 'hide_render', frame = start_frame + PARTICLE_APPEARANCE_TIME)'''
        hide_self_and_descendants(first, keyframes = True, frame = start_frame + PARTICLE_APPEARANCE_TIME)

        #Show final object once particles have arrived
        hide_self_and_descendants(last, hide = False, keyframes = True, frame = end_frame - PARTICLE_APPEARANCE_TIME)
        '''last.hide = True
        last.hide_render = True
        last.keyframe_insert(data_path = 'hide', frame = end_frame - PARTICLE_APPEARANCE_TIME - 1)
        last.keyframe_insert(data_path = 'hide_render', frame = end_frame - PARTICLE_APPEARANCE_TIME - 1)
        last.hide = False
        last.hide_render = False
        last.keyframe_insert(data_path = 'hide', frame = end_frame - PARTICLE_APPEARANCE_TIME)
        last.keyframe_insert(data_path = 'hide_render', frame = end_frame - PARTICLE_APPEARANCE_TIME)'''

    def add_morph_particles(self, obj, start_frame, end_frame):
        has_particles = False
        #Could really just search for particle systems directly. No need to
        #look in modifiers.
        for mod in obj.modifiers:
            if mod.type == 'PARTICLE_SYSTEM':
                has_particles = True
                break

        #Just one particle system per mesh, except for on the controller
        if has_particles == False or obj == self.particle_controller:
            mod = obj.modifiers.new("ParticleSystem", type = 'PARTICLE_SYSTEM')
            psys = mod.particle_system
            psys.seed = random() * 10000
            stngs = psys.settings

            stngs.count = PARTICLES_PER_MESH
            stngs.frame_start = start_frame #+ self.appear_frame
            stngs.frame_end = start_frame #+ self.appear_frame
            stngs.lifetime = end_frame - start_frame
            stngs.emit_from = 'FACE'
            stngs.distribution = 'RAND'

            stngs.physics_type = "NO"
            stngs.render_type = 'NONE'


            stngs.normal_factor = 0
            stngs.tangent_factor = 0
            stngs.effector_weights.gravity = 0

            '''if obj != self.particle_controller:
                mod.particle_system.parent = obj
                pass'''

    def key_particles(self, start, end, start_frame, end_frame, backward = False):
        #Once to shoot particles out of the original object
        self.add_morph_particles(self.particle_controller, start_frame, end_frame)
        psys = self.particle_controller.modifiers[-1].particle_system
        stngs = psys.settings

        #Set up particle keys
        stngs.physics_type = "KEYED"
        psys.use_keyed_timing = True

        #Set up object for particles to duplicate (for color)
        stngs.render_type = 'OBJECT'
        bpy.ops.mesh.primitive_ico_sphere_add(location = (1000, 0, 0))
        dup = bpy.context.object
        #dup.parent = start
        dup.parent = self.particle_controller.parent
        dup.data.materials.append(start.active_material)
        stngs.dupli_object = dup

        #stngs.size_random = 1
        stngs.particle_size = 0
        stngs.keyframe_insert(data_path = 'particle_size', frame = start_frame)
        stngs.particle_size = MORPH_PARTICLE_SIZE
        stngs.keyframe_insert(data_path = 'particle_size', frame = start_frame + PARTICLE_APPEARANCE_TIME)
        stngs.particle_size = 0
        stngs.keyframe_insert(data_path = 'particle_size', frame = end_frame)

        bpy.ops.particle.new_target({'particle_system': psys})
        targ = psys.targets[-1]
        targ.object = start
        targ.duration = PARTICLE_APPEARANCE_TIME

        bpy.ops.particle.new_target({'particle_system': psys})
        targ = psys.targets[-1]
        targ.object = end
        targ.time = end_frame - start_frame


        #And again to suck particles into new object
        #Might make sense to reorg this
        self.add_morph_particles(self.particle_controller, start_frame, end_frame)
        psys = self.particle_controller.modifiers[-1].particle_system
        stngs = psys.settings

        #Set up particle keys
        stngs.physics_type = "KEYED"
        psys.use_keyed_timing = True

        #Set up object for particles to duplicate (for color)
        stngs.render_type = 'OBJECT'
        bpy.ops.mesh.primitive_ico_sphere_add(location = (1000, 0, 0))
        dup = bpy.context.object
        dup.parent = self.particle_controller.parent
        #dup.parent = end
        dup.data.materials.append(end.active_material)
        stngs.dupli_object = dup

        bpy.ops.particle.new_target({'particle_system': psys})
        targ = psys.targets[-1]
        targ.object = start

        bpy.ops.particle.new_target({'particle_system': psys})
        targ = psys.targets[-1]
        targ.object = end
        targ.time = end_frame - start_frame - PARTICLE_APPEARANCE_TIME
        targ.duration = PARTICLE_APPEARANCE_TIME

        #stngs.size_random = 1
        stngs.particle_size = 0
        stngs.keyframe_insert(data_path = 'particle_size', frame = start_frame)
        stngs.particle_size = MORPH_PARTICLE_SIZE
        stngs.keyframe_insert(data_path = 'particle_size', frame = end_frame - PARTICLE_APPEARANCE_TIME)
        stngs.particle_size = 0
        stngs.keyframe_insert(data_path = 'particle_size', frame = end_frame)

    def move_to(
        self,
        start_frame,
        end_frame,
        displacement = None,
        new_location = None,
        new_scale = None,
        scale_until = None
    ):
        obj = self.ref_obj
        if displacement != None:
            for dx, x in zip(displacement, self.ref_obj.location):
                x += dx
            obj.keyframe_insert(data_path="location", frame = start_frame)
            obj.keyframe_insert(data_path="location", frame = end_frame)

        if new_location != None:
            obj.keyframe_insert(data_path="location", frame = start_frame)
            obj.location = new_location
            obj.keyframe_insert(data_path="location", frame = end_frame)
        if new_scale != None:
            if end_frame >= scale_until:
                raise Warning('In move_to(), end frame is after scale_until')
            obj.keyframe_insert(data_path="scale", frame = start_frame)
            obj.scale = [new_scale ] * 3
            self.scale = new_scale
            obj.keyframe_insert(data_path="scale", frame = end_frame)
            #Need to add an extra keyframe to avoid clashing with the disappear
            #animation
            obj.keyframe_insert(data_path="scale", frame = scale_until)

    def pulse(
        self,
        frame = 0,
        factor = 1.2,
        attack = OBJECT_APPEARANCE_TIME / 2,
        decay = OBJECT_APPEARANCE_TIME / 2,
        duration = OBJECT_APPEARANCE_TIME,
    ):
        obj = self.ref_obj
        obj.keyframe_insert(data_path="scale", frame = frame)
        obj.scale *= factor
        obj.keyframe_insert(data_path="scale", frame = frame + attack)
        obj.keyframe_insert(data_path="scale", frame = frame + duration - decay)
        obj.scale /= factor
        obj.keyframe_insert(data_path="scale", frame = frame + duration)

class TexComplex(Bobject):
    """docstring for TexComplex."""
    def __init__(self, *tex_bobjects, center = False, **kwargs):
        super().__init__(**kwargs)
        self.subbobjects = tex_bobjects
        for sub in tex_bobjects:
            sub.superbobject = self
        self.centered = center

    def add_to_blender(self, **kwargs):
        super().add_to_blender(**kwargs)

        #Add constituent tex_bobjects to blender at frame 0
        #Their actual appearance will be controlled by the complex
        #Commented out because this so far does not behave differently from
        #self.subbobjects.
        '''
        for tex_bobj in self.tex_bobjects:
            tex_bobj.add_to_blender(animate = False)
            tex_bobj.ref_obj.parent = self.ref_obj
        '''


        self.arrange_tex_bobjects()

    def arrange_tex_bobjects(self, start_frame = None, end_frame = None, center = None):
        t_bobjs = self.subbobjects

        if start_frame != None:
            bpy.context.scene.frame_set(start_frame)
            bpy.context.scene.update()
            for t_bobj in t_bobjs:
                t_bobj.ref_obj.keyframe_insert(data_path = 'location', frame = start_frame)

        if end_frame != None:
            bpy.context.scene.frame_set(end_frame)
            bpy.context.scene.update()

        next_align = 0
        for t_bobj in t_bobjs:
            #Align expression
            t_bobj_length = t_bobj.expressions[t_bobj.active_expression_index]['length']
            if t_bobj.centered == True:
                t_bobj.ref_obj.location[0] = next_align + t_bobj_length / 2
            else:
                t_bobj.ref_obj.location[0] = next_align
            expr_length = t_bobj_length
            next_align += expr_length + \
                         SPACE_BETWEEN_EXPRESSIONS * t_bobj.ref_obj.scale[0]

        if center == None: center = self.centered
        if center == True:
            next_align -= SPACE_BETWEEN_EXPRESSIONS
            for t_bobj in t_bobjs:
                t_bobj.ref_obj.location[0] -= next_align / 2

        if end_frame != None:
            for t_bobj in t_bobjs:
                t_bobj.ref_obj.keyframe_insert(data_path = 'location', frame = end_frame)

class RainBobject(Bobject):
    """docstring for RainBobject.
    This is really just made for one instance. If I do more rain, I'll need to
    make it more customizable.
    """
    def __init__(self, start_raining = 0, stop_raining = 0, **kwargs):
        super().__init__(**kwargs)

        self.start_raining = start_raining
        self.stop_raining = stop_raining

        self.make_it_rain()

    def add_to_blender(self, **kwargs):
        super().add_to_blender(**kwargs)

        #This override allows drops to fall away after the collision objects
        #go away, rather than just disappearing.

        if kwargs['animate'] == True:
            raise Warning("RainBobjects are currently designed to not be animated")

        disappear_frame = kwargs['disappear_frame']

        #Make emitter and raindrop last longer
        if disappear_frame != None:
            for obj in [self.emitter, self.raindrop]:
                obj.hide = False
                obj.hide_render = False
                obj.keyframe_insert(data_path = 'hide', frame = disappear_frame)
                obj.keyframe_insert(data_path = 'hide_render', frame = disappear_frame)
                hide_self_and_descendants(obj, keyframes = True, frame = disappear_frame + 100)

        #Make drops fall through hidden collision_objects
        for obj in self.collision_objects:
            col = obj.collision
            col.keyframe_insert(data_path = 'permeability', frame = disappear_frame - 1)
            col.permeability = 1
            col.keyframe_insert(data_path = 'permeability', frame = disappear_frame)

    def make_it_rain(self):
        emitter_container = import_object('xzplane', 'primitives', name = 'emitter')
        emitter_container.ref_obj.parent = self.ref_obj
        emitter_container.ref_obj.location = (0, 12, 0)
        emitter_container.ref_obj.scale = (16, 16, 16)

        emitter = emitter_container.ref_obj.children[0]
        #A bit hacky, but this method links the emitter object to the scene,
        #changes settings, and then unlinks the emitter object. The normal flow
        #with bobjects is to set everything up, then link the object(s) to the
        #scene, but this particular emitter uses fluid physics for the particle
        #system, which needs to be linked to the scene to update settings.
        bpy.context.scene.objects.link(emitter)
        emitter.scale[2] = 1/160
        self.emitter = emitter #Used to override add_to_blender()

        mod = emitter.modifiers.new("ParticleSystem", type = 'PARTICLE_SYSTEM')
        psys = mod.particle_system
        psys.seed = random() * 10000
        stngs = psys.settings

        #Could improve this by making rain density a constant and setting count
        #based on that density and that duration
        stngs.count = 30000
        stngs.frame_start = self.start_raining #+ self.appear_frame +
        stngs.lifetime = self.stop_raining - self.start_raining
        #Stop emitting drops in time to have them all run out by the end frome
        fall_time = 55 #probably make this an arg when generalizing
        stngs.frame_end = self.stop_raining - fall_time #+ self.appear_frame
        stngs.emit_from = 'FACE'
        stngs.distribution = 'RAND'
        stngs.normal_factor = 0
        stngs.tangent_factor = 0
        stngs.factor_random = 0.5
        stngs.brownian_factor = 0.1

        stngs.physics_type = 'FLUID'
        bpy.data.scenes[0].update()
        stngs.fluid.solver = 'CLASSICAL'
        stngs.fluid.fluid_radius = 0.2
        stngs.render_type = 'OBJECT'
        stngs.particle_size = 0.05
        stngs.size_random = 0.5
        dup_bobj = import_object('goodicosphere', 'primitives', location = (1000, 0 , 0), name = 'raindrop model')
        dup_bobj.ref_obj.parent = self.ref_obj
        dup = dup_bobj.ref_obj.children[0]
        apply_material(dup, 'clear')
        stngs.dupli_object = dup
        self.raindrop = dup

        #See comment above about why linking and unlinking happens here.
        bpy.context.scene.objects.unlink(emitter)

        #bpy.data.scenes['Scene.001'].objects.unlink(bpy.data.objects['Cube.001'])


        obj = bpy.context.object

        '''stngs = obj.particle_systems[0].settings

        stngs.physics_type = 'FLUID'
        stngs.fluid.solver = 'CLASSICAL'
        stngs.fluid.fluid_radius = 0.05'''

    def add_collision_objects(self, *collision_objects, text = False, frame = 0):
        objects = []
        new_objects = []
        if text == True:
            for obj in collision_objects:
                #objects.append(obj)
                #intentionally don't append the object itself, since for text,
                #it's a hidden reference object
                append_descendants(obj, objects)

            scn = bpy.context.scene
            scn.frame_set(frame)

            for obj in objects: #Skip the reference character if text
                obj.data.extrude = 0.1
                new_mesh = obj.to_mesh(scn, True, 'PREVIEW')
                new_obj = bpy.data.objects.new('collision', new_mesh)
                obj.data.extrude = 0
                new_obj.parent = self.ref_obj
                new_obj.matrix_world = obj.matrix_world

                new_obj.modifiers.new("CollisionSettings", type = 'COLLISION')
                new_obj.collision.damping_factor = 0.8
                new_obj.collision.damping_random = 0.5
                new_objects.append(new_obj)

        else:
            raise Warning("Collision objects not implemented for non-text")
        self.collision_objects = new_objects
        bpy.data.scenes[0].update()
