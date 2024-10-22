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
        self.font = pygame.font.Font('../font/SproutLand.ttf', size=28)
        self.backpack_button = pygame.Rect(50, 50, 150, 50)  # Vị trí và kích thước của nút "Backpack"

    # Hàm để vẽ UI lên màn hình
    def draw_ui(self, screen):
        # Vẽ nút Backpack
        pygame.draw.rect(screen, COLOR_BASE_1, self.backpack_button)  # Vẽ nút với màu xám
        text_surface = self.font.render('Backpack', True, COLOR_MAIN)
        screen.blit(text_surface, (self.backpack_button.x + 20, self.backpack_button.y + 10))

    # Kiểm tra nếu con trỏ chuột đang hover lên một phần tử UI
    def check_hover(self):
        mouse_pos = pygame.mouse.get_pos()  # Lấy vị trí chuột
        if self.backpack_button.collidepoint(mouse_pos):
            return 'backpack'  # Trả về 'backpack' nếu con trỏ đang hover lên nút này
        return None

    # Xử lý các sự kiện chuột
    def handle_event(self):
        mouses = pygame.mouse.get_pressed()
        if mouses[0] == 1:
            hover_item = self.check_hover()
            if hover_item == 'backpack':
                self.open_backpack()

    def open_backpack(self):
        # Thực hiện các hành động mở backpack ở đây
        print("Backpack opened")  # Bạn có thể thay thế bằng hành động thực tế

    def run(self):
        self.draw_ui(self.display_surface)
        self.handle_event()

