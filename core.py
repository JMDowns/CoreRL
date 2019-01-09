import libtcodpy as libtcod
import logging

from camera import Camera
from cursor import Cursor
from entity import Entity
from input_handlers import handle_keys
from map_objects.game_map import GameMap
from render_functions import clear_all, render_all

def main():

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')

    file_handler = logging.FileHandler('debug.log')
    file_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)

    warning_handler = logging.FileHandler('warning.log')
    warning_handler.setFormatter(formatter)
    warning_handler.setLevel(logging.WARNING)
    logger.addHandler(warning_handler)
    
    screen_width = 80
    screen_height = 50
    map_width = 160
    map_height = 90
    camera_width = 80
    camera_height = 45

    colors = {
        'dark_wall': libtcod.Color(0,0,100),
        'dark_ground': libtcod.Color(50,50,150)
    }

    camera = Camera(0, 0, camera_width, camera_height)

    cursor =  Cursor(Entity(int(screen_width / 2), int(screen_height / 2), '+', libtcod.white, camera))

    null_entity = Entity(0, 0, ' ', libtcod.red, camera, True)
    
    player = Entity(camera_width+1, 10, '@', libtcod.white, camera)
    npc = Entity(int(screen_width / 2 - 5), int(screen_height / 2), '@', libtcod.yellow, camera)
    npc1 = Entity(int(screen_width / 2 - 5+1), int(screen_height / 2), '@', libtcod.yellow, camera)
    npc2 = Entity(int(screen_width / 2 - 5+2), int(screen_height / 2), '@', libtcod.yellow, camera)
    npc3 = Entity(int(screen_width / 2 - 5+3), int(screen_height / 2), '@', libtcod.yellow, camera)
    npc4 = Entity(int(screen_width / 2 - 5+4), int(screen_height / 2), '@', libtcod.yellow, camera)
      
    entities = [npc, npc1, npc2, npc3, npc4, player]

    empty_objects = [[null_entity for y in range(0, map_height)] for x in range (0, map_width)]
    
    libtcod.console_set_custom_font('arial10x10.png',
                                    libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

    libtcod.console_init_root(screen_width, screen_height, 'CoreRL', False)

    con = libtcod.console_new(screen_width, screen_height)

    game_map = GameMap(map_width, map_height, empty_objects, entities, null_entity)
    game_map.make_map()
    
    key = libtcod.Key()
    mouse = libtcod.Mouse()

    logger.debug('Initialized starting game variables')

    logger.debug('Starting game loop')
    
    while not libtcod.console_is_window_closed():
        
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)
        
        render_all(con, cursor, entities, camera, game_map, screen_width, screen_height, colors, logger)
        
        libtcod.console_flush()

        clear_all(con, cursor, game_map, camera, logger)

        action = handle_keys(key)

        camera_move = action.get('camera_move')
        cursor_move = action.get('cursor_move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')
        build = action.get('build')

        if camera_move:
            dx, dy = camera_move
            if not camera.is_on_edge(game_map, dx, dy):
                camera.move(dx, dy)
                cursor.entity.move_with_camera(dx, dy)
                
        if cursor_move:
            dx, dy = cursor_move
            if not game_map.is_cursor_blocked(cursor.entity.x+dx, cursor.entity.y+dy, camera):
                logger.debug('moved cursor {} x, {} y units'.format(dx, dy))
                logger.debug('cursor x={}, y={}'.format(cursor.entity.x, cursor.entity.y))
                cursor.entity.move(dx, dy)
                logger.debug('after moving, cursor x={}, y={}'.format(cursor.entity.x, cursor.entity.y))
            else:
                logger.debug('cursor x={}, y={}'.format(cursor.entity.x, cursor.entity.y))
                logger.debug('cursor cam_x={}, cam_y={}'.format(cursor.entity.cam_x, cursor.entity.cam_y))

        if build:
            print("build mode")
            
        if exit:
            return True

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())


if __name__=="__main__":
    main()
