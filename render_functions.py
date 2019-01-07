import libtcodpy as libtcod


def render_all(con, entities, camera, game_map, screen_width, screen_height, colors):
    # Draw all tiles in game map
    for y in range(camera.height):
        for x in range(camera.width):
            cam_x = camera.x + x
            cam_y = camera.y + y
            wall = game_map.tiles[cam_x][cam_y].block_sight
            entity = game_map.objects[cam_x][cam_y]

            if wall:
                libtcod.console_set_char_background(con, x, y, colors.get('dark_wall'), libtcod.BKGND_SET)
            else:
                libtcod.console_set_char_background(con, x, y, colors.get('dark_ground'), libtcod.BKGND_SET)
                if entity.null_entity is False:
                    draw_entity(con, entity, x, y)
    # Draw  all entities in list 
    #for entity in entities:
    #    if (entity.cam_x):
    #        draw_entity(con, entity)
    libtcod.console_blit(con, 0, 0, camera.width, camera.height, 0, 0, 0)

def clear_all(con, objects, camera):
    for y in range(camera.height):
        for x in range(camera.width):
            cam_x = camera.x + x
            cam_y = camera.y + y
            entity = objects[cam_x][cam_y]
            if (entity.null_entity == False):
                clear_entity(con, entity, x, y)

def draw_entity(con, entity, x, y):
    libtcod.console_set_default_foreground(con, entity.color)
    libtcod.console_put_char(con, x, y, entity.char, libtcod.BKGND_NONE)

def clear_entity(con, entity, x, y):
    # erase the character that represents this object

    libtcod.console_put_char(con, x, y, ' ', libtcod.BKGND_NONE)
