import bpy
import collections

def clear_blender():
    print('Clearing Blender data')
    for bpy_data_iter in (
                bpy.data.objects,
                bpy.data.meshes,
                bpy.data.lamps,
                bpy.data.cameras,
                bpy.data.curves,
                bpy.data.materials,
                bpy.data.particles,
                bpy.data.worlds
                ):

        for id_data in bpy_data_iter:
            bpy_data_iter.remove(id_data)

    #bpy.ops.wm.read_homefile(use_empty=True)
    #bpy.context.scene.update()

if __name__ == '__main__':
    clear_blender()
