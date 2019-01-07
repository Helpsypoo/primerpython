import os
import math
import datetime
from copy import deepcopy

'''
Quality
'''
RENDER_QUALITY = 'final'
#'medium' or higher turns on expression morphing
#which takes a few seconds per run
if RENDER_QUALITY == 'final':
    RESOLUTION_PERCENTAGE = 100
    LIGHT_SAMPLING_THRESHOLD = 0.01
    SAMPLE_COUNT = 64
    RENDER_QUALITY = 'high'
    RENDER_TILE_SIZE = 256
    #The 'final' stuff is over, so just setting to 'high' for rest of code
else:
    RESOLUTION_PERCENTAGE = 30
    LIGHT_SAMPLING_THRESHOLD = 0.0 #For my scenes, it seems there's so little
                                   #ray bouncing that the cutoff test actually
                                   #takes longer than letting the light keep going
    SAMPLE_COUNT = 64
    RENDER_TILE_SIZE = 256

if RENDER_QUALITY == 'high':
    LAMPS_TO_A_SIDE = 1
    LAMP_TYPE = 'SUN'
    ICO_SUBDIVISIONS = 6
    CONTROL_POINTS_PER_SPLINE = 50 #TODO: figure out the threshold for noticing a difference
    PARTICLES_PER_MESH = 300000 #Could be smaller if morphing smaller objects
    #Could even be a function of scale
    #Or number of other objects

else:
    LAMPS_TO_A_SIDE = 1
    LAMP_TYPE = 'SUN'
    ICO_SUBDIVISIONS = 2
    CONTROL_POINTS_PER_SPLINE = 30
    PARTICLES_PER_MESH = 1000

    RESOLUTION_PERCENTAGE = 30
    LIGHT_SAMPLING_THRESHOLD = 0.1
    SAMPLE_COUNT = 64

'''
Colorssssss
'''
color_scheme = 2
if color_scheme == 1:
    #Coolors Exported Palette - https://coolors.co/393e41-f3f2f0-3e7ea0-ff9400-e7e247
    COLORS = [
        [57, 62, 65, 1],
        #[211, 208, 203, 1],
        [243, 242, 240, 1],
        [62, 126, 160, 1],
        [255, 148, 0, 1],
        #[232, 225, 34, 1],
        [231, 226, 71, 1],
        #[106, 141, 115, 1]
        [215, 38, 61, 1]
        #[255, 0, 0, 1]
    ]
elif color_scheme == 2: #Main. Why isn't #1 main? Because your face.
    COLORS = [
        #[42, 46, 48, 1], #Three darker than first video
        [47, 51, 54, 1], #Two darker than first video
        #[211, 208, 203, 1],
        [243, 242, 240, 1],
        [62, 126, 160, 1],
        [255, 148, 0, 1],
        #[232, 225, 34, 1],
        [231, 226, 71, 1],
        #[106, 141, 115, 1]
        [214, 59, 80, 1],
        #[255, 0, 0, 1]
        [105, 143, 63, 1],
        [219, 90, 186, 1],
        [145, 146.5, 147, 1] #Gray from averaging 1 and 2
    ]

elif color_scheme == 3:
    #Coolors Exported Palette - coolors.co/191308-bbd8b3-f3b61f-48a0c9-72120d
    COLORS = [
        [1, 33, 31, 1],
        [255, 237, 225, 1],
        [32, 164, 243, 1],
        [255, 51, 102, 1],
        [234, 196, 53, 1],
        [215, 38, 61, 1]
    ]

elif color_scheme == 4: #UCSF
    #https://identity.ucsf.edu/print-digital/digital-colors
    COLORS = [
        [5, 32, 73, 1], #Dark blue
        [255, 255, 255, 1], #White
        [255, 221, 0, 1], #Yellow
        [80, 99, 128, 1], #Light Navy
        [47, 51, 54, 1], #Two darker than first video
        [0, 0, 0, 1], #Black
        [113, 111, 178, 1], #Light purple
        [180, 185, 191, 1], #Dark gray
        [209, 211, 211, 1], #Light gray
    ]

