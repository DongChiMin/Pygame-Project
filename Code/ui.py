# UI.py
from settings import *
import pygame

COLOR_BASE_1 = (232, 207, 166)
COLOR_BASE_2 = (220, 185, 138)
COLOR_MAIN = (170, 121, 89)


class ui:
    def __init__(self, player):
        self.player = player  # Giả sử bạn cần truy cập vào đối tượng player

        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font('../font/SproutLand.ttf', size=30)


        #backpack
        self.backpack_button_surf = pygame.image.load('../graphics/overlay/square.png').convert_alpha()  # Vị trí và kích thước của nút "Backpack"
        self.backpack_button_hover_surf = pygame.image.load('../graphics/overlay/highlight_square.png').convert_alpha()
        self.backpack_button_rect = self.backpack_button_surf.get_rect(bottomright = OVERLAY_POSITIONS['backpack'])

        #vẽ chuột
        self.cursor_surf = pygame.image.load('../graphics/overlay/mouse_cursor.png').convert_alpha()
        self.cursor_rect = self.cursor_surf.get_rect()
        pygame.mouse.set_visible(False)

        #các cờ (flags)
        self.ui_opened = False
        self.opening_backpack = False

    # Hàm để vẽ UI lên màn hình
    def draw_button_backpack(self):
        # Kiểm tra nếu chuột đang hover lên nút ba lô
        if self.check_hover(self.backpack_button_rect):
            self.display_surface.blit(self.backpack_button_hover_surf, self.backpack_button_rect)  # Vẽ hình ảnh hover
        else:
            self.display_surface.blit(self.backpack_button_surf, self.backpack_button_rect)  # Vẽ hình ảnh bình thường

    def draw_ui_backpack(self):
        ui_backpack_surf = pygame.image.load('../graphics/ui/backpack.png').convert_alpha()
        ui_backpack_rect = ui_backpack_surf.get_rect(center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        self.display_surface.blit(ui_backpack_surf, ui_backpack_rect)

    # Kiểm tra nếu con trỏ chuột đang hover lên một phần tử UI
    def check_hover(self, rect):
        mouse_pos = pygame.mouse.get_pos()  # Lấy vị trí chuột
        if rect.collidepoint(mouse_pos):
            return True  # Trả về true nếu con trỏ đang hover lên nút này
        return False

    # Xử lý các sự kiện chuột
    def handle_event(self):
        mouses = pygame.mouse.get_pressed()
        if mouses[0] == 1 and not self.ui_opened:
            if self.check_hover(self.backpack_button_rect):
                self.opening_backpack = True
                self.ui_opened = True


    def run(self):
        self.draw_button_backpack()
        self.handle_event()
        if self.opening_backpack:
            self.draw_ui_backpack()



        # Draw mouse cursor
        mouse_x, mouse_y = pygame.mouse.get_pos()  # Get mouse position
        self.cursor_rect.topleft = (mouse_x, mouse_y)  # Update position
        self.display_surface.blit(self.cursor_surf, self.cursor_rect)


