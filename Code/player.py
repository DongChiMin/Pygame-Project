import pygame
from settings import *
from support import *
from timer import Timer

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, collision_sprites,
                 tree_sprites, interaction, soil_layer, toggle_UI):
        super().__init__(group)

        self.import_assets()
        self.status = 'down'
        self.frame_index = 0

        #general setup
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center = pos)
        self.z = LAYERS["main"]

        #movement attributes
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 200

        # collision
        self.hitbox = self.rect.copy().inflate((-126, -70))
        self.collision_sprites = collision_sprites

        #timers
        self.timers = {
            'tool use': Timer(350, self.use_tool),
            'tool switch': Timer(200),
            'seed use': Timer(350, self.use_seed),
            'seed switch': Timer(200),
        }

        # tools
        self.tools = ['hoe', 'axe', 'water']
        self.tool_index = 0
        self.selected_tool = self.tools[self.tool_index]

        # seeds
        self.seeds = ['wheat', 'tomato']
        self.seed_index = 0
        self.selected_seed = self.seeds[self.seed_index]

        # player inventory (player's knapsack)
        self.item_inventory = {
            'wood': 0,
            'apple': 0,
            'wheat': 0,
            'tomato': 0
        }

        self.seed_inventory = {
            'wheat' : 5,
            'tomato': 5
        }
        self.money = 200

        # interaction
        self.tree_sprites = tree_sprites
        self.interaction = interaction
        self.sleep = False
        self.soil_layer = soil_layer
        self.toggle_UI = toggle_UI

        #sound
        self.isMoving = False
        self.watering = pygame.mixer.Sound("../audio/watering.wav")
        self.footstep = pygame.mixer.Sound("../audio/footstep.mp3")
        self.footstep.set_volume(1.5)
        self.button_sound = pygame.mixer.Sound('../audio/button.wav')

    def use_tool(self):
        print(f"Tool use = {self.selected_tool}")
        if self.selected_tool == 'hoe':
            self.soil_layer.get_hit(self.target_pos)

        if self.selected_tool == 'axe':
            for tree in self.tree_sprites.sprites():
                if tree.rect.collidepoint(self.target_pos):
                    tree.damage()

        if self.selected_tool == 'water':
            self.soil_layer.water(self.target_pos)
            self.watering.play()


    def get_target_pos(self):
        self.target_pos = self.rect.center + PLAYER_TOOL_OFFSET[self.status.split('_')[0]]
# hien
    def use_seed(self):
        if self.seed_inventory[self.selected_seed] > 0:
            #neu o dat chua co cay thi moi trong cay
            if self.soil_layer.plant_seed(self.target_pos, self.selected_seed):
                self.seed_inventory[self.selected_seed] -= 1

    def import_assets(self):
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
                           'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [],
                           'right_hoe': [], 'left_hoe': [], 'up_hoe': [], 'down_hoe': [],
                           'right_axe': [], 'left_axe': [], 'up_axe': [], 'down_axe': [],
                           'right_water': [], 'left_water': [], 'up_water': [], 'down_water': []}

        for animation in self.animations.keys():
            full_path = '../graphics/character/' + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self, dt):
        self.frame_index += 4 * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0

        self.image = self.animations[self.status][int(self.frame_index)]

    def input(self):
        keys = pygame.key.get_pressed()
        mouses = pygame.mouse.get_pressed()

        if not self.timers['tool use'].active and not self.sleep:
            if keys[pygame.K_w]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_s]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            if keys[pygame.K_d]:
                self.direction.x = 1
                self.status = 'right'
            elif keys[pygame.K_a]:
                self.direction.x = -1
                self.status = 'left'
            else:
                self.direction.x = 0

                # tool use
            if keys[pygame.K_SPACE]:
                self.input_tool_use()

                # change tool
            if keys[pygame.K_q] and not self.timers['tool switch'].active:
                self.change_tool()

                # seed use
            if keys[pygame.K_LCTRL]:
                self.input_seed_use()

                # change seed
            if keys[pygame.K_e] and not self.timers['seed switch'].active:
                self.change_seed()

            # if keys[pygame.K_f]:
            #     self.toggle_UI()
            #     collied_interaction_sprite = pygame.sprite.spritecollide(self, self.interaction, False)
            #     if collied_interaction_sprite:
            #         if collied_interaction_sprite[0].name == 'Trader':
            #             self.toggle_UI()
            #         else:
            #             self.status = 'left_idle'
            #             self.sleep = True

            if keys[pygame.K_f]:
                collied_interaction_sprite = pygame.sprite.spritecollide(self, self.interaction, False)
                if collied_interaction_sprite:
                    if collied_interaction_sprite[0].name == 'Bed':
                        self.status = 'left_idle'
                        self.sleep = True

    def open_trader(self):
        self.button_sound.play()
        print("opening trader")
        self.toggle_UI()

    def end_conservation(self):
        pass

    def input_tool_use(self):
        self.timers['tool use'].activate()
        self.direction = pygame.math.Vector2()
        self.frame_index = 0

    def input_seed_use(self):
        self.timers['seed use'].activate()
        self.direction = pygame.math.Vector2()
        self.frame_index = 0

    def change_tool(self):
        self.timers['tool switch'].activate()
        self.tool_index += 1
        self.tool_index = self.tool_index if self.tool_index < len(self.tools) else 0
        self.selected_tool = self.tools[self.tool_index]

    def change_seed(self):
        self.timers['seed switch'].activate()
        self.seed_index += 1
        self.seed_index = self.seed_index if self.seed_index < len(self.seeds) else 0
        self.selected_seed = self.seeds[self.seed_index]

    def get_status(self):
        # idle
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'

        # tool use
        if self.timers['tool use'].active:
            self.status = self.status.split('_')[0] + '_' + self.selected_tool

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def collision(self, direction):
        for sprite in self.collision_sprites.sprites():
            if hasattr(sprite, 'hitbox'):
                if sprite.hitbox.colliderect(self.hitbox):
                    if direction == 'horizontal':
                        if self.direction.x > 0:
                            self.hitbox.right = sprite.hitbox.left
                        if self.direction.x < 0:
                            self.hitbox.left = sprite.hitbox.right
                        self.rect.centerx = self.hitbox.centerx
                        self.pos.x = self.hitbox.centerx
                    if direction == 'vartical':
                        if self.direction.y > 0:
                            self.hitbox.bottom = sprite.hitbox.top
                        if self.direction.y < 0:
                            self.hitbox.top = sprite.hitbox.bottom
                        self.rect.centery = self.hitbox.centery
                        self.pos.y = self.hitbox.centery

    def move(self, dt):


        #nomalizing a vector
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()
            if not self.isMoving:
                self.footstep.play(loops = -1   )
                self.isMoving = True
        else:
            self.footstep.stop()
            self.isMoving = False


        #horizontal movement
        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox.centerx = round(self.pos.x)
       # before self.rect.centerx = self.pos.x
        self.rect.centerx = self.hitbox.centerx
        self.collision('horizontal')

        #vertical movement
        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.centery = round((self.pos.y))
        # bf self.rect.centery = self.pos.y
        self.rect.centery = self.hitbox.centery
        self.collision('vartical')

    def update(self, dt):
        self.input()
        self.get_status()
        self.update_timers()
        self.get_target_pos()
        self.move(dt)
        self.animate(dt)
