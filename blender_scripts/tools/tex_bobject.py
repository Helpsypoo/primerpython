import bpy
import mathutils

import collections
import sys
import os
import imp

import sys
sys.path.append('C:\\Users\\justi\\Documents\\CodeProjects\\Primer\\blender_scripts')

import svg_bobject
imp.reload(svg_bobject)
from svg_bobject import *

import constants
imp.reload(constants)
from constants import *

import helpers
imp.reload(helpers)
from helpers import *

import tex_complex
imp.reload(tex_complex)

import draw_scenes

import clear

class TexBobject(SVGBobject):
    def __init__(self, *expressions, typeface = 'default', **kwargs):
        self.kwargs = kwargs
        self.centered = self.get_from_kwargs('centered', False)

        self.typeface = typeface

        if 'vert_align_centers' not in kwargs:
            kwargs['vert_align_centers'] = True

        if 'name' not in kwargs:
            kwargs['name'] = 'tex'

        #paths = get_svg_file_paths(expressions)
        super().__init__(*expressions, **kwargs)
        #self.active_expression_path = self.paths[0]
        self.annotations = []
        #self.align()

    def get_figure_curves(self, fig):
        if fig == None:
            return self.imported_svg_data[fig]['curves']
        else:
            return self.imported_svg_data[fig]['curves'][1:]

    def align_figure(self, fig):
        curve_list = super().align_figure(fig)
        #Get rid of reference H after alignment is done
        if fig == None:
            self.imported_svg_data[fig]['curves'] = curve_list
        else:
            self.imported_svg_data[fig]['curves'] = curve_list[1:]

    def morph_figure(
        self,
        final_index,
        start_time = None,
        start_frame = None,
        duration = DEFAULT_MORPH_TIME,
        transition_type = None,
        arrange_super = True
    ):
        if start_time != None:
            if start_frame != None:
                raise Warning("You defined both start frame and start time. " +\
                              "Just do one, ya dick.")
            start_frame = int(start_time * FRAME_RATE)

        if final_index == 'next':
            final_index = self.paths.index(self.active_path) + 1
        #self.active_expression_path = self.paths[final_index]

        super().morph_figure(
            final_index,
            start_frame = start_frame,
            duration = duration,
            transition_type = transition_type
        )

        #This code messes up the counters, making the numbers all wobbly.
        #I don't fully get why, but it has something to do with the fact that
        #the counters morph over 3 frames rather than the standard 10.
        #For now, this just checks whether the superbobject TexComplex is a
        #counter, and then skips if so.
        if isinstance(self.superbobject, tex_complex.TexComplex) \
            and 'sim_counter' not in self.superbobject.name and \
            arrange_super == True:
            self.superbobject.arrange_tex_bobjects(
                start_frame = start_frame,
                end_frame = start_frame + duration
            )

        for i, annotation in enumerate(self.annotations):
            gesture = annotation[0].subbobjects[0]
            label = gesture.subbobjects[0].subbobjects[0]
            for j, target in enumerate(annotation[1]):
                if target[0] == final_index and j > 0:
                    #old_loc = deepcopy(gesture.subbobjects[0].ref_obj.location)
                    gesture.morph_figure(
                        j,
                        start_frame = start_frame,
                        duration = duration
                    )
                    #new_loc = deepcopy(gesture.subbobjects[0].ref_obj.location)
                    d_loc = [0, 0, 0]#new_loc - old_loc

                    for t_bobj in label.tex_bobjects:
                        t_bobj.morph_figure(
                            j,
                            start_frame = start_frame,
                            duration = duration
                        )
                        #If a t_bobj morphs to an empty expression, adjust d_loc
                        if t_bobj.paths[j] == None and \
                            annotation[2] == 'top' and \
                            j > 0 and \
                            t_bobj.paths[j-1] != None:
                            d_loc[1] -= 0.8 #line height as scale = 0.67
                                            #Such hack.
                                            #Should make a vertical alignment
                                            #function for TexComplex TODO
                        if t_bobj.paths[j] != None and \
                            annotation[2] == 'top' and \
                            j > 0 and \
                            t_bobj.paths[j-1] == None:
                            d_loc[1] += 0.8

                    label.move_to(
                        start_frame = start_frame,
                        displacement = d_loc,
                        new_angle = [0, 0, -label.ref_obj.parent.rotation_euler[2]]
                    )
                    break

    def get_file_paths(self, expressions):
        #Replaces an svg_bobject method
        self.paths = []
        template = deepcopy(TEMPLATE_TEX_FILE)
        if self.typeface != 'default':
            template = template[:-4] #chop off the .tex
            template += '_' + self.typeface + '.tex'
            if not os.path.exists(template):
                raise Warning('Can\'t find template tex file for that font.')
        for expr in expressions:
            if expr == None:
                self.paths.append(expr)
            else: self.paths.append(tex_to_svg_file(expr, template, self.typeface))

