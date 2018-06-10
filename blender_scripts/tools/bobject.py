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

#Blender Object
class Bobject(object):
    """docstring for ."""
    #Create object data
    def __init__(self, *subbobjects, **kwargs):
        super().__init__()
        self.kwargs = kwargs #This is used in the get_from_kwargs() method

        self.name = self.get_from_kwargs('name', 'bobject')

        #Would be cleaner elsewhere to override the setter to update
        #self.ref_obj.scale when self.scale is updated
        #(similarly for any attribute that's actually on the ref_obj)
        self.appear_frame = self.get_from_kwargs('appear_frame', 0)

        ref_obj = bpy.data.objects.new(name = self.name, object_data = None)
        ref_obj.location = self.get_from_kwargs('location', (0, 0, 0) )
        ref_obj.rotation_euler = self.get_from_kwargs('rotation_euler', (0, 0, 0) )
        self.scale = self.get_from_kwargs('scale', 1)
        if isinstance(self.scale, int) or isinstance(self.scale, float):
            self.scale = [self.scale] * 3
        ref_obj.scale = self.scale
        ref_obj.name = self.name
        self.ref_obj = ref_obj

        #Blender objects with this bobject as the container
        self.objects = self.get_from_kwargs('objects', [])
        for obj in self.objects:
            obj.parent = ref_obj

        #Other bobject containers which handle themselves
        self.subbobjects = self.get_from_kwargs('subbobjects', [])
        for bobj in subbobjects:
            self.add_subbobject(bobj)

        self.superbobject = None #Changed when initializing a super
        self.appear_with_super = self.get_from_kwargs('appear_with_super', True)

    def get_from_kwargs(self, kwarg_str, default):
        if kwarg_str in self.kwargs:
            return self.kwargs[kwarg_str]
        else:
            return default

    def add_subbobject(self, bobj):
        self.subbobjects.append(bobj)
        bobj.ref_obj.parent = self.ref_obj
        bobj.superbobject = self

    def add_to_blender(self,
        appear_frame = 0,
        animate = True,
        subbobject_timing = 'start',
        transition_time = OBJECT_APPEARANCE_TIME,
        is_creature = False
    ):
        main_obj = self.ref_obj
        if main_obj.name not in bpy.context.scene.objects:
            bpy.context.scene.objects.link(main_obj)
        else:
            pass
            #print("Re-adding " + self.name)


        main_obj.hide = True
        main_obj.hide_render = True
        main_obj.keyframe_insert(data_path="hide", frame = appear_frame - 1)
        main_obj.keyframe_insert(data_path="hide_render", frame = appear_frame - 1)
        main_obj.hide = False
        main_obj.keyframe_insert(data_path="hide", frame = appear_frame)


        for obj in self.objects:
            if obj.name not in bpy.context.scene.objects:
                bpy.context.scene.objects.link(obj)
            link_descendants(obj) #Useful for multi-part imports from .blend files
            hide_self_and_descendants(
                obj,
                keyframes = True,
                frame = appear_frame - 1
            )
            hide_self_and_descendants(
                obj,
                hide = False, #Unhide objects
                keyframes = True,
                frame = appear_frame
            )

        if animate == False:
            if self.superbobject == None:
                scale_up_frame = appear_frame - transition_time
            #Might be able to get rid of this once morphing is fixed
            else:
                #print(self.superbobject.appear_frame)
                scale_up_frame = self.superbobject.appear_frame - transition_time
            #Makes the scale-up happen before the unhiding if we don't want
            #the bobject to animate in
        else:
            scale_up_frame = appear_frame
        if is_creature == True:
            duration = MATURATION_TIME
        else:
            duration = transition_time

        main_obj.scale = [0, 0, 0]
        main_obj.keyframe_insert(data_path="scale", frame = scale_up_frame)
        main_obj.scale = self.scale
        main_obj.keyframe_insert(data_path="scale", frame = scale_up_frame + duration)
        #don't need to do this for contained objects because it happens through
        #parenting

        followers = [x for x in self.subbobjects if x.appear_with_super == True]

        #appear_frame += subbobject_delay #Just for TexComplex bobjects right now

        if subbobject_timing == 'start':
            for bobj in followers:
                bobj.add_to_blender(
                    appear_frame = appear_frame,
                    animate = animate,
                    transition_time = transition_time
                )
        elif subbobject_timing == 'flurry':
            timing = transition_time / len(self.subbobjects)
            for i, bobj in enumerate(followers):
                bobj.add_to_blender(appear_frame = appear_frame + i * timing)
        elif isinstance(subbobject_timing, int):
            for i, bobj in enumerate(followers):
                bobj.add_to_blender(appear_frame = appear_frame + subbobject_timing)
        elif isinstance(subbobject_timing, list):
            if len(subbobject_timing) != len(followers):
                print("Subbobject list and timing list are mismatched.")
            for frame, bobj in zip(subbobject_timing, followers):
                #frame += subbobject_delay
                bobj.add_to_blender(appear_frame = appear_frame + frame, animate = True)
        else:
            raise Warning("So many types are accepted for subbobject_timing, "
                          "but you still managed to give an invalid value.")


    #Keyframe additions
    def disappear(self,
        disappear_frame = None,
        animate = True,
        no_shrink = False,
        is_creature = False
    ):
        if disappear_frame == None:
            raise Warning('Must specify frame for bobject disappearance')

        main_obj = self.ref_obj

        main_obj.hide = True
        main_obj.hide_render = True
        main_obj.keyframe_insert(data_path="hide", frame = disappear_frame)
        main_obj.keyframe_insert(data_path="hide_render", frame = disappear_frame)

        for obj in self.objects:
            hide_self_and_descendants(
                obj,
                keyframes = True,
                frame = disappear_frame
            )

        if is_creature == True:
            duration = MATURATION_TIME
        else:
            duration = OBJECT_APPEARANCE_TIME

        if animate == True:
            #scale_down_frame = disappear_frame + OBJECT_APPEARANCE_TIME
            #Makes the scale-down happen after the hiding if we don't want
            #the bobject to animate out
            scale_down_frame = disappear_frame

            #Uses current scale. This assumes keyframes have been added
            #chronologically, so the previous keyframe agrees with the current
            #object scale.
            main_obj.keyframe_insert(data_path="scale", frame = scale_down_frame - duration)
            main_obj.scale = [0, 0, 0]
            main_obj.keyframe_insert(data_path="scale", frame = scale_down_frame)

        else:
            scale_down_frame = disappear_frame



        for subbobj in self.subbobjects:
            subbobj.disappear(disappear_frame = disappear_frame, animate = False)

    def move_to(
        self,
        start_frame = None,
        end_frame = None,
        displacement = None,
        new_location = None,
        new_scale = None,
        new_angle = None
    ):
        if start_frame == None:
            if end_frame == None:
                raise Warning('Need start frame and/or end frame for move_to')
            else:
                start_frame = end_frame - OBJECT_APPEARANCE_TIME

        if end_frame == None:
            end_frame = start_frame + OBJECT_APPEARANCE_TIME

        obj = self.ref_obj
        if displacement != None:
            obj.keyframe_insert(data_path="location", frame = start_frame)
            for i in range(len(self.ref_obj.location)):
                self.ref_obj.location[i] += displacement[i]
            obj.keyframe_insert(data_path="location", frame = end_frame)
        if new_location != None:
            obj.keyframe_insert(data_path="location", frame = start_frame)
            obj.location = new_location
            obj.keyframe_insert(data_path="location", frame = end_frame)
        if new_scale != None:
            #if end_frame >= scale_until:
            #    raise Warning('In move_to(), end frame is after scale_until')
            obj.keyframe_insert(data_path="scale", frame = start_frame)
            if isinstance(new_scale, int) or isinstance(new_scale, float):
                new_scale = [new_scale] * 3
            obj.scale = new_scale
            self.scale = new_scale
            obj.keyframe_insert(data_path="scale", frame = end_frame)
        if new_angle != None:
            obj.keyframe_insert(data_path="rotation_euler", frame = start_frame)
            obj.rotation_euler = new_angle
            obj.keyframe_insert(
                data_path="rotation_euler",
                frame = end_frame
            )
        #bpy.context.scene.update()

    def spiny(
        self,
        spin_rate = 1, #Revolutions per second
        start_frame = None,
        end_frame = None
    ):
        if start_frame == None:
            raise Warning('Need start frame for spin function')
        if end_frame == None:
            raise Warning('Need end frame for spin function')

        obj = self.ref_obj
        obj.keyframe_insert(data_path="rotation_euler", frame = start_frame)

        new_y = spin_rate * (start_frame - end_frame) / 60 #60 fps

        obj.rotation_euler[1] = new_y
        obj.keyframe_insert(
            data_path="rotation_euler",
            frame = end_frame
        )

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

    def color_shift(
        self,
        color = COLORS_SCALED[3],
        start_frame = 0,
        duration = OBJECT_APPEARANCE_TIME * 2,
        shift_time = OBJECT_APPEARANCE_TIME
    ):
        if duration < shift_time * 2:
            shift_time = duration / 2
            print('Adjusted shift time')

        #For now, only works for simple bobjects
        obj = self.ref_obj.children[0]
        mat_copy = obj.material_slots[0].material.copy()
        obj.active_material = mat_copy
        color_field = mat_copy.node_tree.nodes[-1].inputs[0]

        if duration != None:
            #If duration is finite, store original color
            original_color = list(color_field.default_value)

        color_field.keyframe_insert(data_path = 'default_value', frame = start_frame)
        color_field.default_value = color
        color_field.keyframe_insert(data_path = 'default_value', frame = start_frame + shift_time)

        #Viewport color
        mat_copy.keyframe_insert(data_path = 'diffuse_color', frame = start_frame)
        mat_copy.diffuse_color = color[:3]
        mat_copy.keyframe_insert(data_path = 'diffuse_color', frame = start_frame + shift_time)

        if duration != None:
            #If duration is finite, return to original color
            color_field.keyframe_insert(data_path = 'default_value', frame = start_frame + duration - shift_time)
            color_field.default_value = original_color
            color_field.keyframe_insert(data_path = 'default_value', frame = start_frame + duration)

            mat_copy.keyframe_insert(data_path = 'diffuse_color', frame = start_frame + duration - shift_time)
            mat_copy.diffuse_color = original_color[:3]
            mat_copy.keyframe_insert(data_path = 'diffuse_color', frame = start_frame + duration)

