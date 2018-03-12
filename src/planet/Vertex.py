class Vertex:
    def __init__(self, position):
        self.id = position
        self.position = position
    pass

    def equals(self, obj):
        if obj and isinstance(obj, Vertex):
            return self.position == obj.position
        else:
            return False

    def __str__(self):
        return 'Vertex(' + str(self.position[0]) + '|' + str(self.position[1]) + ')'
