from random import randint, choice
from timer import Timer
from settings import *
from support import *

class Generic(pygame.sprite.Sprite):
    def __init__(self,pos, surf, groups, z = LAYERS["main"]):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.z = z
        self.hitbox = self.rect.copy().inflate(-20, -self.rect.height * 0.75)

class Water (Generic):
    def __init__(self, pos, frames, groups):
        #animation setup
        self.frames = frames
        self.frame_index = 0

        #sprite setup
        super().__init__(pos = pos, surf = self.frames[self.frame_index], groups = groups, z = LAYERS['water'])

    def animate (self, dt):
        self.frame_index += 4 * dt
        if self.frame_index >= len(self.frames):
            self.frame_index = 0

        self.image = self.frames[int(self.frame_index)]

    def update(self, dt):
        self.animate(dt)

class WildFlower (Generic):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)


class Tree (Generic): # quản lý sức khỏe và sự tương tác của cây
    def __init__(self, pos, surf, groups, name):
        super().__init__(pos, surf, groups)
        # #tree_attributes
        # self.health = 5
        # self.alive = True
        # stump_path = f'../graphics/stumps/{"small" if name == "Small" else "large"}.png'
        # self.stumps_surf = pygame.image.load(stump_path).convert_alpha()
        # self.invul_timer = Timer(200)



     # apples
        self.apples_surf = pygame.image.load('../graphics/fruit/apple.png')
        self.apple_pos = APPLE_POS[name] # name: large or small
        self.apple_sprites = pygame.sprite.Group()
        self.create_fruit() # co tao moc

    def create_fruit(self):
       for pos in self.apple_pos:
           if randint(0, 10) < 2: # xác định khả năng tạo quả
               x = pos[0] + self.rect.left
               y = pos[1] + self.rect.top
               Generic(
                   pos = (x, y),
                   surf = self.apples_surf,
                   groups = [self.apple_sprites, self.groups()[0]],
                   z = LAYERS['fruit'])

