import tcod
import tcod.event
import json
from map_objects.game_map import GameMap
from components.inventory import Inventory
from entity import Entity
from renderer import RenderOrder, render_all, clear_all
from game_states import GameStates
from input_handler import handle_event
from factions import Factions

def main():
    # Importing data from config
    with open('data/config.json') as cfg:
        data=json.load(cfg)
    terminal_width=data['terminal_width']
    terminal_height=data['terminal_height']
    map_width=data['map_width']
    map_height=data['map_height']
    fov_algorithm=data['fov_algorithm']
    fov_light_walls=bool(data['fov_light_walls'])
    fov_radius=data['fov_radius']
    # Init root console and player
    player=Entity(0, 0, 'Ratiel Snailface', Factions.ALLY, '@', (217, 160, 102), 5, 1, 0, 15, RenderOrder.ACTOR, False, Inventory(26), None, None)
    entities=[player]
    tcod.console_set_custom_font('gfx/fonts/terminal16x16_gs_ro.png', tcod.FONT_TYPE_GREYSCALE | tcod.tcod.FONT_LAYOUT_CP437)
    root_console=tcod.console_init_root(terminal_width, terminal_height, 'Dance of the Pythons', False, tcod.RENDERER_SDL2, 'C', False)
    display=tcod.console.Console(terminal_width, terminal_height, 'C')
    display.bg[:]=(8, 19, 4)
    #interface=tcod.console.Console(terminal_width, map_height, 'C')
    game_map=GameMap(map_width, map_height)
    # Then generate map
    fov_recompute=True
    # message log
    game_state=GameStates.TURN_PLAYER
    prev_game_state=game_state
    #targeting_item=None
    # Rendering for the first time
    game_map.recompute_fov(player.x, player.y, fov_radius, fov_light_walls, fov_algorithm)
    render_all(root_console, display, entities, player, game_map, fov_recompute, terminal_width, terminal_height, game_state)
    fov_recompute=False
    tcod.console_flush()
    # Game loop
    while True:
        # Render
        if fov_recompute:
            game_map.recompute_fov(player.x, player.y, fov_radius, fov_light_walls, fov_algorithm)
        render_all(root_console, display, entities, player, game_map, fov_recompute, terminal_width, terminal_height, game_state)
        fov_recompute=False
        tcod.console_flush()
        clear_all(display, entities)
        # Processing action
        action=handle_event(game_state)
        move=action.get('move')
        pickup=action.get('pickup')
        take_inventory=action.get('take_inventory')
        fullscreen=action.get('fullscreen')
        exit=action.get('exit')
        # Player's Turn
        player_results=[]
        if game_state==GameStates.TURN_PLAYER:
            if move:
                dx, dy=move
                if game_map.path_map.walkable[player.y+dy, player.x+dx] and player.x+dx>=0 and player.y+dy>=0:
                    # target=get_blocking_entities(entities, player.x+dx, player.y+dy)
                    if False:
                        print('PLACEHOLDER')
                    # if target:
                        # depends on object: if enemy attack, if ally swap, if vendor/chest interact
                    else:
                        player.move(dx, dy)
                        fov_recompute=True
                    game_state=GameStates.TURN_ALLY
            elif pickup: # Should implement a pickup list like POWDER
                for entity in entities:
                    if entity.item and entity.x==player.x and entity.y==player.y:
                        print('ADD ITEM')   # Add item
                        break
                else:
                    print('GRAB GROUND')    # Message log to grab ground
        
        if take_inventory:
            prev_game_state=game_state
            game_state=GameStates.MENU_INVENTORY
        
        if exit:
            if game_state.value>=10:  # Game states >= 10 are menus: inventory, quipment, etc.
                game_state=prev_game_state
            if game_state.value>=20:  # Game states >= 20 are targetings
                player_results.append({'targeting_cancelled': True})
            # else brings up main menu
        
        if fullscreen:
            tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

        # Player turn messages

        # Faction turns (includes message logs built within)
        if game_state==GameStates.TURN_ALLY:
                game_state=GameStates.TURN_ENEMY
        
        if game_state==GameStates.TURN_ENEMY:
                game_state=GameStates.TURN_NEUTRAL
        
        if game_state==GameStates.TURN_NEUTRAL:
                game_state=GameStates.TURN_PLAYER


if __name__=='__main__':
    main()