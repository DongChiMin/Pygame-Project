import pygame

from Code.sky import RainOverlay
from settings import *
from player import Player
from overlay import Overlay
from sprites import *
from pytmx.util_pygame import load_pygame
from support import *
from transition import Transition
from soil import SoilLayer
from sky import Rain, Sky
from random import randint
from menu import Menu
from ui import ui

class Level:
    def __init__(self):
        
        # get the display surface
        self.display_surface = pygame.display.get_surface()

        self.all_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()
        self.tree_sprites = pygame.sprite.Group()
        self.interaction_sprites = pygame.sprite.Group()
        self.soil_layer = SoilLayer(self.all_sprites, self.collision_sprites)

        self.setup()
        self.overlay = Overlay(self.player)

        self.transition = Transition(self.reset_day, self.player)

        # sky
        self.rain_overlay = RainOverlay()
        self.rain = Rain(self.all_sprites)
        self.raining = randint(0, 10) > 7
        self.soil_layer.raining = self.raining
        self.sky = Sky()

        #UI
        self.ui = ui(self.player, self.overlay, self)

        #shop
        self.Menu = Menu(self.player, self.toggle_UI)
        self.UI_menu_active = False

        #sound
        self.background_music = pygame.mixer.Sound("../audio/music.mp3")
        self.background_music.set_volume(0.5)
        self.background_music.play()
        self.success = pygame.mixer.Sound("../audio/success.wav")
        self.success.set_volume(0.4)

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
                    interaction = self.interaction_sprites,
                    soil_layer = self.soil_layer,
                    toggle_UI = self.toggle_UI
                 )
            if obj.name == 'Bed':
                Interaction(
                    pos = (obj.x, obj.y),
                    size = (obj.width, obj.height),
                    groups = self.interaction_sprites,
                    name = obj.name
                )

            if obj.name == 'Trader':
                Interaction(
                    pos=(obj.x, obj.y),
                    size=(obj.width, obj.height),
                    groups=self.interaction_sprites,
                    name=obj.name
                )


        #background loading
        Generic(
            pos = (0,0),
            surf= pygame.image.load("../graphics/world/ground.png").convert_alpha(),
            groups = self.all_sprites,
            z = LAYERS["ground"])

    def player_add_item (self, item):
        self.player.item_inventory[item] += 1
        self.success.play()
        item_image = pygame.image.load(f'../graphics/items/{item}.png').convert_alpha()
        self.ui.add_item_display(item_image)  # Thêm item vào danh sách hiển thị

    def toggle_UI(self):
        self.UI_menu_active = not self.UI_menu_active

    def reset_day (self):
        # plants hien
        self.soil_layer.update_plants()
        # soil
        self.soil_layer.remove_water()
        self.raining = randint(0, 10) > 3
        self.soil_layer.raining = self.raining
        if self.raining:
            self.soil_layer.water_all() 

        # apple on the tree
        for tree in self.tree_sprites.sprites():
            if isinstance(tree, Tree):
                for apple in tree.apple_sprites.sprites():
                    apple.kill()
                tree.create_fruit()

        # hien
        self.sky.start_color = [255, 255, 255]

    def plant_collision(self):
        if self.soil_layer.plant_sprites:
            for plant in self.soil_layer.plant_sprites.sprites():
                if plant.harvestable and plant.rect.colliderect(self.player.hitbox):
                    self.player_add_item(plant.plant_type)
                    plant.kill()
                    Particle(plant.rect.topleft, plant.image, self.all_sprites, z = LAYERS['main'])
                    self.soil_layer.grid[plant.rect.centery // TILE_SIZE][plant.rect.centerx // TILE_SIZE].remove('P')

    def run(self, dt):

        #drawing logic
        self.display_surface.fill('black')
        self.all_sprites.custom_draw(self.player)


        #weather

        if self.raining:
            self.rain_overlay.display()
            if not self.UI_menu_active and not self.ui.ui_opened:
                self.rain.update()

        # updates
        if self.UI_menu_active:
            #daytime: neu UI dang bat thi khong chay thời gian nữa
            self.sky.display(dt, True)
            self.Menu.update()
        elif self.ui.ui_opened:
            self.sky.display(dt, True)
        else:
            # daytime
            self.sky.display(dt, False)
            # neu khong hien UI thi sprites mới được update
            self.all_sprites.update(dt)
            self.plant_collision()


        if not self.ui.ui_opened:
            self.overlay.display()
        self.ui.run()




        #show inventory log
        #print(self.player.item_inventory)

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