COLORS_SCALED = []
for color in COLORS:
    color_scaled = deepcopy(color)
    for i in range(3):
        color_scaled[i] /= 255
        #color_scaled[i] = color_scaled[i] ** 2.2
    COLORS_SCALED.append(color_scaled)

'''
File and directory constants
'''
MEDIA_DIR = os.path.join(os.path.expanduser('~'), "Documents\\CodeProjects\\Primer")

###
THIS_DIR          = os.path.dirname(os.path.realpath(__file__))
MAIN_DIR          = os.path.join(THIS_DIR, "..")
FILE_DIR          = os.path.join(MAIN_DIR, "files")
TEX_DIR           = os.path.join(FILE_DIR, "tex")
SIM_DIR           = os.path.join(FILE_DIR, "sims")
SVG_DIR           = os.path.join(FILE_DIR, "svg")
IMG_DIR           = os.path.join(FILE_DIR, "raster")
BLEND_DIR         = os.path.join(FILE_DIR, "blend")

for folder in [FILE_DIR, TEX_DIR, SIM_DIR, SVG_DIR, BLEND_DIR]:
    if not os.path.exists(folder):
        os.makedirs(folder)

TEX_TEXT_TO_REPLACE = "YourTextHere"
TEMPLATE_TEX_FILE  = os.path.join(FILE_DIR, "template.tex")

'''
Birth and death constants
'''
#Equilibrium number =
#BIRTH_CHANCE / (DEATH_CHANCE - REPLICATION_CHANCE)
#Different if there's mutation to/from the species

BASE_BIRTH_CHANCE = 0.001
BASE_DEATH_CHANCE = 0.001
BASE_REPLICATION_CHANCE = 0.001 #If this is higher than DEATH_CHANCE,
                                #it can get cray
DEFAULT_MUTATION_CHANCE = 0.5

INITIAL_CREATURES = 10
DEFAULT_POP_CAP = 3000

'''
Sim motion constants
'''
CREATURE_BUBBLE_WIDTH = 0.1
BOUNCE_DAMP_FACTOR = 0.8
FLOOR_PADDING = 1
BLINK_CHANCE = 0.0025
BLINK_LENGTH = 11
BLINK_CYCLE_LENGTH = 1200
#Could make a constant for the velocity parameters

'''
Blob constants
'''
BLOB_VOLUME_DENSITY = 0.04

'''
World constants
'''
DEFAULT_WORLD_DURATION = 100
WORLD_RADIUS = 10

'''
Camera and lighting constants
'''
CAMERA_LOCATION = (0, 0, 32.8)
CAMERA_ANGLE = (0, 0, 0)

'''
Text constants
'''
SPACE_BETWEEN_EXPRESSIONS = 0.1 #For text svgs  #0.45 For actual tex_bobjects
TEX_LOCAL_SCALE_UP = 260 #Value that makes line height about 1 Blender Unit

'''
Animation constants
'''
FRAME_RATE = 60

MATURATION_TIME = 5 #time for a new creature to grow to full scale.
OBJECT_APPEARANCE_TIME = 30
PARTICLE_APPEARANCE_TIME = 1
DEFAULT_MORPH_TIME = OBJECT_APPEARANCE_TIME
MORPH_PARTICLE_SIZE = 0.03
FLOOR_APPEARANCE_TIME = OBJECT_APPEARANCE_TIME #time for floor to appear in a new world
TEXT_APPEARANCE_TIME = OBJECT_APPEARANCE_TIME
DEFAULT_SCENE_DURATION = 150
DEFAULT_SCENE_BUFFER = 0 #This was used when multiple scenes were in blender at
                         #once, which was basically never, and will never be.
                         #Could just delete.

'''
Graph constants
'''
AXIS_WIDTH = 0.05
AXIS_DEPTH = 0.01
ARROW_SCALE = [0.3, 0.3, 0.4]
GRAPH_PADDING = 1
CURVE_WIDTH = 0.04
if RENDER_QUALITY == 'high':
    PLOTTED_POINT_DENSITY = 30
else:
    PLOTTED_POINT_DENSITY = 20
CURVE_Z_OFFSET = 0.01
AUTO_TICK_SPACING_TARGET = 2 #Blender units
HIGHLIGHT_POINT_UPDATE_TIME = OBJECT_APPEARANCE_TIME
