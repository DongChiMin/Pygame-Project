import pygame
from settings import *
from pytmx.util_pygame import load_pygame

class SoilLayer:
    def __init__(self, all_sprites):

        # sprite groups
        self.all_sprites = all_sprites
        self.soil_sprites = pygame.sprite.Group()

        #graphic
        self.soil_surf = pygame.image.load("../graphics/soil/o.png")
        self.create_soil_grid()
        self.creat_hit_rects()

    def create_soil_grid(self):
        ground = pygame.image.load("../graphics/world/ground.png")

        #get the number of tiles horizontally and vertically
        h_tiles = ground.get_width() // TILE_SIZE  #128
        v_tiles = ground.get_height() // TILE_SIZE #80
        print(h_tiles, v_tiles)

        self.grid = [[[] for col in range (h_tiles)] for row in range (v_tiles)]
        for x, y, _ in load_pygame("../data/map.tmx").get_layer_by_name("Farmable").tiles():
            self.grid[y][x].append('F')

        #log farmable tiles
        # for row in self.grid:
        #     print(row)

    def creat_hit_rects(self):
        self.hit_rects = []
        #enumarate rows
        for index_row, row in enumerate(self.grid):
            for index_col, cell in enumerate(row):
                if 'F' in cell:
                    x = index_col * TILE_SIZE
                    y = index_row * TILE_SIZE
                    rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                    self.hit_rects.append(rect)

    def get_hit(self, point):
        for rect in self.hit_rects:
            # kiểm tra tọa độ chuẩn đang nằm tại tiles bao nhiêu
            if rect.collidepoint(point):
                x = rect.x // TILE_SIZE
                y = rect.y // TILE_SIZE
                if 'F' in self.grid[y][x]:
                    print("Soil tile = farmable")
                    self.grid[y][x].append('X')
                    self.create_soil_tiles()

    def create_soil_tiles(self):
        self.soil_sprites.empty()
        for index_row, row in enumerate(self.grid):
            for index_col, cell in enumerate(row):
                if 'X' in cell:
                    SoilTile(
                        pos = (index_col * TILE_SIZE, index_row * TILE_SIZE),
                        surf = self.soil_surf,
                        groups = [self.all_sprites, self.soil_sprites]
                    )


class SoilTile (pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.z = LAYERS['soil']

