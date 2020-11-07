import bpy
import subprocess
import os
import shutil

from .tools import helpers

overwrite = True

def render_with_skips(start, stop):
    """
    Take start and stop, and render animation only for animated
    frames. Still frames, are substituted into the output folder
    as copies of their equivalents.
    """

    render_range = list(range(start, stop + 1))
    #+1 because range should for frames should be inclusive

    # create JSON like dictionary to store each
    # animated object's fcurve data at each frame.
    all_obj_fcurves = {}
    for obj in bpy.data.objects:
        obj_fcurves = {}

        try:
            obj.animation_data.action.fcurves
        except AttributeError:
            #print("--|'%s' is not animated" % obj.name)
            continue

        #print("\n--> '%s' is animated at frames:" % obj.name)

        for fr in list(range(start,stop+1)):
            fc_evals = [c.evaluate(fr) for c in obj.animation_data.action.fcurves]
            obj_fcurves.update({int(fr): fc_evals})
            #print(fr, end=", ")
        #print()

        all_obj_fcurves.update({obj.name: obj_fcurves})


    # loop through each animated object and find its
    # animated frames. then remove those frames from
    # a set containing all frames, to get still frames.
    fr_prev = None
    still_frames = set(render_range)
    for obj in all_obj_fcurves.keys():
        obj_animated_frames = []
        for i, fr in enumerate(sorted(all_obj_fcurves[obj].keys())):
            if i != 0:
                if all_obj_fcurves[obj][fr] != all_obj_fcurves[obj][fr_prev]:
                    obj_animated_frames.append(fr)
            fr_prev = fr

        still_frames = still_frames - set(obj_animated_frames)

    print("\nFound %d still frames" % len(still_frames))
    print(sorted(still_frames), end="\n\n")


    # render animation, skipping the still frames and
    # filling them in as copies of their equivalents
    filepath = bpy.context.scene.render.filepath

    for fr in render_range:
        exists = False
        if overwrite == False:
            directory = os.fsencode(filepath)
            for file in os.listdir(directory):
                filename = os.fsdecode(file)
                if ('%04d' % fr) in filename:
                    exists = True
        if exists == False:
            if fr not in still_frames or fr == render_range[0]:
                bpy.context.scene.frame_set(fr)
                bpy.context.scene.render.filepath = filepath + '%04d' % fr
                bpy.context.scene.render.use_overwrite = False
                bpy.ops.render.render(write_still=True)
            else:
                scene = bpy.context.scene
                abs_filepath = scene.render.frame_path(scene.frame_current)
                #abs_path = '/'.join(abs_filepath.split('/')[:-1]) + '/'
                print("Frame %d is still, copying from equivalent" % fr)
                scn = bpy.context.scene
                shutil.copyfile(filepath + '%04d.png' % (fr-1), filepath + '%04d.png' % fr)

    bpy.context.scene.render.filepath = filepath

start = bpy.data.scenes['Scene'].frame_start
end = bpy.data.scenes['Scene'].frame_end
render_with_skips(start,end)
helpers.finish_noise()
