#This script is a place for me to run random code with the script runner addon
#https://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/Import-Export/Script_Runner


from helpers import *
from constants import *
import tex_bobject

#primer = import_object('logo')
#primer.add_to_blender(appear_frame = 0)

define_materials()

yt = tex_bobject.TexBobject(
    '\\xcancel{B} + N \\times R = N \\times D'
)
yt.add_to_blender(appear_frame = 0)
