import libtcodpy as libtcod

def handle_keys(key):
    key_char = chr(key.c)
    
    #Movement keys
    if key.vk == libtcod.KEY_UP:
        return {'camera_move': (0,-1)}
    elif key.vk == libtcod.KEY_DOWN:
        return {'camera_move': (0,1)}
    elif key.vk == libtcod.KEY_LEFT:
        return {'camera_move': (-1, 0)}
    elif key.vk == libtcod.KEY_RIGHT:
        return {'camera_move': (1, 0)}

    if key_char == 'w':
        return {'cursor_move': (0, -1)}
    elif key_char == 's':
        return {'cursor_move': (0, 1)}
    elif key_char == 'a':
        return {'cursor_move': (-1, 0)}
    elif key_char == 'd':
        return {'cursor_move': (1, 0)}
    
    if key.lctrl and key_char == 'b':
        return {'build': True}
    
    if key.vk == libtcod.KEY_ENTER and key.lalt:
        #Alt+Enter: toggle full screen
        #return {'fullscreen': True}
        pass

    elif key.vk == libtcod.KEY_ESCAPE:
        #Exit the game
        return {'exit': True}

    #No key pressed
    return {}

def build_keys(key):
    pass
