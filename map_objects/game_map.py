from map_objects.tile import Tile


class GameMap:
    def __init__(self, width, height, entities, objects):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()
        self.objects = self.initialize_objects(entities, objects)

    def is_blocked(self, x, y):
        if x < self.width and y < self.height:
            if self.tiles[x][y].blocked:
                return True
            
            return False
        
        return True

    def initialize_objects(self, entities, objects):
        entity_array = objects
        for entity in entities:
            entity_array[entity.x][entity.y] = entity
        return entity_array
        
    def initialize_tiles(self):
        tiles = [[Tile(False) for y in range(self.height)] for x in range(self.width)]

        tiles[0][0].blocked = True
        tiles[0][0].block_sight = True
        tiles[30][22].blocked = True
        tiles[30][22].block_sight = True
        tiles[31][22].blocked = True
        tiles[31][22].block_sight = True
        tiles[32][22].blocked = True
        tiles[32][22].block_sight = True
        return tiles

