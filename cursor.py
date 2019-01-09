class Cursor():
    def __init__(self, entity):
        self.entity = entity
        self.entity.x = self.entity.cam_x
        self.entity.y = self.entity.cam_y

    def appear(self):
        self.entity.char = '+'

    def disappear(self):
        self.entity.char = ' '
    
