class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    null_entity is used to spawn the initial object map and is used to verify if anything is in the
        way
    """
    def __init__(self, x, y, char, color, camera, null_entity = False):
        self.x = x
        self.y = y
        (self.cam_x, self.cam_y) = camera.to_camera_coordinates(x,y)
        self.char = char
        self.color = color
        self.null_entity = null_entity

    def move(self, dx, dy):
    # Move the entity by a given amount
        self.x += dx
        self.y += dy
        self.cam_x += dx
        self.cam_y += dy

    def move_with_camera(self, dx, dy):
        self.x += dx
        self.y += dy
