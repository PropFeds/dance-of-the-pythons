import tcod
import json
from data.enums import RenderOrder
from components.position import Position
from components.graphics import Graphics

class Renderer:
    def __init__(self):
        self.config=json.load(open('data/config.json'))
        self.palette=json.load(open('data/palette.json'))
        tcod.console_set_custom_font('data/fonts/terminal12x16_gs_ro.png', tcod.FONT_TYPE_GREYSCALE | tcod.tcod.FONT_LAYOUT_CP437)
        self.console_root=tcod.console_init_root(self.config['terminal_width'], self.config['terminal_height'], 'Dance of the Pythons', False, tcod.RENDERER_SDL2, 'C', False)
        # array to blit by order
        self.map_consoles=[]
        # Grounds, walls, entities and particles consoles (index 0~6)
        for i in range(7):
            self.map_consoles.append(tcod.console.Console(self.config['consoles']['map']['width'][i], self.config['consoles']['map']['height'][i], 'C'))
        
    def render_routine(self, terrain_map, fov):
        self.render_terrain(terrain_map, fov)
        self.blit_entities()
    
    def render_terrain(self, terrain_map, fov):
        # gather fov (array) from bitwise orring entities with both Vision and Companion components
        for y in range(terrain_map.width):
            for x in range(terrain_map.height):
                if fov[y, x]:
                    self.map_consoles[0].tiles[['ch', 'fg']][y, x]=ord(terrain_map.grounds[y, x].char), (*terrain_map.grounds[y, x].colour_lit, 255)
                    self.map_consoles[1].tiles[['ch', 'fg']][y, x]=ord(terrain_map.walls[y, x].char), (*terrain_map.walls[y, x].colour_lit, 255)
                    terrain_map.explored[y, x]=True
                elif terrain_map.explored[y, x]:
                    self.map_consoles[0].tiles[['ch', 'fg']][y, x]=ord(terrain_map.grounds[y, x].char), (*terrain_map.grounds[y, x].colour_dim, 255)
                    self.map_consoles[1].tiles[['ch', 'fg']][y, x]=ord(terrain_map.walls[y, x].char), (*terrain_map.walls[y, x].colour_dim, 255)

    def render_entities(self, spawner, fov):
        for entity in spawner.entities:
            if entity.components[Position] and entity.components[Graphics]:
                y=entity.components[Position].y
                x=entity.components[Position].x
                if fov[y, x]:
                    self.map_consoles[RenderOrder[entity.components[Graphics].render_order].value].tiles[['ch', 'fg']][y, x]=ord(entity.components[Graphics].char), (*entity.components[Graphics].colour, 255)

    def blit_entities(self):
        for i, console in enumerate(self.map_consoles):
            console.blit(self.console_root, self.config['consoles']['map']['x'][i], self.config['consoles']['map']['y'][i], 0, 0, self.config['consoles']['map']['width'][i], self.config['consoles']['map']['height'][i])

    def erase_entities(self, spawner, fov):
        # gather fov (array) from bitwise orring entities with both Vision and Companion components
        for entity in spawner.entities:
            if entity.components[Position] and entity.components[Graphics]:
                y=entity.components[Position].y
                x=entity.components[Position].x
                if fov[y, x]:
                    self.map_consoles[RenderOrder[entity.components[Graphics].render_order].value].tiles[['ch']][y, x]=0