class Vertex:
    def __init__(self, _id, x, y):
        self.id = _id
        self.x = x
        self.y = y
    pass

    def equals(self, obj):
        if obj:
            return self.id == obj.id
        else:
            return False

    def tostring(self):
        return 'Vertex_' + str(self.id) + '(' + str(self.x) + '|' + str(self.y) + ')'