class MeshMorphBobject(Bobject):
    def __init__(self, *subbobjects, **kwargs):
        super().__init__(*subbobjects, **kwargs)
        self.series = self.get_from_kwargs('series', [])
        self.particle_controller = None

    def add_to_blender(self, **kwargs):
        super().add_to_blender(**kwargs)
        self.series[0].add_to_blender(
            animate = False,
            appear_frame = kwargs['appear_frame']
        )

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
        subbobject.superbobject = self

    def morph_bobject(self, initial_index, final_index, start_frame, end_frame, dissolve_time = 0):
        self.series[initial_index].disappear(
            disappear_frame = start_frame + 1,
            animate = False
        )
        self.series[final_index].add_to_blender(
            appear_frame = end_frame,
            animate = False
        )

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
                controller_ref.name = 'morph_helpers'
                controller_ref.location = (0, 1000, 0) #This should never be seen
                controller_ref.parent = self.ref_obj
                bpy.context.scene.objects.link(controller_ref)
                link_descendants(controller_ref)
                controller = controller_ref.children[0]
                controller.name = "particle_controller"
                self.particle_controller = controller

            #TODO: Change when looping through objects to morph
            for first in initial_meshes:
                for last in final_meshes:
                    self.morph_mesh_to_mesh(first, last, start_frame, end_frame, dissolve_time = dissolve_time)

        if RENDER_QUALITY == 'high':
            print('Bobject morphed')

    def morph_mesh_to_mesh(self, first, last, start_frame, end_frame, dissolve_time = 0):
        self.add_morph_particles(first, start_frame, end_frame)
        self.add_morph_particles(last, end_frame - 1, end_frame)
        #Above is a way of making the particles live only at the end frame
        #which allows particles to aim for where the target mesh will be.
        self.key_particles(first, last, start_frame, end_frame, dissolve_time = dissolve_time)

    def add_morph_particles(self, obj, start_frame, end_frame, dissolve_time = 0):
        bpy.context.scene.frame_set(start_frame)
        bpy.context.scene.update()
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
            stngs.frame_end = start_frame + dissolve_time #+ self.appear_frame
            stngs.frame_start = start_frame #+ self.appear_frame
            stngs.lifetime = end_frame - start_frame
            stngs.emit_from = 'FACE'
            stngs.distribution = 'RAND'

            stngs.physics_type = "NO"
            stngs.render_type = 'NONE'


            stngs.normal_factor = 0
            stngs.tangent_factor = 0
            stngs.effector_weights.gravity = 0

    '''def add_turbulent_particles(self, obj, start_frame, end_frame):
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

        stngs.physics_type = 'NEWTON'
        stngs.render_type = 'NONE'

        stngs.normal_factor = 0
        stngs.tangent_factor = 0
        stngs.effector_weights.gravity = 0

        bpy.ops.object.effector_add(type = 'TURBULENCE', location = obj.location)
        turb = bpy.context.object
        turb.parent = self.particle_controller.parent
        turb.field.strength = 1'''


    def key_particles(self, start, end, start_frame, end_frame, backward = False, dissolve_time = 0):
        #Once to shoot particles out of the original object
        self.add_morph_particles(self.particle_controller, start_frame, end_frame, dissolve_time = dissolve_time)
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


        '''self.add_turbulent_particles(start, start_frame, end_frame)
        bpy.ops.particle.new_target({'particle_system': psys})
        targ = psys.targets[-1]
        targ.object = start
        targ.system = 2
        targ.time = (end_frame - start_frame) / 4'''

        bpy.ops.particle.new_target({'particle_system': psys})
        targ = psys.targets[-1]
        targ.object = end
        targ.time = end_frame - start_frame - dissolve_time


        #And again to suck particles into new object
        #Might make sense to reorg this
        self.add_morph_particles(self.particle_controller, start_frame, end_frame, dissolve_time = dissolve_time)
        psys = self.particle_controller.modifiers[-1].particle_system
        stngs = psys.settings

        #Set up particle keys
        stngs.physics_type = "KEYED"
        psys.use_keyed_timing = True

        #Set up object for particles to duplicate (for color)
        stngs.render_type = 'OBJECT'
        bpy.ops.mesh.primitive_ico_sphere_add(location = (0, 1000, 0))
        dup = bpy.context.object
        dup.parent = self.particle_controller.parent
        dup.data.materials.append(end.active_material)
        stngs.dupli_object = dup

        bpy.ops.particle.new_target({'particle_system': psys})
        targ = psys.targets[-1]
        targ.object = start
        targ.duration = PARTICLE_APPEARANCE_TIME

        '''self.add_turbulent_particles(start, start_frame, end_frame)
        bpy.ops.particle.new_target({'particle_system': psys})
        targ = psys.targets[-1]
        targ.object = start
        targ.system = 2
        targ.time = (end_frame - start_frame) / 4'''

        bpy.ops.particle.new_target({'particle_system': psys})
        targ = psys.targets[-1]
        targ.object = end
        targ.time = end_frame - start_frame  - dissolve_time - PARTICLE_APPEARANCE_TIME
        targ.duration = PARTICLE_APPEARANCE_TIME

        #stngs.size_random = 1
        stngs.particle_size = 0
        stngs.keyframe_insert(data_path = 'particle_size', frame = start_frame)
        stngs.particle_size = MORPH_PARTICLE_SIZE
        stngs.keyframe_insert(data_path = 'particle_size', frame = end_frame - PARTICLE_APPEARANCE_TIME)
        stngs.particle_size = 0
        stngs.keyframe_insert(data_path = 'particle_size', frame = end_frame)

