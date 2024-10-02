import pygame

from Code.sprites import Water
from settings import *
from player import Player
from overlay import Ovelay
from sprites import *
from pytmx.util_pygame import load_pygame
from support import *


class Level:
    def __init__(self):
        
        # get the display surface
        self.display_surface = pygame.display.get_surface()

        # sprite groups
        #before: self.all_sprites = pygame.sprite.Group()
        #after
        self.all_sprites = CameraGroup()

        self.setup()
        self.overlay = Ovelay(self.player)

    def setup(self):
        tmx_data = load_pygame('../data/map.tmx')

        #import house tiles
        for layer in ['HouseFloor', 'HouseFurnitureBottom']:
            for x,y, surf in tmx_data.get_layer_by_name(layer).tiles():
                Generic((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites,LAYERS['house bottom'])
        for layer in ['HouseWalls', 'HouseFurnitureTop']:
            for x,y, surf in tmx_data.get_layer_by_name(layer).tiles():
                Generic((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites,LAYERS['main'])

        #import fence tiles
        for x, y, surf in tmx_data.get_layer_by_name('Fence').tiles():
            Generic ((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites, LAYERS['main'])

        #import water tiles
        water_frame = import_folder('../graphics/water')
        for x, y, surf in tmx_data.get_layer_by_name('Water').tiles():
            Water((x * TILE_SIZE, y * TILE_SIZE), water_frame , self.all_sprites)

        #import trees
        for object in tmx_data.get_layer_by_name('Trees'):
            Tree((object.x, object.y), object.image, self.all_sprites, object.name)

        # import decoration
        for object in tmx_data.get_layer_by_name('Decoration'):
            WildFlower((object.x, object.y), object.image, self.all_sprites)

        self.player = Player((640, 360), self.all_sprites)
        #background loading
        Generic(
            pos = (0,0),
            surf= pygame.image.load("../graphics/world/ground.png").convert_alpha(),
            groups = self.all_sprites,
            z = LAYERS["ground"])


    def run(self, dt):
        self.display_surface.fill('black')
        #before: self.all_sprites.draw(self.display_surface)
        #after:
        self.all_sprites.custom_draw(self.player)
        self.all_sprites.update(dt)
        self.overlay.display()

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

    def custom_draw (self, player):
        self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2
        self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2

        for layer in LAYERS.values():
            for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    self.display_surface.blit(sprite.image, offset_rect)