import libtcodpy as libtcod


def render_all(con, cursor, entities, camera, game_map, screen_width, screen_height, colors, mode, logger):
    # Draw all tiles and entities in game map
    for y in range(camera.height):
        for x in range(camera.width):
            cam_x = camera.x + x
            cam_y = camera.y + y
            try:
                tile = game_map.tiles[cam_x][cam_y]
                entity = game_map.objects[cam_x][cam_y]
            except IndexError:
                logger.error('cam_x = {}, cam_y = {}'.format(cam_x, cam_y))
                logger.error('Rendering out of map range')
                raise IndexError('Rendered outside of map range')
            
            if tile.block_sight:
                if tile.selected:
                    libtcod.console_set_char_background(con, x, y, colors.get('good_selected_wall'), libtcod.BKGND_SET)
                else:
                    libtcod.console_set_char_background(con, x, y, colors.get('dark_wall'), libtcod.BKGND_SET)
            else:
                if tile.selected:
                    libtcod.console_set_char_background(con, x, y, colors.get('good_selected_floor'), libtcod.BKGND_SET)
                else:
                    libtcod.console_set_char_background(con, x, y, colors.get('dark_ground'), libtcod.BKGND_SET)
            #Draw all entities in camera range    
            if not entity.null_entity:
                draw_entity(con, entity, x, y)

    if mode != 0:
        draw_entity(con, cursor.entity, cursor.entity.cam_x, cursor.entity.cam_y)

    libtcod.console_blit(con, 0, 0, camera.width, camera.height, 0, 0, 0)

def clear_all(con, cursor, game_map, camera, logger):
    for y in range(camera.height):
        for x in range(camera.width):
            cam_x = camera.x + x
            cam_y = camera.y + y
            try:
                entity = game_map.objects[cam_x][cam_y]
            except IndexError:
                logger.error('cam_x = {}, cam_y = {}'.format(cam_x, cam_y))
                logger.error('Clearing entity out of map range')
                raise IndexError('Rendered outside of map range')
            if not entity.null_entity:
                clear_entity(con, entity, x, y)
    clear_entity(con, cursor.entity, cursor.entity.cam_x, cursor.entity.cam_y)
    
def draw_entity(con, entity, x, y):
    libtcod.console_set_default_foreground(con, entity.color)
    libtcod.console_put_char(con, x, y, entity.char, libtcod.BKGND_NONE)

def clear_entity(con, entity, x, y):
    # erase the character that represents this object
    libtcod.console_put_char(con, x, y, ' ', libtcod.BKGND_NONE)
