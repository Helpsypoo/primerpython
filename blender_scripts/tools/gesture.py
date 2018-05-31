import math
from svg_bobject import SVGFromBlend
from helpers import *

class Gesture(SVGFromBlend):
    """This is convoluted and everything is named horribly. My bad."""
    def __init__(
        self,
        gesture_series = None,

        **kwargs
    ):

        self.gesture_series = gesture_series
        if self.gesture_series == None:
            raise Warning('Hey, you need to define the gesture objects')

        paths = []
        for i, gesture in enumerate(self.gesture_series):
            if gesture['type'] == 'bracket':
                paths.append('bracket ' + str(i))

        #self.annotation_point = list(gesture['points']['annotation_point'])
        #self.left_point = list(gesture['points']['left_point'])
        #self.right_point = list(gesture['points']['right_point'])

        #self.process_points()

        #TODO: Fix the fact that passing a name to an SVGFromBlend object
        #breaks things.
        #if 'name' not in kwargs:
        #    kwargs['name'] = 'bracket'
        super().__init__(*paths, **kwargs)

        self.curve = self.ref_obj
        print(self.ref_obj.name)

    def process_points(self, gesture):
        #Vectors and lengths from points
        width_vec = add_lists_by_element(gesture['points']['right_point'],
                                        gesture['points']['left_point'],
                                        subtract = True)
        #print(width_vec)
        width_unit_vec = get_unit_vec(width_vec)
        width = vec_len(width_vec)
        #print("Width unit vec length, which should be 1, is " + str(vec_len(width_unit_vec)))
        left_to_top_vec = add_lists_by_element(gesture['points']['annotation_point'],
                                               gesture['points']['left_point'],
                                               subtract = True)
        left_to_top = vec_len(left_to_top_vec)

        #Rotation
        angle = math.atan2(width_vec[1], width_vec[0])
        #self.ref_obj.rotation_euler = [0, 0, angle]

        #Extend arms/stem
        default_left_length = 1.3689 #Distance between prong points in bracket.blend
        left_length = dot_product(width_unit_vec, left_to_top_vec)
        left_extension = left_length - default_left_length
        #print("Left extension: " + str(self.left_extention))
        #Might warp the bracket if arms are too short.

        default_right_length = 1.3688
        right_length = width - left_length
        right_extension = right_length - default_right_length

        default_height = 1
        height = math.sqrt(left_to_top ** 2 - left_length ** 2)
        height_extension = height - default_height

        return {
                    'angle': angle,
                    'left_extension': left_extension,
                    'right_extension': right_extension,
                    'height_extension': height_extension
                }

    def deform(self, curve, params):
        #curve = self.ref_obj.children[0].children[0]
        #curve = self.imported_svg_data[self.paths[0]]['curves'][0].ref_obj.children[0]
        #curve = self.morph_chains[0][0].ref_obj.children[0]
        points = curve.data.splines[0].bezier_points
        for i in range(4, 11): #Happens to be the points on the left arm
            point = points[i]
            point.co[0] -= params['left_extension']
            point.handle_left[0] -= params['left_extension']
            point.handle_right[0] -= params['left_extension']

        for i in range(15, 20): #Happens to be the points on the right arm
            point = points[i]
            point.co[0] += params['right_extension']
            point.handle_left[0] += params['right_extension']
            point.handle_right[0] += params['right_extension']

        for i in range(1, 23): #Happens to be the points on the right arm
            point = points[i]
            point.co[1] -= params['height_extension']
            point.handle_left[1] -= params['height_extension']
            point.handle_right[1] -= params['height_extension']

    def import_and_modify_curve(self, index, path):
        #path is purposely not used by this method, which overrides a method
        #from the super class
        gesture = self.gesture_series[index]

        if gesture['type'] == 'bracket':
            path = ['bracket', 'svgblend']

            new_curve_bobj = import_object(*path)
            params = self.process_points(gesture)
            #print(params)

            ref = new_curve_bobj.ref_obj.children[0]
            curve = ref.children[0]
            curve.rotation_euler = (0, 0, params['angle'])
            curve.location = gesture['points']['annotation_point']
            self.deform(curve, params)


            return new_curve_bobj
