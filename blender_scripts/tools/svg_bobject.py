import imp
from copy import deepcopy
import winsound

import sys
sys.path.append('C:\\Users\\justi\\Documents\\CodeProjects\\Primer\\blender_scripts')

import bobject
imp.reload(bobject)
from bobject import *

import constants
imp.reload(constants)
from constants import *

import helpers
imp.reload(helpers)
from helpers import *


class SVGBobject(Bobject):
    """docstring for ."""
    def __init__(self, *filenames, **kwargs):
        super().__init__(**kwargs)

        if 'vert_align_centers' in kwargs:
            self.vert_align_centers = kwargs['vert_align_centers']
        else:
            self.vert_align_centers = False

        if RENDER_QUALITY == 'medium' or RENDER_QUALITY == 'high':
            default_transition_type = 'morph'
        else:
            default_transition_type = 'instant'
        self.transition_type = self.get_from_kwargs('transition_type', default_transition_type)
        self.lazy_morph = self.get_from_kwargs('lazy_morph', True)
        self.min_length = self.get_from_kwargs('min_length', 1)

        self.get_file_paths(filenames)
        self.import_svg_data()
        self.align()
        if self.transition_type == 'morph':
            print("Making morph chains")
            self.make_morph_chains()
            print("Processing morph chains")
            self.process_morph_chains() #Add splines and points for centering
                                        #and smooth morphing
            print("Making rendered curve objects")
            self.make_rendered_curve_bobjects()
            self.make_lookup_table()

        elif self.transition_type == 'instant':
            self.rendered_bobject_lists = []
            for svg in self.paths:
                rendered_bobject_list = []
                for curve in self.imported_svg_data[svg]['curves']:
                    new_curve = curve.ref_obj.children[0].copy()
                    new_curve.data = curve.ref_obj.children[0].data.copy()
                    apply_material(new_curve, 'color5')
                    new_curve_bobj = bobject.Bobject(
                        objects = [new_curve],
                        location = curve.ref_obj.location
                    )
                    rendered_bobject_list.append(new_curve_bobj)
                self.rendered_bobject_lists.append(rendered_bobject_list)
            self.make_lookup_table()


        print("SVG Bobject initialized")

        self.copyable_null = None

    def add_to_blender(self, **kwargs):
        if 'appear_mode' in kwargs:
            appear_mode = kwargs['appear_mode']
        else:
            appear_mode = 'per_curve'

        if self.transition_type == 'instant':
            initial_shape = self.rendered_bobject_lists[0]
            for bobj in initial_shape:
                self.add_subbobject(bobj)
            super().add_to_blender(**kwargs)
            for shape in self.rendered_bobject_lists[1:]:
                for bobj in shape:
                    bobj.ref_obj.parent = self.ref_obj
                    bobj.superbobject = self

        else:
        #This part is a bit fragile because it assumes appear_frame is in kwargs
            if appear_mode == 'per_curve':
                #Bobject appears early but with each curve at size zero, then
                #the curves morph to non-zero size, making it look like the
                #curves appear independently.
                kwargs['appear_frame'] -= DEFAULT_MORPH_TIME
                if 'subbobject_timing' in kwargs:
                    if isinstance(kwargs['subbobject_timing'], list):
                        for time in kwargs['subbobject_timing']:
                            time += DEFAULT_MORPH_TIME
                else:
                    kwargs['subbobject_timing'] = DEFAULT_MORPH_TIME

            if 'transition_time' in kwargs:
                transition_time = kwargs['transition_time']
            else:
                transition_time = DEFAULT_MORPH_TIME

            super().add_to_blender(**kwargs)
            self.morph_figure(
                0,
                start_frame = kwargs['appear_frame'] + DEFAULT_MORPH_TIME,
                duration = transition_time
            )

    def disappear(self, **kwargs):
        if 'disappear_mode' in kwargs:
            disappear_mode = kwargs['appear_mode']
        else:
            disappear_mode = 'per_curve'

        if disappear_mode == 'per_curve' and \
            self.transition_type == 'morph':
            #Bobject appears early but with each curve at size zero, then
            #the curves morph to non-zero size, making it look like the
            #curves appear independently.
            for bobj in self.rendered_curve_bobjects:
                bobj.disappear(disappear_frame = kwargs['disappear_frame'])
            kwargs['disappear_frame'] += DEFAULT_MORPH_TIME
            super().disappear(**kwargs)
        else:
            super().disappear(**kwargs)

    def make_rendered_curve_bobjects(self):
        null = new_null_curve(
            parent = self.ref_obj,
            location = self.ref_obj.location,
            rotation = self.ref_obj.rotation_euler,
            color = 'color5'
        )

        #print("Max spline count is " + str(max_spline_count))
        equalize_spline_count(null.objects[0], self.max_spline_count)
        bpy.context.scene.objects.link(null.objects[0])
        add_points_to_curve_splines(null.objects[0], total_points = self.max_point_count)
        bpy.context.scene.objects.unlink(null.objects[0])

        self.rendered_curve_bobjects = []
        for i in range(len(self.morph_chains)):
            #Would just deepcopy null, but that doesn't work on Blender data blocks
            dup = null.ref_obj.children[0].copy()
            dup.data = null.ref_obj.children[0].data.copy()
            apply_material(dup, 'color5')
            rendered_curve = bobject.Bobject(objects = [dup], name = 'rendered')
            rendered_curve.ref_obj.location = \
                                self.morph_chains[i][0].ref_obj.location
            rendered_curve.ref_obj.rotation_euler = \
                                self.morph_chains[i][0].ref_obj.rotation_euler

            self.add_subbobject(rendered_curve)
            self.rendered_curve_bobjects.append(rendered_curve)

    def make_lookup_table(self):
        print('Making lookup table')
        if self.transition_type == 'morph':
            #This function makes it easier to find the bobjects associated with
            #individual curves/characters when coding a scene. This would otherwise
            #be hard because the imported curves are copied and mixed into morph
            #chains.
            self.lookup_table = []
            for curve_list in self.lists_of_copies:
                self.lookup_table.append([])
                for cur in curve_list:
                    #Find the morph chain where cur appears and add the
                    #corresponding rendered curve to self.lookup_table[-1].
                    for i, chain in enumerate(self.morph_chains):
                        if cur in chain:
                            self.lookup_table[-1].append(self.rendered_curve_bobjects[i])
                            break
        elif self.transition_type == 'instant':
            self.lookup_table = self.rendered_bobject_lists
        else:
            raise Warning('Lookup table not defined for transition type: ' + \
                                                    str(self.transition_type))

    def import_svg_data(self):
        self.imported_svg_data = {} #Build dictionary of imported svgs to use
                                    #shape keys later and to avoid duplicate
                                    #imports
        for path in self.paths:
            #Import svg and get list of new curves in Blender
            if path not in self.imported_svg_data.keys():
                #This is a dict of dicts for metadata, e.g., center and length
                #of tex expressions
                self.imported_svg_data[path] = {'curves' : []}

                previous_curves = [x for x in bpy.data.objects if x.type == 'CURVE']
                bpy.ops.import_curve.svg(filepath = path)
                new_curves = [x for x in bpy.data.objects if \
                                x.type == 'CURVE' and x not in previous_curves]

                #Arrange new curves relative to tex object's ref_obj
                scale_up = TEX_LOCAL_SCALE_UP #* self.scale[0]

                for curve in new_curves:
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

                    bpy.ops.object.select_all(action = 'DESELECT')
                    curve.select = True
                    bpy.ops.object.origin_set(type = "ORIGIN_GEOMETRY")

                    #This partis just meant for tex_objects

                    if self.vert_align_centers == True:
                        loc = curve.location
                        new_y = new_curves[0].location[1]
                        bpy.context.scene.cursor_location = (loc[0], new_y, loc[2])
                        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')

                    curve.select = False

                    bpy.context.scene.objects.unlink(curve)

                self.imported_svg_data[path]['curves'] = new_curves

        #Make imported curve objects into bobjects
        for svg in self.imported_svg_data:
            for i, curve in enumerate(self.imported_svg_data[svg]['curves']):
                curve_bobj = bobject.Bobject(objects = [curve])
                #Make the bobject's ref_obj handle location
                curve_bobj.ref_obj.location = curve.location
                curve.location = [0, 0, 0]

                #curve_bobj.add_to_blender(appear_frame = 0)

                self.imported_svg_data[svg]['curves'][i] = curve_bobj

                #self.add_subbobject(curve_bobj)

        #print(self.imported_svg_data)
        bpy.context.scene.update()

    def align(self):
        pass
        #Implemented by subclass

    def get_file_paths(self, filenames):
        self.paths = []
        for name in filenames:
            path = os.path.join(
                SVG_DIR,
                name
            ) + ".svg"
            if not os.path.exists(path):
                raise Warning("Could not find " + name + ".svg")
            self.paths.append(path)

    def make_morph_chains(self):
        #Need to copy curves to avoid reusing them when looping and linking into
        #chains below
        self.lists_of_copies = []
        for path in self.paths:
            copies = []
            for curve in self.imported_svg_data[path]['curves']:
                obj = curve.ref_obj.children[0].copy()
                obj.data = curve.ref_obj.children[0].data.copy()
                bobj = bobject.Bobject(
                    objects = [obj],
                    location = curve.ref_obj.location,
                    rotation_euler = curve.ref_obj.rotation_euler,
                    name = 'curve_copy')
                copies.append(bobj)
            self.lists_of_copies.append(copies)

        self.morph_chains = []
        for i, path in enumerate(self.paths):
            print("Adding curves to morph chains for shape " + str(i + 1) + " of " + str(len(self.paths)))
            #print()
            #print('######################################################')
            #print('### Morph chains round  ' + str(i) + ' ####################')
            #print('######################################################')
            #print()
            try:
                #initial = self.imported_svg_data[self.paths[i]]['curves']
                #final = self.imported_svg_data[self.paths[i + 1]]['curves']
                initial = self.lists_of_copies[i]
                final = self.lists_of_copies[i + 1]
            except:
                if i + 1 == len(self.paths):
                    #If there's just one path, add the corresponding curves to
                    #self.morph_chains so the first figure can still be
                    #morphed to.
                    if i == 0:
                        for j in range(len(initial)):
                            self.morph_chains.append([initial[j]])
                    #print("That's the last one!")
                    break
                else:
                    raise Warning('Something went wrong in make_morph_chains')

            if self.lazy_morph == True:
                destinations = self.find_lazy_morph_plan(initial, final)
                #For convenience, get inverse of destinations, caleed 'sources',
                #which is from the perspective of the 'final' expression.
                sources = []
                for j in range(len(final)):
                    if j in destinations:
                        sources.append(destinations.index(j))
                    else:
                        sources.append(None)
            else:
                #length = max(len(initial), len(final))
                while len(initial) < len(final):
                    null_curve = new_null_curve(
                        parent = initial[-1].ref_obj.parent,
                        location = initial[-1].ref_obj.location,
                        rotation = initial[-1].ref_obj.rotation_euler
                    )
                    initial.append(null_curve)
                while len(final) < len(initial):
                    null_curve = new_null_curve(
                        parent = final[-1].ref_obj.parent,
                        location = final[-1].ref_obj.location,
                        rotation = final[-1].ref_obj.rotation_euler
                    )
                    final.append(null_curve)
                destinations = range(len(initial))
                sources = destinations

            #print('Destinations and sources before pairing:')
            #print(' Destinations', destinations)
            #print(' Sources', sources)
            #print()

            #print("  Adding curves to chains")
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
                    #curves without a source will look forward to try to
                    #pair with a curve that has no source, but won't jump past
                    #other curves with sources.
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
                #bpy.context.scene.update()

            #print('Destinations and sources after source -> dest match:')
            #print(' Destinations', destinations)
            #print(' Sources', sources)
            #print()

            #print("  Adding null curves for destination-less curves")
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
                        loc_cur = final[k]
                    else:
                        loc_cur = final[j]

                    #print("Discontinuing chain ")

                    null_curve = new_null_curve(
                        parent = final[0].ref_obj.parent,
                        location = loc_cur.ref_obj.location,
                        rotation = loc_cur.ref_obj.rotation_euler
                        #reuse_object = self.reusable_empty_curve
                    )
                    self.add_to_or_make_morph_chain(i, cur, null_curve)

            #print("  Adding null curves for sourceless curves")
            #If sources[j] is still None after trying to pair final[j] with
            #a source, just insert a zero-size curve for final[j] to morph from.
            for j, src in enumerate(sources):
                if src == None:
                    cur = final[j]
                    if j > 0:
                        k = j
                        while k >= len(initial):
                            k -= 1
                        loc_cur = initial[k]
                    else:
                        loc_cur = initial[j]

                    #Make the null curve if i == 1, because that means the curve
                    #to morph from is one that is actually rendered. Otherwise,
                    #reuse the reusable empty curve.
                    '''if i == 1:
                        reuse = None
                    else:
                        pass'''
                        #reuse = self.reusable_empty_curve
                    #bpy.context.scene.update()
                    null_curve = new_null_curve(
                        parent = initial[0].ref_obj.parent,
                        location = loc_cur.ref_obj.location,
                        rotation = loc_cur.ref_obj.rotation_euler
                        #reuse_object = reuse
                    )
                    #self.expressions[0]['curves'].append(null_curve)
                    #print(i)
                    self.add_to_or_make_morph_chain(i, null_curve, cur)


            '''print(destinations)
            print(sources)
            print()'''
            #print("  Okay, done with that chain")

        print("  Adding null curves to extend chains")
        #Make sure all the chains are the same length. Relevant, e.g., if
        #a char in the first expression disappears in the second expression,
        #and a third expression exists. We need to extend the chain of
        #zero-size curves to keep later functions from tripping.
        chain_length = 0
        for chain in self.morph_chains:
            chain_length = max(len(chain), chain_length)
        for chain in self.morph_chains:
            while len(chain) < chain_length:
                null_curve = new_null_curve(
                parent = final[0].ref_obj.parent,
                location = chain[-1].ref_obj.location,
                rotation = chain[-1].ref_obj.rotation_euler
                #reuse_object = self.reusable_empty_curve
                )
                chain.append(null_curve)
                #self.add_to_or_make_morph_chain(i, chain[-1], null_curve)

        #Print chain info
        '''for i, chain in enumerate(self.morph_chains):
            print(
                "Chain " + str(i + 1) + " of " + str(len(self.morph_chains)) + \
                " which are each of length " + str(len(chain))
            )
            chain = [x.ref_obj.children[0].name for x in chain]
            print(chain)'''

    def add_to_or_make_morph_chain(self, index, char1, char2):
        for chain in self.morph_chains:
            if char1 == chain[-1]:
                chain.append(char2)
                '''if 'null' in char2.name:
                    chain_index = self.morph_chains.index(chain)
                    print('Discontinuing chain ' + str(chain_index) + \
                          ' after inserting null curve at index ' + str(index + 1))
                    chain_names = [x.ref_obj.children[0].name for x in chain]
                    print(chain_names)'''
                if len(chain) != index + 2:
                    raise Warning("Chain lengths messed up")
                return
        #If that doesn't exit the function, we have a new chain
        working_chain = []
        scavenged = False
        #Scavenge for dropped chains that have ended near the right location
        for chain in self.morph_chains:
            if len(chain) <= index:
                working_chain = chain
                scavenged = True
                chain_index = self.morph_chains.index(chain)
                print("Scavenged chain")
                break
        for i in range(len(working_chain), index):
            #-1 because we're actually adding two curves to the chain, so the
            #chain will have length equal to index + 1 at the end of this.
            null_curve = new_null_curve(
                parent = self.ref_obj,
                location = char1.ref_obj.location,
                rotation = char1.ref_obj.rotation_euler
                #reuse_object = self.reusable_empty_curve
            )
            working_chain.append(null_curve)
        working_chain.append(char1)
        working_chain.append(char2)
        if scavenged == False:
            #print("A new chain, which means a curve had no source ")
            self.morph_chains.append(working_chain)

        if len(working_chain) != index + 2:
            raise Warning("Chain lengths messed up")

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

    def process_morph_chains(self):
        self.max_spline_count = 0
        self.max_point_count = CONTROL_POINTS_PER_SPLINE
        for chain in self.morph_chains:
            for link in chain:
                spline_count = len(link.ref_obj.children[0].data.splines)
                self.max_spline_count = max(spline_count, self.max_spline_count)
                for spline in link.ref_obj.children[0].data.splines:
                    point_count = len(spline.bezier_points)
                    self.max_point_count = max(point_count, self.max_point_count)


        #print(self.max_spline_count)

        self.prep_log = []
        count = 0
        for chain in self.morph_chains:
            count += 1
            print('Processing morph chain ' + str(count) + ' of ' + str(len(self.morph_chains)))
            for link in chain:
                already_processed = False
                #cur = link.ref_obj.children[0]
                '''for entry in self.prep_log:
                    if are_chars_same(link.ref_obj.children[0], entry[0]):
                        already_processed = True

                        #Out with the old
                        old = link.ref_obj.children[0]
                        try:
                            link.objects.remove(old)
                        except:
                            pass

                        old.parent = None

                        #In with the new
                        new = entry[1].copy()
                        new.data = entry[1].data.copy()
                        new.parent = link.ref_obj
                        link.objects.append(new)

                        break'''

                if already_processed == False:
                    #print("Processing new curve")
                    #entry = []
                    #unprocessed = link.ref_obj.children[0].copy()
                    #unprocessed.data = link.ref_obj.children[0].data.copy()
                    #bpy.context.scene.objects.link(unprocessed)
                    #entry.append(unprocessed)
                    equalize_spline_count(link.ref_obj.children[0], self.max_spline_count)
                    bpy.context.scene.objects.link(link.ref_obj.children[0])
                    #for spline in link.ref_obj.children[0].data.splines:
                    #    print('There were ' + str(len(spline.bezier_points)))
                    add_points_to_curve_splines(link.ref_obj.children[0], total_points = self.max_point_count)
                    bpy.context.scene.objects.unlink(link.ref_obj.children[0])
                    #for spline in link.ref_obj.children[0].data.splines:
                    #    print('Now there are ' + str(len(spline.bezier_points)))

                    #processed = link.ref_obj.children[0].copy()
                    #processed.data = link.ref_obj.children[0].data.copy()

                    #entry.append(processed)
                    #self.prep_log.append(entry)

    def morph_figure(
        self,
        final_index,
        start_frame = 0,
        duration = DEFAULT_MORPH_TIME
    ):
        print('Morphing ' + self.ref_obj.name + ' to shape ' + str(final_index + 1) + \
                ' of ' + str(len(self.paths)))
        #duration = 60
        end_frame = start_frame + duration
        morph_pairs = []
        print('Start frame = ' + str(start_frame))
        print('End frame = ' + str(end_frame))

        if self.transition_type == 'morph':
            for curve, chain in zip(self.rendered_curve_bobjects, self.morph_chains):
                morph_pairs.append([curve, chain[final_index]])

            for char1, char2 in morph_pairs:
                char1 = char1.objects[0]
                char2 = char2.objects[0]
                self.morph_curve(char1, char2)
                #Keyframes
                #Character location relative to parent
                #This ensures preservation of overall expression arrangement
                char1.parent.keyframe_insert(data_path = "location", frame = start_frame)
                char1.parent.location = char2.parent.location
                char1.parent.keyframe_insert(data_path = "location", frame = end_frame)

                char1.parent.keyframe_insert(data_path = "rotation_euler", frame = start_frame)
                char1.parent.rotation_euler = char2.parent.rotation_euler
                char1.parent.keyframe_insert(data_path = "rotation_euler", frame = end_frame)

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

        else:
            initial = self.rendered_bobject_lists[final_index - 1]
            for bobj in initial:
                bobj.disappear(
                    animate = False,
                    disappear_frame = start_frame
                )
            final = self.rendered_bobject_lists[final_index]
            for bobj in final:
                bobj.add_to_blender(
                    animate = False,
                    appear_frame = start_frame
                )

    def add_morph_shape_keys(self, initial, final):
        if len(initial.data.splines) != len(final.data.splines):
            #winsound.MessageBeep(type = MB_ICONEXCLAMATION)
            print("#" + str(initial.name) + " has " + str(len(initial.data.splines)) + \
                        " splines and " + str(final.name) + " has " + \
                        str(len(final.data.splines)) + " splines, which is not the same number.")
            print("#This means something went wrong when processing morph chains.")
            print('#I gotchu this time, but you might wanna take a look back and fix the underlying issue.')
            if len(initial.data.splines) < len(final.data.splines):
                raise Warning("Oh dang. I actually don't gotchu. The rendered " + \
                                "curve is missing splines, I think.")

            bpy.context.scene.objects.link(final)
            equalize_spline_count(final, self.max_spline_count)
            add_points_to_curve_splines(final)
            bpy.context.scene.objects.unlink(final)

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

        #This might be a bit confusing, caused by the fact that I mixed up
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
                print('#' + str(initial.name) + " has " + str(len(initial_points)) + \
                        " points in spline " + str(i+1) + " and " + \
                        str(final.name) + " has " + str(len(final_points)) + \
                        " points in spline " + str(i+1) + \
                        " which is not the same number.")
                print("#This means something went wrong when processing morph chains.")
                print('#I gotchu this time, but you might wanna take a look back and fix the underlying issue.')
                if len(initial_points) < len(final_points):
                    raise Warning("Oh dang. I actually don't gotchu. The rendered " + \
                                    "curve is missing points, I think.")

                bpy.context.scene.objects.link(final)
                add_points_to_curve_splines(final)
                bpy.context.scene.objects.unlink(final)

            #Assign final_points values to initial_points
            for j in range(len(initial_points)):
                initial_points[j].co = final_points[j].co
                initial_points[j].handle_left = final_points[j].handle_left
                initial_points[j].handle_right = final_points[j].handle_right


        bpy.ops.object.mode_set(mode = 'OBJECT')
        if was_hidden:
            initial.hide = True

    def morph_curve(self, initial, final):
        #equalize_spline_count(initial, final)
        char_set = [initial, final]
        for char in char_set:
            for spline in char.data.splines:
                reindex_to_top_point(spline)
            #add_points_to_curve_splines(char, CONTROL_POINTS_PER_SPLINE)
        self.add_morph_shape_keys(initial, final)

