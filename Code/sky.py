import pygame
from settings import *
from support import import_folder
from sprites import Generic
from random import randint, choice
#hien

import pygame
from settings import *


class RainOverlay:
    def __init__(self, opacity=100):
        # Lấy màn hình hiện tại
        self.display_surface = pygame.display.get_surface()
        # Tạo một surface với kích thước toàn màn hình
        self.overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        # Màu phủ, có thể là màu xám (ví dụ RGB: (100, 100, 100)) và độ trong suốt (opacity)
        self.color = (77, 77, 77)
        # Điều chỉnh độ trong suốt của ảnh mờ
        self.overlay.set_alpha(opacity)

    def display(self):
        # Tô màu cho surface
        self.overlay.fill(self.color)

        # Dùng cờ BLEND_RGB_MULT để tạo hiệu ứng phủ mờ
        self.display_surface.blit(self.overlay, (0, 0))


class Sky:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.full_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))  # Thay đổi ở đây
        self.start_color = [255, 255, 255]
        self.end_color = (38, 101, 189)

        self.time = 0

    def display(self, dt, OnUI):
        if not OnUI:
            self.time += dt
            for index, value in enumerate(self.end_color):
                if self.start_color[index] > value:
                    #300s dau tien chay toc do 0.4, con lai chay toc do 1
                    if self.time <= 270:
                        self.start_color[index] -= 0.4 * dt
                    else:
                        self.start_color[index] -= 1 * dt

        self.full_surf.fill(self.start_color)
        self.display_surface.blit(self.full_surf, (0, 0), special_flags = pygame.BLEND_RGBA_MULT)



class Drop(Generic):
    def __init__(self, surf, pos, moving, groups, z):

        # general setup
        super().__init__(pos, surf, groups, z)
        self.lifetime = randint(400, 500)
        self.start_time = pygame.time.get_ticks()

        # moving
        self.moving = moving
        if self.moving:
            self.pos = pygame.math.Vector2(self.rect.topleft)
            self.direction = pygame.math.Vector2(-2, 4)
            self.speed = randint(200, 250)

    def update(self, dt):
        # movement
        if self.moving:
            self.pos += self.direction * self.speed * dt
            self.rect.topleft = (round(self.pos.x), round(self.pos.y))

        # timer
        if pygame.time.get_ticks() - self.start_time >= self.lifetime:
            self.kill()


class Rain:
    def __init__(self, all_sprites):
        self.all_sprites = all_sprites
        self.rain_drops = import_folder('../graphics/rain/drops/')
        self.rain_floor = import_folder('../graphics/rain/floor/')
        self.floor_w, self.floor_h = pygame.image.load('../graphics/world/ground.png').get_size()

    def create_floor(self):
        Drop(
            surf=choice(self.rain_floor),
            pos=(randint(0, self.floor_w), randint(0, self.floor_h)),
            moving=False,
            groups=self.all_sprites,
            z=LAYERS['rain floor'])

    def create_drops(self):
        Drop(
            surf=choice(self.rain_drops),
            pos=(randint(0, self.floor_w), randint(0, self.floor_h)),
            moving=True,
            groups=self.all_sprites,
            z=LAYERS['rain drops'])

    def update(self):
        for _ in range(20):
            self.create_floor()
            self.create_drops()
