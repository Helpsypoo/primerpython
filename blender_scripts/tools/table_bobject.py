import bpy

import imp
#from copy import deepcopy
import math

import bobject
imp.reload(bobject)
from bobject import *

import tex_bobject
imp.reload(tex_bobject)
import svg_bobject
imp.reload(svg_bobject)

class TableBobject(Bobject):
    """docstring for TableBobject."""
    def __init__(self,
        width = 10,
        height = 10,
        cell_padding = 0.75,
        centered = False,
        element_matrix = None,
        **kwargs
    ):
        print('Initializing table bobject')
        if 'name' not in kwargs:
            kwargs['name'] = 'table'
        super().__init__(**kwargs)

        self.width = width
        self.height = height
        #This doesn't actually do anything right now.
        self.centered = centered

        if element_matrix == None:
            element_matrix = self.default_element_matrix()
        self.element_matrix = element_matrix

        for row in self.element_matrix:
            for element in row:
                self.add_subbobject(element)

        #Get row and column dimensions
        self.cell_padding = cell_padding
        self.row_heights = []
        self.column_widths = []
        for i, row in enumerate(self.element_matrix):
            self.row_heights.append(0)
            for j, cell in enumerate(row):
                width, height = self.get_element_dimensions(self.element_matrix[i][j])

                width += 2 * self.cell_padding
                height += 2 * self.cell_padding

                if self.row_heights[i] < height:
                    self.row_heights[i] = height

                if len(self.column_widths) < j + 1:
                    self.column_widths.append(0)
                if self.column_widths[j] < width:
                    self.column_widths[j] = width


        self.fill_dimensions()
        self.place_elements()
        self.draw_grid()

    def get_element_dimensions(self, element):
        if not isinstance(element, svg_bobject.SVGBobject):
            raise Warning("Tables can't yet hold things that aren't svg bobjects")

        width = 0
        height = 0
        #Just size to the max width out of all possible forms
        for key in element.imported_svg_data:
            fig = element.imported_svg_data[key]
            if fig['length'] > width:
                width = fig['length']
            if fig['height'] > height:
                height = fig['height']

        return width, height

    def place_elements(self):
        y = 0
        for i, row in enumerate(self.element_matrix):
            x = 0
            for j, element in enumerate(row):
                x_disp = 0
                if element.centered == True:
                    x_disp = self.column_widths[j] / 2
                else:
                    x_disp = self.cell_padding
                element.ref_obj.location[0] = x + x_disp
                x += self.column_widths[j]

                #SVG bobjects are currently vertically centered
                #(or maybe not purposefully unaligned)
                y_disp = self.row_heights[i] / 2
                element.ref_obj.location[1] = y - y_disp
            y -= self.row_heights[i]

    def fill_dimensions(self):
        width_factor = self.width / sum(self.column_widths)
        height_factor = self.height / sum(self.row_heights)

        self.scale_factor = min(width_factor, height_factor)

        for i in range(len(self.row_heights)):
            self.row_heights[i] = self.row_heights[i] * self.scale_factor
        for j in range(len(self.column_widths)):
            self.column_widths[j] = self.column_widths[j] * self.scale_factor


        for i, row in enumerate(self.element_matrix):
            for j, element in enumerate(row):
                element.scale = [
                    element.scale[0] * self.scale_factor,
                    element.scale[1] * self.scale_factor,
                    element.scale[2] * self.scale_factor,
                ]

    def draw_grid(self):
        #Just going to draw two lines here, since that's what I need right now.
        vert_line = import_object(
            'one_side_cylinder', 'primitives',
            location = [self.column_widths[0], 0, 0],
            scale = [0.05, 0.05, sum(self.row_heights)],
            rotation_euler = [math.pi / 2, 0, 0]
        )
        hor_line = import_object(
            'one_side_cylinder', 'primitives',
            location = [0, -self.row_heights[0], 0],
            scale = [0.05, 0.05, sum(self.column_widths)],
            rotation_euler = [0, math.pi / 2, 0]
        )


        for line in [vert_line, hor_line]:
            self.add_subbobject(line)

    def default_element_matrix(self):
        strings = [['This', 'is', 'a'],['wide', 'table', 'dawg']]
        element_matrix = []

        for row in strings:
            element_matrix.append([])
            for element in row:
                element_matrix[-1].append(
                    tex_bobject.TexBobject(
                        '\\text{' + element + '}',
                        centered = True
                    )
                )

        return element_matrix