class SVGFromBlend(SVGBobject):
    def __init__(self, *filenames, **kwargs):
        super().__init__(*filenames, **kwargs)

    def get_file_paths(self, filenames):
        #Should just be one file for SVGFromBlend, prepping to import.
        #Might be multiple strings in the format helpers.import_object takes
        self.paths = list(filenames)

    def import_svg_data(self):
        #import from the .blend file and add curves to self.imported_svg_data,
        #mimicking the data structure of regular svg bobjects
        paths = self.paths
        self.imported_svg_data = {}

        #For this type of object, the path list items are lists, which can
        #have multiple strings to feed to import_objects()
        for i, path in enumerate(paths):
            name = str(path)
            self.imported_svg_data[name] = {'curves' : []}
            new_curve_bobj = self.import_and_modify_curve(i, path)
            #self.modify_curves(new_curve_bobj.ref_obj.children[0].children[0])
            #self.modify_curves()

            new_curves = []
            #These will all have container objects because they were likely
            #made as regular svgbobjects the first time, so just take the actual
            #curves.
            for obj in new_curve_bobj.ref_obj.children:
                new_curves.append(obj.children[0])

            #self.imported_svg_data[name]['curves'] = new_curves

            #After calling import_objects(), it's best for paths to not be lists
            #for i in range(len(self.paths)):
            #    self.paths[i] = str(self.paths[i])

            for j, curve in enumerate(new_curves):
                curve_bobj = bobject.Bobject(objects = [curve])
                #Make the bobject's ref_obj handle location
                curve_bobj.ref_obj.location = curve.location
                curve.location = [0, 0, 0]
                curve_bobj.ref_obj.rotation_euler = curve.rotation_euler
                curve.rotation_euler = [0, 0, 0]

                self.imported_svg_data[name]['curves'].append(curve_bobj)

        print(self.imported_svg_data)
        print(self.paths)

    def import_and_modify_curve(self, index, path):
        #This just imports a curve and returns it
        #Extemded by subclass
        #index is needed for subclass implementation to know which curve it's
        #modifying.
        new_curve_bobj = import_object(*path)
        return new_curve_bobj


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

