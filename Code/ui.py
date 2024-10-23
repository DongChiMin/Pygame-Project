# UI.py
from idna import check_hyphen_ok

from settings import *
from timer import *
import pygame

COLOR_BASE_1 = (232, 207, 166)
COLOR_BASE_2 = (220, 185, 138)
COLOR_MAIN = (170, 121, 89)


class ui:
    def __init__(self, player, overlay):
        self.player = player  # Giả sử bạn cần truy cập vào đối tượng player
        self.overlay = overlay

        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font('../font/SproutLand.ttf', size=30)

        #weather ui
        self.weather_ui_surf = pygame.image.load('../graphics/ui/weather.png').convert_alpha()
        self.weather_ui_rect = self.weather_ui_surf.get_rect(topright = OVERLAY_POSITIONS['weather'])

        #backpack
        self.backpack_button_surf = pygame.image.load('../graphics/overlay/square.png').convert_alpha()  # Vị trí và kích thước của nút "Backpack"
        self.backpack_button_hover_surf = pygame.image.load('../graphics/overlay/highlight_square.png').convert_alpha()
        self.backpack_button_rect = self.backpack_button_surf.get_rect(bottomright = OVERLAY_POSITIONS['backpack'])

        #vẽ chuột
        self.cursor_surf = pygame.image.load('../graphics/overlay/mouse_cursor.png').convert_alpha()
        self.cursor_rect = self.cursor_surf.get_rect()
        pygame.mouse.set_visible(False)

        #vẽ Bg backpack
        self.ui_backpack_surf = pygame.image.load('../graphics/ui/backpack.png').convert_alpha()
        self.ui_backpack_rect = self.ui_backpack_surf.get_rect(center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

        #vẽ nút exit
        self.exit_button_surf = pygame.image.load('../graphics/ui/exit_button.png').convert_alpha()
        self.exit_button_hover_surf = pygame.image.load('../graphics/ui/exit_button_hover.png').convert_alpha()
        self.exit_button_rect = self.exit_button_surf.get_rect(topright = (self.ui_backpack_rect.right - 32, self.ui_backpack_rect.top + 67))

        #các cờ (flags)
        self.ui_opened = False
        self.opening_backpack = False
        self.is_mouse_on_UI = False

        #list lưu các UI đang hiện
        self.active_ui_rects = []
        self.active_ui_rects.append(self.backpack_button_rect)
        self.active_ui_rects.append(self.overlay.center_tool_rect)
        self.active_ui_rects.append(self.overlay.center_seed_rect)

        #timer
        self.remove_backpack_ui = Timer(500, self.remove_ui_elements)
        

    # Hàm để vẽ UI lên màn hình
    def draw_UI(self):
        # Vẽ nút backpack
        if self.check_hover(self.backpack_button_rect):
            self.display_surface.blit(self.backpack_button_hover_surf, self.backpack_button_rect)  # Vẽ hình ảnh hover
        else:
            self.display_surface.blit(self.backpack_button_surf, self.backpack_button_rect)  # Vẽ hình ảnh bình thường

        #Vẽ UI weather
        self.display_surface.blit(self.weather_ui_surf, self.weather_ui_rect)



    def draw_ui_backpack(self):
        #vẽ background backpack
        self.display_surface.blit(self.ui_backpack_surf, self.ui_backpack_rect)
        if self.ui_backpack_rect not in self.active_ui_rects:
            self.active_ui_rects.append(self.ui_backpack_rect)

        #vẽ nút exit
        if self.check_hover(self.exit_button_rect):
            self.display_surface.blit(self.exit_button_hover_surf, self.exit_button_rect)
        else:
            self.display_surface.blit(self.exit_button_surf, self.exit_button_rect)
        if self.exit_button_rect not in self.active_ui_rects:
            self.active_ui_rects.append(self.exit_button_rect)


    # Kiểm tra nếu con trỏ chuột đang hover lên một phần tử UI
    def check_hover(self, rect):
        mouse_pos = pygame.mouse.get_pos()  # Lấy vị trí chuột
        if rect.collidepoint(mouse_pos):
            return True  # Trả về true nếu con trỏ đang hover lên nút này
        return False


    # Hàm kiểm tra va chạm với mọi UI đang mở
    def check_mouse_collision(self):
        self.is_mouse_on_UI = False
        for rect in self.active_ui_rects:
            if self.check_hover(rect):
                self.is_mouse_on_UI = True
                break

    # Xử lý các sự kiện chuột
    def handle_event(self):
        mouses = pygame.mouse.get_pressed()
        if mouses[0] == 1:
            #neu ui dang dong:
            if not self.ui_opened:
                if self.check_hover(self.backpack_button_rect):
                    self.opening_backpack = True
                    self.ui_opened = True
            #neu ui dang mo
            else:
                if self.check_hover(self.exit_button_rect):
                    self.opening_backpack = False
                    self.ui_opened = False
                    self.remove_backpack_ui.activate()


    def player_click(self):
        # Kiểm tra nếu chuột trái được bấm khi không hover
        if pygame.mouse.get_pressed()[0] == 1 and not self.is_mouse_on_UI:
            self.player.timers['tool use'].activate()
            self.player.direction = pygame.math.Vector2()
            self.player.frame_index = 0

        # Kiểm tra nếu chuột phải được bấm khi không hover
        if pygame.mouse.get_pressed()[2] == 1 and not self.is_mouse_on_UI:
            self.player.timers['seed use'].activate()
            self.player.input_seed_use()

    def remove_ui_elements(self):
        if self.exit_button_rect in self.active_ui_rects:
            self.active_ui_rects.remove(self.exit_button_rect)
        if self.ui_backpack_rect in self.active_ui_rects:
            self.active_ui_rects.remove(self.ui_backpack_rect)


    def run(self):
        self.draw_UI()
        self.handle_event()

        self.player_click()
        self.check_mouse_collision()
        print(self.active_ui_rects)

        if self.opening_backpack:
            self.draw_ui_backpack()

        #delay 0.5s trước khi tắt UI backpack
        self.remove_backpack_ui.update()


        # Draw mouse cursor
        mouse_x, mouse_y = pygame.mouse.get_pos()  # Get mouse position
        self.cursor_rect.topleft = (mouse_x, mouse_y)  # Update position
        self.display_surface.blit(self.cursor_surf, self.cursor_rect)


