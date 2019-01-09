from map_objects.rectangle import Rect
from map_objects.tile import Tile


class GameMap:
    def __init__(self, width, height, objects, entities, null_entity, logger):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()
        self.objects = self.initialize_objects(entities, objects)
        self.null_entity = null_entity
        self.logger = logger

    def select_rectangle(self, x1, y1, x2, y2):
        if x1 > x2:
            xg = x1
            xl = x2
        else:
            xg = x2
            xl = x1
        if y1 > y2:
            yg = y1
            yl = y2
        else:
            yg = y2
            yl = y1
        for x in range(xl, xg + 1):
            for y in range(yl, yg + 1):
                self.tiles[x][y].selected = True

        self.tiles[x1][y1].selected = True
        self.tiles[x2][y2].selected = True
        print(self.tiles[x1][y1].selected)

        self.logger.debug('changed tiles to be selected')

    def deselect_all(self):
        for x in range(0, self.width):
            for y in range(0, self.height):
                self.tiles[x][y].selected = False
                
    def is_blocked(self, x, y):
        if x < self.width and y < self.height and x > 0 and y > 0:
            if self.tiles[x][y].blocked:
                return True
            
            return False
        
        return True

    def move(self, entity, dx, dy):
        self.objects[entity.x + dx][entity.y + dy] = self.objects[entity.x][entity.y]
        self.objects[entity.x][entity.y] = self.null_entity
        self.objects[entity.x + dx][entity.y + dy].move(dx, dy)
        
    def is_cursor_blocked(self, x, y, camera):
        (cam_x, cam_y) = camera.to_camera_coordinates(x, y)
        if isinstance(cam_x, int):
            if cam_x < camera.width and cam_y < camera.height and cam_x >= 0 and cam_y >= 0:
                return False
        return True
    
    def initialize_objects(self, entities, objects):
        entity_array = objects
        for entity in entities:
            entity_array[entity.x][entity.y] = entity
        return entity_array

    def create_room(self, room):
        # go through the tilesin the rectangle and make them passable
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False

    def make_map(self):
        # Create starting room layout
        room1 = Rect(20, 15, 10, 15)
        room2 = Rect(35, 15, 10, 15)

        self.create_room(room1)
        self.create_room(room2)
        
    
    def initialize_tiles(self):
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]

        return tiles

