import bpy
import mathutils

import imp
import pickle
import math

import two_d_world
import tex_bobject
import constants

#import alone doesn't check for changes in cached files
imp.reload(two_d_world)
from two_d_world import TwoDWorld
imp.reload(tex_bobject)
imp.reload(constants)
from constants import *

import helpers
imp.reload(helpers)
from helpers import *

import bobject
imp.reload(bobject)
from bobject import *

class DrawnWorld(TwoDWorld, Bobject):
    """docstring for .DrawnWorld"""
    def __init__(
        self,
        name = '',
        location = (0, 0, 0),
        scale = 0,
        appear_frame = 0,
        start_delay = 0,
        duration = DEFAULT_WORLD_DURATION,
        load = None,
        save = False,
        overlap_okay = False,
        initial_creatures = 10,
        gene_updates = [],
        motion_vars = None,
        counter_alignment = 'right_top',
        creature_model = ['boerd_blob', 'creatures', 'boerd_blob_squat', 'creatures']
    ):
        #This is slightly wonky because we want to save instances of
        #TwoDWorld (the parent class), but not instances of DrawnWorld
        #itself.
        #TwoDWorld has data that's randomly generated and independent from
        #exactly how objects appear when rendered in Blender, so it's useful for
        #saving a nice-looking sim.
        #DrawnWorld's additional attributes aren't generated randomly, and
        #They will be manually changed while working on a video, so saving
        #isn't helpful here.
        #Could be that class inheritance isn't worth it here. ¯\_(ツ)_/¯
        self.duration = duration - start_delay
        if load != None:
            self.get_saved_world(load)
        else:
            world = TwoDWorld(
                duration = self.duration, #/2 because of 60 fps vs 30 fps
                overlap_okay = overlap_okay,
                initial_creatures = initial_creatures,
                gene_updates = gene_updates
            )
            self.__dict__ = world.__dict__
            if save == True:
                world.save_sim_result()

        #It is a world. It is a Bobject.
        Bobject.__init__(self,
            location = location,
            scale = scale,
            appear_frame = appear_frame
        )

        #Could make radius more than 1D, but for now, just uses the
        #x component of scale
        #self.world_radius = self.scale[0] * self.radius #attribute of TwoDWorld
        self.start_frame = self.appear_frame + start_delay
        #self.disappear_frame = self.start_frame + self.duration

        self.info = []
        self.counter_frames_lists = []
        #I kind of hate the above line, but it was the easiest way to separate
        #The creation of the python counter object and the morphing of the
        #characters after adding to blender
        self.counter_alignment = counter_alignment
        self.creature_model = creature_model

    def get_saved_world(self, world_file):
        result = os.path.join(
            SIM_DIR,
            world_file
        ) + ".pkl"
        with open(result, 'rb') as input:
            world = pickle.load(input)
        self.__dict__ = world.__dict__
        print("Loaded the world")

    def add_to_blender(self, **kwargs):
        super().add_to_blender(**kwargs)
        self.align_info()
        self.morph_counters()
        self.add_creatures_to_blender()
        self.set_world_keyframes()

    def add_creatures_to_blender(self):
        #Create floor
        plane = import_object(
            'xyplane', 'primitives',
            scale = self.radius,
            location = (0, 0, -0.7),
            name = 'sim_plane'
        )
        #print(plane.ref_obj.scale)
        apply_material(plane.ref_obj.children[0], 'color2')
        self.add_subbobject(plane)
        #plane.ref_obj.parent = self.ref_obj
        #print(plane.ref_obj.scale)
        #plane.superbobject = self
        #self.subbobjects.append(plane)
        plane.add_to_blender(appear_frame = self.appear_frame)

        print("Adding " + str(len(self.creatures)) + " creatures to Blender")
        #creature_cache = []
        for cre in self.creatures:
            cre.reused = False
            cre_needs_bobject = True
            #Assumes creatures are in order of birthday by assuming
            #other_cre.bobject and other_cre.reused exist.
            for other_cre in self.creatures:
                #2 * MATURATION_TIME because that's the minimum length of time
                #for a creature to be animated as it's born and then dies
                if other_cre != cre and \
                other_cre.deathday + MATURATION_TIME < cre.birthday and \
                other_cre.alleles == cre.alleles and \
                other_cre.reused == False:
                    cre.bobject = other_cre.bobject
                    cre.bobject.add_to_blender(
                        #2 * cre.birthday due to transition from 30 to 60 fps
                        appear_frame = self.start_frame + cre.birthday,
                        is_creature = True
                    )
                    other_cre.reused = True
                    cre_needs_bobject = False
                    print('Hand-me-down for ' + str(cre.name))
                    break
            if cre_needs_bobject == True:
                self.add_creature_to_blender(cre)

        bpy.ops.object.select_all(action='DESELECT')

    def add_creature_to_blender(self, cre):
        size = float(cre.alleles['size']) #* self.scale[0]
        type_req = None #For applying material to only objects of certain type
        if RENDER_QUALITY != 'high':
            if cre.alleles['shape'] == "shape1":
                bobj = import_object('icosphere', 'primitives')
            if cre.alleles['shape'] == "shape2":
                bobj = import_object('torus', 'primitives')
        else:
            model = self.creature_model
            if model == ['boerd_blob', 'creatures', 'boerd_blob_squat', 'creatures']:
                type_req = 'META'
            if cre.alleles['shape'] == "shape1":
                bobj = import_object(model[0], model[1])
            if cre.alleles['shape'] == "shape2":
                bobj = import_object(model[2], model[3])


        #2 * cre.birthday because of change from 30 to 60 fps
        bobj.add_to_blender(
            appear_frame = self.start_frame + cre.birthday,
            is_creature = True
        )
        cre.bobject = bobj
        obj = bobj.ref_obj
        #bpy.context.scene.objects.link(obj)

        if cre.alleles['color'] == 'creature_color_1':
            col = 'creature_color3'
        elif cre.alleles['color'] == 'creature_color_2':
            col = 'creature_color4'

        recursive = True
        if 'stanford_bunny' in self.creature_model:
            recursive = False

        apply_material(obj.children[0], col, recursive = recursive, type_req = type_req)

        obj.parent = self.ref_obj
        #obj.matrix_parent_inverse = obj.parent.matrix_world.inverted()
        print("Added " + str(cre.name))

    def set_world_keyframes(self):
        for cre in self.creatures:
            print("Setting keyframes for " + str(cre.name))
            bobj = cre.bobject
            obj = bobj.ref_obj

            #Set scale to 1 in case cre.bobject is being reused.
            obj.scale = (1, 1, 1)
            #If creature dies right away, animate as if it lasted long enough to
            #finish appearing before dying
            effective_deathday = cre.deathday
            if effective_deathday - cre.birthday < MATURATION_TIME:
                effective_deathday = cre.birthday + MATURATION_TIME
            #MATURATION_TIME / 2 because cre time is in 30 fps
            disappear_frame = self.start_frame + 2 * effective_deathday + MATURATION_TIME
            #Ensure creature disappears in place.
            try:
                obj.location = cre.locations[cre.deathday]
            except:
                obj.location = cre.locations[-1]
            obj.keyframe_insert(data_path = 'location', frame = disappear_frame)
            bobj.disappear(
                disappear_frame = disappear_frame,
                is_creature = True
            )

            for t in range(self.duration):
                if cre.locations and cre.locations[t] != None:

                    #obj.location = mathutils.Vector(translated_loc)
                    obj.location = cre.locations[t]
                    #2 * t because of change from 30 to 60 fps
                    obj.keyframe_insert(data_path="location", frame = t + self.start_frame)

                    #obj.rotation_euler[2] = cre.rotation[t]
                    #obj.keyframe_insert(data_path="rotation_euler", frame = t + self.start_frame)

                    if RENDER_QUALITY == 'high':
                        if self.creature_model == \
                                ['boerd_blob', 'creatures', 'boerd_blob_squat', 'creatures']:
                            if cre.head_angle and cre.head_angle[t] != None:
                                bone = obj.children[0].pose.bones[3]
                                bone.rotation_quaternion = cre.head_angle[t]
                                #2 * t because of change from 30 to 60 fps
                                bone.keyframe_insert(data_path="rotation_quaternion", frame = t + self.start_frame)

    def add_counter(
        self,
        location = 'right_top',
        size = 'any',
        shape = 'any',
        color = 'any',
        average = False,
        label = ''
    ):

        #Counting business
        count_by_time = self.get_creature_count_by_t(size, shape, color)
        if average == True:
            average_by_time = []
            for i in range(len(count_by_time)):
                total = 0
                for j in range(i + 1):
                    total += count_by_time[j]
                avg = total / (i + 1)
                avg = round(avg, 1)
                average_by_time.append(avg)
            count_by_time = average_by_time


        #print("Creating expressions for " + label)
        expressions = ['0']
        expression_frames = [0]
        #Make list of expressions for each time the count changes
        count = -math.inf
        for t in range(self.duration):
            if count_by_time[t] != count:
                count = count_by_time[t]
                expressions.append(str(count))
                expression_frames.append(t)
        self.counter_frames_lists.append(expression_frames)
        #Everything above here could perhaps be moved to morph_counters, since
        #It's all preparing for that.

        label_tex = tex_bobject.TexBobject(label)
        count_tex = tex_bobject.TexBobject(*expressions, transition_type = 'instant')
        #Lazy morphing is too intensive for a counter that switches to many
        #values, and the counting happens too fast for it to be appeciated
        #anyway.
        counter = bobject.TexComplex(
            label_tex, count_tex,
            name = 'sim_counter ' + label
        )

        self.info.append(counter)
        self.subbobjects.append(counter)
        counter.ref_obj.parent = self.ref_obj
        counter.superbobject = self

    def add_info(self, info):
        #Could maybe override the info.append() to prevent it from being done
        #the wrong way.
        self.info.append(info)
        self.subbobjects.append(info)
        info.ref_obj.parent = self.ref_obj
        info.superbobject = self

    def align_info(self, frame = None):
        align = self.counter_alignment
        #Sort out the location
        #num_prev_counters = len(self.info)
        #Will add cases as needed
        locs = []
        for i in range(len(self.info)):
            locs.append([0, 0, 0])
        for i, loc in enumerate(locs):
            if align == 'right_top':
                loc[0] = 8.5
                loc[1] = 7 - i * 1.5 #Could make this sensitive to counter
                                     #scale, but may not be necessary
            elif align == 'top_left':
                loc[0] = -8
                loc[1] = 9
                #bump the previous ones up, since we're aligning to bottom here
                for j in range(i):
                    locs[j][1] += 1.5

        #frame is used when updating info after the drawn_world has been added
        #to blender
        if frame == None:
            for loc, info in zip(locs, self.info):
                info.ref_obj.location = loc
        else:
            for loc, info in zip(locs, self.info):
                if info.ref_obj.name not in bpy.context.scene.objects:
                    info.ref_obj.location = loc
                    info.add_to_blender(appear_frame = frame, animate = True)
                else:
                    info.move_to(
                        new_location = loc,
                        start_frame = frame,
                        end_frame = frame + OBJECT_APPEARANCE_TIME
                    )

    def morph_counters(self):
        for counter, frames in zip(self.info, self.counter_frames_lists):
            count_tex = counter.subbobjects[1] #The second tex_bobject is the counter
            for i in range(1, len(frames)):
                frame = frames[i]
                #morph quickly if there's another animation coming up, otherwise
                #morph over three frames.
                try:
                    morph_duration = frames[i + 1] - frames[i]
                    if morph_duration > 6: #6 is an arbitrary max duration
                        morph_duration = 6
                except: #should only run for the last expression
                    morph_duration = self.duration - frames[i]
                    if morph_duration > 6: #6 is an arbitrary max duration
                        morph_duration = 6

                #"Morphed expression " + str(i)
                #print(count_tex.expressions[i], frame  + self.start_frame, frame + self.start_frame + morph_duration)

                #2 * frame because of change from 30 to 60 fps
                count_tex.morph_figure(
                    i,
                    start_frame = frame  + self.start_frame,
                    duration = morph_duration
                )

    def move_to(self, new_counter_alignment = None, **kwargs):
        super().move_to(**kwargs)
        if 'start_frame' in kwargs:
            start_frame = kwargs['start_frame']
        else:
            if end_frame in kwargs:
                start_frame = kwargs['end_frame'] - OBJECT_APPEARANCE_TIME
            else:
                raise Warning('Need to specify start frame or end frame for move_to')

        if 'end_frame' in kwargs:
            end_frame = kwargs['end_frame']
        else:
            end_frame = start_frame + OBJECT_APPEARANCE_TIME


        if new_counter_alignment != None:
            for counter in self.info:
                counter.ref_obj.keyframe_insert(data_path = 'location', frame = start_frame)
            self.counter_alignment = new_counter_alignment
            self.align_info()
            for counter in self.info:
                counter.ref_obj.keyframe_insert(data_path = 'location', frame = end_frame)
