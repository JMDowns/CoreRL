import libtcodpy as libtcod
import logging

from camera import Camera
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

    player = Entity(camera_width+1, 10, '@', libtcod.white, camera)
    npc = Entity(int(screen_width / 2 - 5), int(screen_height / 2), '@', libtcod.yellow, camera)
    
    entities = [npc, player]

    objects = [[Entity(x, y, ' ', libtcod.red, camera, True)
                for y in range(map_height)] for x in range(map_width)]

    libtcod.console_set_custom_font('arial10x10.png',
                                    libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

    libtcod.console_init_root(screen_width, screen_height, 'CoreRL', False)

    con = libtcod.console_new(screen_width, screen_height)

    game_map = GameMap(map_width, map_height, entities, objects)

    key = libtcod.Key()
    mouse = libtcod.Mouse()

    logger.debug('Initialized starting game variables')

    logger.debug('Starting game loop')
    
    while not libtcod.console_is_window_closed():
        
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)
        
        render_all(con, entities, camera, game_map, screen_width, screen_height, colors, logger)
        
        libtcod.console_flush()

        clear_all(con, game_map.objects, camera, logger)

        action = handle_keys(key)

        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        if move:
            dx, dy = move
            if not camera.is_on_edge(game_map, dx, dy):
                camera.move(dx, dy)
            
            if not game_map.is_blocked(player.x+dx, player.y+dy):
                #player.move(dx,dy)
                pass

        if exit:
            return True

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())


if __name__=="__main__":
    main()