class RainBobject(Bobject):
    """docstring for RainBobject.
    This is really just made for one instance. If I do more rain, I'll need to
    make it more customizable.
    """
    def __init__(self, start_raining = 0, stop_raining = 0, **kwargs):
        super().__init__(**kwargs)

        self.start_raining = start_raining + OBJECT_APPEARANCE_TIME
        #The above addition of OBJECT_APPEARANCE_TIME is purposely there in
        #addition to any buffer passed into start_raining to make sure the
        #emitter is in place before it actually starts raining. Probably a more
        #robust way of doing it, but this stopped rogue raindrops for now.
        self.stop_raining = stop_raining

        self.make_it_rain()

    def add_to_blender(self, **kwargs):
        super().add_to_blender(**kwargs)

        #For collision objects, replace the unhide keyframe with another hide
        #keyframe so they are never actually shown. They're just for physics.
        #Doing it this way so the extra thickness on characters doesn't appear.
        #More keyframes than necessary.
        appear_frame = kwargs['appear_frame']
        for obj in self.collision_objects:
            obj.hide = True
            obj.hide_render = True
            obj.keyframe_insert(data_path="hide", frame = appear_frame)
            obj.keyframe_insert(data_path="hide_render", frame = appear_frame)

    def disappear(self, disappear_frame = None, animate = False):
        #This override allows drops to fall away after the collision objects
        #go away, rather than just disappearing.
        if animate == True:
            raise Warning("RainBobjects are currently designed to not be animated")

        #Make emitter and raindrop last longer
        if disappear_frame != None:
            objs = [x for x in self.subbobjects if x.name == 'emitter']
            for obj in objs:#[self.emitter, self.raindrop]:
                obj.disappear(disappear_frame = disappear_frame + 100, animate = False)
                obj.ref_obj.parent = None
                obj.superbobject = None
                self.subbobjects.remove(obj)

            #Make drops fall through hidden collision_objects, which seem to
            #still take part in physics.
            for obj in self.collision_objects:
                col = obj.collision
                col.keyframe_insert(data_path = 'permeability', frame = disappear_frame - 1)
                col.permeability = 1
                col.keyframe_insert(data_path = 'permeability', frame = disappear_frame)

        super().disappear(disappear_frame = disappear_frame, animate = animate)

    def make_it_rain(self):
        emitter_container = import_object('xzplane', 'primitives', name = 'emitter')
        #emitter_container.ref_obj.parent = self.ref_obj
        self.add_subbobject(emitter_container)
        emitter_container.ref_obj.children[0].location = (0, 12, 0)
        emitter_container.ref_obj.children[0].scale = (16, 16, 16)

        emitter = emitter_container.ref_obj.children[0]
        #A bit hacky, but this method links the emitter object to the scene,
        #changes settings, and then unlinks the emitter object. The normal flow
        #with bobjects is to set everything up, then link the object(s) to the
        #scene, but this particular emitter uses fluid physics for the particle
        #system, which needs to be linked to the scene to update settings.
        bpy.context.scene.objects.link(emitter)
        emitter.scale[2] = 1/160
        #self.emitter = emitter #Used to override add_to_blender()

        mod = emitter.modifiers.new("ParticleSystem", type = 'PARTICLE_SYSTEM')
        psys = mod.particle_system
        psys.seed = random() * 10000
        stngs = psys.settings

        #Could improve this by making rain density a constant and setting count
        #based on that density and that duration
        if RENDER_QUALITY == 'high':
            stngs.count = 30000
        else:
            stngs.count = 1000
        stngs.lifetime = self.stop_raining - self.start_raining
        #Stop emitting drops in time to have them all run out by the end frome
        fall_time = 55 #probably make this an arg when generalizing
        stngs.frame_end = self.stop_raining - fall_time #+ self.appear_frame
        stngs.frame_start = self.start_raining
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

        obj = bpy.context.object

    def add_collision_objects(self, collision_bobjects, text = False, frame = 0):
        objects = []
        new_objects = []
        if text == True:
            for bobj in collision_bobjects:
                #intentionally don't append the object itself, (only descendants)
                #since for text, it's a hidden reference object
                #append_descendants(obj, objects)
                objects.append(bobj.ref_obj.children[0])

            #objects = [x for x in objects if x.type == 'CURVE']
            #The above line is a bit of a hack to make this work now that chars
            #are bobjects. Seems okay.

            scn = bpy.context.scene
            scn.frame_set(frame)

            for obj in objects: #Skip the reference character if text
                obj.data.extrude = 0.1
                new_mesh = obj.to_mesh(scn, True, 'PREVIEW')
                new_obj = bpy.data.objects.new('collision', new_mesh)
                obj.data.extrude = 0
                #new_obj.parent = self.ref_obj
                new_bobj = Bobject(objects = [new_obj])
                self.subbobjects.append(new_bobj)
                #This intentionally avoids the method add_subbobject() because
                #the new bobject's parent should be the same as the original
                #bobject, allowing animations to affect the collision objects.
                new_bobj.ref_obj.parent = obj.parent.parent
                new_bobj.ref_obj.matrix_local = obj.parent.matrix_local

                new_obj.modifiers.new("CollisionSettings", type = 'COLLISION')
                new_obj.collision.damping_factor = 0.8
                new_obj.collision.damping_random = 0.5
                new_objects.append(new_obj)

        else:
            raise Warning("Collision objects not implemented for non-text")
        self.collision_objects = new_objects
        bpy.data.scenes[0].update()