def tex_to_svg_file(expression, template_tex_file, typeface):
    path = os.path.join(
        TEX_DIR,
        tex_title(expression, typeface)
    ) + ".svg"
    if os.path.exists(path):
        return path

    tex_file = generate_tex_file(expression, template_tex_file, typeface)
    dvi_file = tex_to_dvi(tex_file)
    return dvi_to_svg(dvi_file)

def tex_title(expression, typeface):
    name = expression
    to_delete = ['/', '\\', '{', '}', ' ', '~', '\'', '\"', '^']
    #Replace these rather than deleting them. These are characters that I've
    #wanted as lone expressions. (Which are also off limits in file names)
    to_replace = {
        '<' : 'lessthan',
        '>' : 'greaterthan',
        '?' : 'questionmark',
        '.' : 'point',
        ':' : 'colon',
        '%' : 'percent',
        '|' : 'vbar'
    }
    for char in name:
        if char in to_delete:
            name = name.replace(char, "")
    for char in name:
        if char in to_replace.keys():
            name = name.replace(char, to_replace[char])
    #name = str(name) + '_'
    if typeface != 'default':
        name += '_' + typeface

    return str(name)

def generate_tex_file(expression, template_tex_file, typeface):
    result = os.path.join(
        TEX_DIR,
        tex_title(expression, typeface)
    ) + ".tex"
    if not os.path.exists(result):
        print("Writing \"%s\" to %s"%(
            "".join(expression), result
        ))
        with open(template_tex_file, "r") as infile:
            body = infile.read()
            #I add an H to every expression to give a common reference point
            #for all expressions, then hide the H character. This is necessary
            #for consistent alignment of tex curves in blender, because
            #blender's import svg function sets the object's origin depending
            #on the expression itself, not according to a typesetting reference
            #frame.
            expression = '\\text{H} ' + expression
            body = body.replace(TEX_TEXT_TO_REPLACE, expression)
        with open(result, "w") as outfile:
            outfile.write(body)
    return result

def tex_to_dvi(tex_file):
    result = tex_file.replace(".tex", ".dvi")
    if not os.path.exists(result):
        commands = [
            "latex",
            "-interaction=batchmode",
            "-halt-on-error",
            "-output-directory=" + TEX_DIR,
            tex_file#,
            #">",
            #get_null()
        ]
        exit_code = os.system(" ".join(commands))
        if exit_code != 0:
            latex_output = ''
            log_file = tex_file.replace(".tex", ".log")
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    latex_output = f.read()
            raise Exception(
                "Latex error converting to dvi. "
                "See log output above or the log file: %s" % log_file)
    return result

def get_null():
    if os.name == "nt":
        return "NUL"
    return "/dev/null"

def dvi_to_svg(dvi_file):
    """
    Converts a dvi, which potentially has multiple slides, into a
    directory full of enumerated pngs corresponding with these slides.
    Returns a list of PIL Image objects for these images sorted as they
    where in the dvi
    """
    result = dvi_file.replace(".dvi", ".svg")
    if not os.path.exists(result):
        commands = [
            "dvisvgm",
            dvi_file,
            "-n",
            "-v",
            "3",
            "-o",
            result
            #Not sure what these are for, and it seems to work without them
            #so commenting out for now
            #,
            #">",
            #get_null()
        ]
        os.system(" ".join(commands))
    return result

#For testing
def main():
    for i in range(1000, 1200):
        tex_to_svg_file(str(i/10), TEMPLATE_TEX_FILE)

if __name__ == "__main__":
    main()
