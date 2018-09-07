class Creature(object):
    def __init__(self, size = '1', color = 'creature_color_1', shape = 'shape1'):
        self.alleles = {
            "size" : size,
            "color" : color,
            "shape" : shape
        }
        self.birthday = None
        self.deathday = None
        self.name = None
        self.parent = None
        self.children = []

        self.locations = []
        self.velocities = []

        self.bobject = None
