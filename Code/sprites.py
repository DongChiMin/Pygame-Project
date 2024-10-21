import pygame
from settings import *
from random import randint, choice
from timer import Timer

class Generic(pygame.sprite.Sprite):
    def __init__(self,pos, surf, groups, z = LAYERS["main"]):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.z = z
        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.2, -self.rect.height * 0.75)

class Interaction(Generic):
    def __init__(self, pos, size, groups, name):
        surf = pygame.Surface(size)
        super().__init__(pos, surf, groups)
        self.name = name


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

class Particle(Generic):
    def __init__(self, pos, surf, groups, z, duration = 200):
        super().__init__(pos, surf, groups, z)
        self.start_time = pygame.time.get_ticks()
        self.duration = duration

        #white surface
        mask_surf = pygame.mask.from_surface(self.image)
        new_surf = mask_surf.to_surface()
        new_surf.set_colorkey((0, 0, 0))
        self.image = new_surf


    def update(self, dt):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time > self.duration:
            self.kill()

class WildFlower (Generic):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)

class Tree(Generic):
    def __init__(self, pos, surf, groups, name, player_add_item):
        super().__init__(pos, surf, groups)

        # tree attributes
        self.health = 5
        self.alive = True
        self.original_pos = pos  # Lưu vị trí ban đầu của cây
        self.shake_offset = 0  # Biến lưu trạng thái "rung"
        self.shake_direction = 1  # Hướng rung
        self.shake_amplitude = 5  # Độ rung (pixel)

        # Timer for shaking
        self.shake_timer = Timer(50)  # Rung trong 50ms

        stump_path = f'../graphics/stumps/{"small" if name == "Small" else "large"}.png'
        self.stump_surf = pygame.image.load(stump_path).convert_alpha()
        self.invul_timer = Timer(200)

        # apples
        self.apple_surf = pygame.image.load('../graphics/fruit/apple.png')
        self.apple_pos = APPLE_POS[name]
        self.apple_sprites = pygame.sprite.Group()
        self.create_fruit()
        self.player_add_item = player_add_item

    def damage(self):

        # damaging the tree
        self.health -= 1
        if not self.shake_timer.active:
            self.shake_timer.activate()

        # remove an apple
        if len(self.apple_sprites.sprites()) > 0:
            random_apple = choice(self.apple_sprites.sprites())
            Particle(pos=random_apple.rect.topleft,
                     surf=random_apple.image,
                     groups=self.groups()[0],
                     z=LAYERS['fruit'])
            self.player_add_item('apple')
            random_apple.kill()

    def shake(self):
        if self.shake_timer.active:
            # Thay đổi vị trí cây mỗi khi rung
            self.shake_offset += self.shake_direction * self.shake_amplitude
            self.shake_direction *= -1  # Đổi hướng rung
            self.rect.x = self.original_pos[0] + self.shake_offset  # Cập nhật vị trí rung

            # Kiểm tra xem timer có hết thời gian chưa
            self.shake_timer.update()

            # Nếu timer đã hết, dừng rung và trả về vị trí gốc
            if not self.shake_timer.active:
                self.rect.x = self.original_pos[0]  # Đảm bảo vị trí đúng
                self.shake_offset = 0

    def check_death(self):
        if self.health <= 0:
            self.image = self.stump_surf
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
            self.hitbox = self.rect.copy().inflate(-10, -self.rect.height * 0.6)
            self.alive = False
            self.player_add_item('wood')

    def update(self, dt):
        if self.alive:
            self.shake()
            self.check_death()

    def create_fruit(self):
        if not self.alive:
            return
        for pos in self.apple_pos:
            if randint(0, 10) < 8:
                x = pos[0] + self.rect.left
                y = pos[1] + self.rect.top
                print(f"Creating apple at ({x}, {y})")
                # Use the Tree instance's apple_sprites group
                Generic(
                    pos=(x, y),
                    surf=self.apple_surf,
                    groups=[self.apple_sprites, self.groups()[0]],
                    z=LAYERS['fruit'])

