class Camera:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def is_on_edge(self, game_map, dx, dy):
        #Checking if zone exits before moving into it
        if (self.x + dx < 0 or
            self.x + self.width + dx > game_map.width or
            self.y + dy < 0 or
            self.y + self.height + dy > game_map.height):
            return True

        return False

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        
    def to_camera_coordinates(self, x, y):
        #convert coordinates on the map to coordinates on the screen
        camx = x - self.x
        camy = y - self.y
        if (camx < 0 or camy < 0 or camx >= self.width or camy >= self.height):
            #if it's outside the view, return nothing
            return (None, None)

        return (camx, camy)

    
