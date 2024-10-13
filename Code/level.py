import pygame

from settings import *
from player import Player
from overlay import Overlay
from sprites import *
from pytmx.util_pygame import load_pygame
from support import *
from transition import Transition

class Level:
    def __init__(self):
        
        # get the display surface
        self.display_surface = pygame.display.get_surface()

        self.all_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()
        self.tree_sprites = pygame.sprite.Group()
        self.interaction_sprites = pygame.sprite.Group()

        self.setup()
        self.overlay = Overlay(self.player)

        self.transition = Transition(self.reset_day, self.player)

    def setup(self):
        tmx_data = load_pygame('../data/map.tmx')

        #import house tiles
        for layer in ['HouseFloor', 'HouseFurnitureBottom']:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                Generic((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites, LAYERS['house bottom'])

        for layer in ['HouseWalls', 'HouseFurnitureTop']:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                Generic((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites)

        #import fence tiles
        for x, y, surf in tmx_data.get_layer_by_name('Fence').tiles():
            Generic ((x * TILE_SIZE, y * TILE_SIZE), surf,[self.all_sprites, self.collision_sprites], LAYERS['main'])

        #import water tiles
        water_frame = import_folder('../graphics/water')
        for x, y, surf in tmx_data.get_layer_by_name('Water').tiles():
            Water((x * TILE_SIZE, y * TILE_SIZE), water_frame , self.all_sprites)

        #import trees
        for object in tmx_data.get_layer_by_name('Trees'):
            Tree(
                pos=(object.x, object.y),
                surf=object.image,
                groups=[self.all_sprites, self.collision_sprites, self.tree_sprites],
                name=object.name,
                player_add_item = self.player_add_item
            )

        # import decoration
        for object in tmx_data.get_layer_by_name('Decoration'):
            WildFlower((object.x, object.y), object.image,[self.all_sprites, self.collision_sprites])

        # collision tiles:
        # Tạo các đối tượng va chạm từ lớp 'Collision'
        for x, y, surf in tmx_data.get_layer_by_name('Collision').tiles():
            collision_tile = Generic((x * TILE_SIZE, y * TILE_SIZE),
                                     pygame.Surface((TILE_SIZE, TILE_SIZE)),
                                     self.collision_sprites)

        # Player
        for obj in tmx_data.get_layer_by_name('Player'):
            if obj.name == 'Start':
                 self.player = Player(
                    pos=(obj.x, obj.y),
                    group=self.all_sprites,
                    collision_sprites=self.collision_sprites,
                    tree_sprites=self.tree_sprites,
                    interaction = self.interaction_sprites
                 )
            if obj.name == 'Bed':
                Interaction(
                    pos = (obj.x, obj.y),
                    size = (obj.width, obj.height),
                    groups = self.interaction_sprites,
                    name = obj.name
                )


        #background loading
        Generic(
            pos = (0,0),
            surf= pygame.image.load("../graphics/world/ground.png").convert_alpha(),
            groups = self.all_sprites,
            z = LAYERS["ground"])

    def player_add_item (self, item):
        self.player.item_inventory[item] += 1

    def reset_day (self):
        # apple on the tree
        for tree in self.tree_sprites.sprites():
            for apple in tree.apple_sprites.sprites():
                apple.kill()
            tree.create_fruit()

    def run(self, dt):
        self.display_surface.fill('white')
        #before: self.all_sprites.draw(self.display_surface)
        #after:
        self.all_sprites.custom_draw(self.player)
        self.all_sprites.update(dt)
        self.overlay.display()

        #show inventory log
        # print(self.player.item_inventory)

        if self.player.sleep:
            self.transition.play()

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

