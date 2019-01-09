import libtcodpy as libtcod
import logging

from camera import Camera
from cursor import Cursor
from entity import Entity
from input_handlers import handle_keys, handle_build_keys
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
        'dark_ground': libtcod.Color(50,50,150),
        'bad_selected_wall': libtcod.Color(100, 0, 0),
        'bad_selected_floor': libtcod.Color(150, 50, 50),
        'good_selected_wall': libtcod.Color(0, 100, 0),
        'good_selected_floor': libtcod.Color(50, 150, 50)
    }

    modes = {
        'none': 0,
        'build': 1
    }

    active_mode = modes.get('none')

    camera = Camera(0, 0, camera_width, camera_height)

    cursor =  Cursor(Entity(int(screen_width / 2), int(screen_height / 2), ' ', libtcod.white, camera))
    has_selected = False
    selected_x = 0
    selected_y = 0

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

    game_map = GameMap(map_width, map_height, empty_objects, entities, null_entity, logger)
    game_map.make_map()
    
    key = libtcod.Key()
    mouse = libtcod.Mouse()

    logger.debug('Initialized starting game variables')

    logger.debug('Starting game loop')
    
    while not libtcod.console_is_window_closed():
        
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)
        
        render_all(con, cursor, entities, camera, game_map, screen_width, screen_height, colors, active_mode, logger)
        
        libtcod.console_flush()

        clear_all(con, cursor, game_map, camera, logger)

        if active_mode == modes.get('none'):
            action = handle_keys(key)
        if active_mode == modes.get('build'):
            action = handle_build_keys(key)
        #base actions (when active_mode is 'none')
        build_mode = action.get('build_mode')
        camera_move = action.get('camera_move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        #actions in build mode, but not in base (active_mode = 'build')
        cursor_move = action.get('cursor_move')
        exit_mode = action.get('exit_mode')
        select = action.get('select')
        
        if camera_move:
           dx, dy = camera_move
           if not camera.is_on_edge(game_map, dx, dy):
                camera.move(dx, dy)
                cursor.entity.move_with_camera(dx, dy)

        if cursor_move:
            dx, dy = cursor_move
            if not game_map.is_cursor_blocked(cursor.entity.x+dx, cursor.entity.y+dy, camera):
                cursor.entity.move(dx, dy)
                logger.debug('has_selected = {}, active_mode = {}'.format(has_selected, active_mode))
                if has_selected and active_mode == modes.get('build'):
                    game_map.deselect_all()
                    game_map.select_rectangle(selected_x, selected_y, cursor.entity.x, cursor.entity.y)
                    logger.debug('called select rectangle')
                logger.debug('cursor x={}, y={}'.format(cursor.entity.x, cursor.entity.y))
            else:
                logger.debug('cursor x={}, y={}'.format(cursor.entity.x, cursor.entity.y))
                logger.debug('cursor cam_x={}, cam_y={}'.format(cursor.entity.cam_x, cursor.entity.cam_y))

        if build_mode:
            active_mode = modes.get('build')
            logger.debug('changed to build mode')
            cursor.appear()

        if select:
            if active_mode == modes.get('build'):
                if has_selected == False:
                    logger.debug('selected an object in build mode')
                    selected_x = cursor.entity.x
                    selected_y = cursor.entity.y
                    has_selected = True
                else:
                    logger.debug('stopped selecting an object in build mode')
                    selected_x = 0
                    selected_y = 0
                    has_selected = False
                    game_map.deselect_all()

        if exit_mode:
            active_mode = modes.get('none')
            game_map.deselect_all()
            logger.debug('switched out of mode')
            cursor.disappear()
            
        if exit:
            return True

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())


if __name__=="__main__":
    main()
