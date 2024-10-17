import pygame
from settings import *
from pytmx.util_pygame import load_pygame
from support import *
from random import choice

class SoilLayer:
    def __init__(self, all_sprites):

        # sprite groups
        self.all_sprites = all_sprites
        self.soil_sprites = pygame.sprite.Group()
        self.water_sprites = pygame.sprite.Group()

        #graphic
        self.soil_surfs = import_folder_dict("../graphics/soil/")
        self.soil_surf = pygame.image.load("../graphics/soil/o.png")
        self.water_surfs = import_folder('../graphics/soil_water')

        self.create_soil_grid()
        self.create_hit_rects()

    def create_soil_grid(self):
        ground = pygame.image.load("../graphics/world/ground.png")

        #get the number of tiles horizontally and vertically
        h_tiles = ground.get_width() // TILE_SIZE  #128
        v_tiles = ground.get_height() // TILE_SIZE #80
        print(h_tiles, v_tiles)

        self.grid = [[[] for col in range (h_tiles)] for row in range (v_tiles)]
        for x, y, _ in load_pygame("../data/map.tmx").get_layer_by_name("Farmable").tiles():
            self.grid[y][x].append('F')

        # #log farmable tiles
        for row in self.grid:
            print(row)

    def create_hit_rects(self):
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
                    if self.raining:
                        self.water_all()

    def water(self, target_pos):
        for soil_sprite in self.soil_sprites.sprites():
            if soil_sprite.rect.collidepoint(target_pos):
                x = soil_sprite.rect.x // TILE_SIZE
                y = soil_sprite.rect.y // TILE_SIZE
                self.grid[y][x].append('U')

                pos = soil_sprite.rect.topleft
                surf = choice(self.water_surfs)
                WaterTile(pos, surf, [self.all_sprites, self.water_sprites])

    def water_all(self):
        for index_row, row in enumerate(self.grid):
            for index_col, cell in enumerate(row):
                if 'X' in cell and 'U' not in cell:
                    cell.append('U')
                    x = index_col * TILE_SIZE
                    y = index_row * TILE_SIZE
                    WaterTile((x, y), choice(self.water_surfs), [self.all_sprites, self.water_sprites])

    def remove_water(self):

        # destroy all water sprites
        for sprite in self.water_sprites.sprites():
            sprite.kill()

        # clean up the grid
        for row in self.grid:
            for cell in row:
                if 'U' in cell:
                    cell.remove('U')

    def create_soil_tiles(self):
        self.soil_sprites.empty()
        for index_row, row in enumerate(self.grid):
            for index_col, cell in enumerate(row):
                if 'X' in cell:
                    # 4 ô đất trên dưới -trái phải hiền với ô hiện tại
                    top = 'X' in self.grid[index_row - 1][index_col]
                    bottom = 'X' in self.grid[index_row + 1][index_col]
                    left = 'X' in self.grid[index_row][index_col - 1]
                    right = 'X' in self.grid[index_row][index_col + 1]

                    tile_type = 'o' # mặc định (ô đất có viền bo tròn 4 cạnh)

                    # kiểm tra các ô trên dưới - trái phải đã tạo đất trồng chưa để chọn đúng hình ảnh ô đất
                    # nếu toàn bộ trên duới trái phải là đất
                    if all((top, right, left, bottom)):
                        tile_type = 'x' #ô giữa trong bảng 3x3

                    # nếu ô bên trái là đất (còn lại thì không)
                    if left and not any((top, bottom, right)):
                        tile_type = 'r' # ô ngoài cùng bên phải
                    # nếu ô bên phải là đất (còn lại thì không)
                    if right and not any((top, bottom, left)):
                        tile_type = 'l' # ô ngoài cùng bên trái
                    #nếu 2 ô trái phải là đất (trên dưới thì không)
                    if left and right and not any((top, bottom)):
                        tile_type = 'lr' # ô ở giữa 1 hàng

                    # nếu ô bên trên là đất (còn lại thì không)
                    if top and not any((bottom, left, right)):
                        tile_type = 'b'  # ô dưới cùng
                    # nếu ô bên dưới là đất (còn lại thì không)
                    if bottom and not any((top, left, right)):
                         tile_type = 't'  # ô trên cùng
                    # nếu 2 ô trên dưới là đất (trái phải thì không)
                    if top and bottom and not any((left, right)):
                        tile_type = 'tb'  # ô ở giữa 1 cột

                    # nếu 2 ô trái và dưới là đất (còn lại thì không)
                    if left and bottom and not any((top, right)):
                        tile_type = 'tr'  # ô trên cùng bên phải
                    # nếu 2 ô trái và trên là đất (còn lại thì không)
                    if left and top and not any((bottom, right)):
                        tile_type = 'br'  # ô dưới cùng bên phải
                    # nếu 2 ô phải và dưới là đất (còn lại thì không)
                    if right and bottom and not any((top, left)):
                        tile_type = 'tl'  # ô trên cùng bên trái
                    # nếu 2 ô phải và trên là đất (còn lại thì không)
                    if right and top and not any((bottom, left)):
                         tile_type = 'bl'  # ô trên cùng bên trái

                    # nếu các ô đát tạo thành hình chữ T (|-)
                    if all ((top, bottom, right)) and not left:
                        tile_type = 'tbr'
                    # nếu các ô đát tạo thành hình chữ T (-|)
                    if all((top, bottom, left)) and not right:
                        tile_type = 'tbl'
                    # nếu các ô đát tạo thành hình chữ T xuôi
                    if all((left, right, bottom)) and not top:
                         tile_type = 'lrt'
                    # nếu các ô đát tạo thành hình chữ T ngược xuồng dưới
                    if all((left, right, top)) and not bottom:
                        tile_type = 'lrb'


                    SoilTile(
                        pos = (index_col * TILE_SIZE, index_row * TILE_SIZE),
                        surf = self.soil_surfs[tile_type],
                        #surf=self.soil_surfs,
                        groups = [self.all_sprites, self.soil_sprites]
                    )


class SoilTile (pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.z = LAYERS['soil']

class WaterTile(pygame.sprite.Sprite):
	def __init__(self, pos, surf, groups):
		super().__init__(groups)
		self.image = surf
		self.rect = self.image.get_rect(topleft = pos)
		self.z = LAYERS['soil water']