def get_spline_length(spline):
    points = spline.bezier_points
    length = 0
    for j in range(len(points)):
        k = (j + 1) % len(points)
        sep = points[k].co - points[j].co
        length += sep.length
    return length

def new_null_curve(
    parent = None,
    location = None,
    rotation = None,
    color = 'color5',
    reuse_object = None
):
    #print("    Adding null curve")

    #if reuse_object == None:
    data = bpy.data.curves.new(name = 'no_curve_data', type = 'CURVE')
    obj = bpy.data.objects.new(name = 'no_curve', object_data = data)
    #else:
    #    print('Reusing object!!!!!!')
    #    obj = reuse_object

    bobj = bobject.Bobject(objects = [obj], name = 'null')
    #obj.parent = bobj.ref_obj
    #bobj.objects.append(obj)

    bobj.ref_obj.parent = parent
    #print(matrix_local)
    bobj.ref_obj.location = location
    bobj.ref_obj.rotation_euler = rotation
    #print(bobj.ref_obj.matrix_local)
    #bpy.context.scene.objects.link(new_null)
    #if reuse_object == None:
    #    bobj.add_to_blender(animate = False)

    #apply_material(obj, color)
    #bpy.data.scenes[0].update()

    #print('    Done adding null curve')

    return bobj

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

def are_chars_same(char1, char2):
    splines1 = char1.data.splines
    splines2 = char2.data.splines
    if len(splines1) != len(splines2):
        return False
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

def main():

    print_time_report()


if __name__ == "__main__":
    main()
