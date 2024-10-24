# UI.py
from idna import check_hyphen_ok

from settings import *
from timer import *
from menu import Menu
import pygame

COLOR_BASE_1 = (232, 207, 166)
COLOR_BASE_2 = (220, 185, 138)
COLOR_MAIN = (170, 121, 89)


class ui:
    def __init__(self, player, overlay, level):
        self.player = player  # Giả sử bạn cần truy cập vào đối tượng player
        self.overlay = overlay

        self.level = level

        #font chữ
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font('../font/SproutLand.ttf', size=30)

        # Thêm thuộc tính cho ngày
        self.current_day = 1  # Ngày bắt đầu
        # Tạo một Timer cho việc thay đổi ngày
        self.day_change_timer = Timer(4000, self.change_day)  # Đặt độ trễ là 2000 ms (2 giây)

        # Thời gian ban đầu
        self.current_hour = 6  # 6:00 sáng
        self.current_minute = 0  # 0 phút
        self.time_running = True  # Biến để kiểm soát thời gian chạy
        # Biến để điều chỉnh tốc độ thời gian
        self.time_speed = 1200  # Số mili giây giữa các lần cập nhật phút
        self.last_time_update = pygame.time.get_ticks()  # Thời gian của lần cập nhật cuối
        # Tạo một Timer để thiết lập giờ, phút và trạng thái
        self.sleep_timer = Timer(4000, self.set_sleep_time)  # Đặt độ trễ là 2000 ms (2 giây)

        # Khởi tạo danh sách hiển thị item
        self.item_display = []  # Danh sách chứa các item hiển thị
        self.display_time = 4000  # Thời gian hiển thị (ms)
        self.start_time = None  # Thời gian bắt đầu hiển thị
        self.active = False  # Trạng thái hiển thị

        #weather icon
        self.sunny_icon_surf = pygame.image.load('../graphics/ui/sunny.png').convert_alpha()
        self.rainy_icon_surf = pygame.image.load('../graphics/ui/rainy.png').convert_alpha()
        self.weather_icon_rect = self.sunny_icon_surf.get_rect(topright=OVERLAY_POSITIONS['weather icon'])

        #weather ui
        self.weather_ui_surf = pygame.image.load('../graphics/ui/weather.png').convert_alpha()
        self.weather_ui_rect = self.weather_ui_surf.get_rect(topright = OVERLAY_POSITIONS['weather'])

        #coin info ui
        self.coin_info_surf = pygame.image.load('../graphics/ui/coin_info.png').convert_alpha()
        self.coin_info_rect = self.coin_info_surf.get_rect(topright = OVERLAY_POSITIONS['coin info'])

        #backpack
        self.backpack_button_surf = pygame.image.load('../graphics/overlay/square.png').convert_alpha()  # Vị trí và kích thước của nút "Backpack"
        self.backpack_button_hover_surf = pygame.image.load('../graphics/overlay/highlight_square.png').convert_alpha()
        self.backpack_button_rect = self.backpack_button_surf.get_rect(bottomright = OVERLAY_POSITIONS['backpack'])

        self.backpack_icon_surf = pygame.image.load('../graphics/overlay/backpack.png').convert_alpha()
        self.backpack_icon_rect = self.backpack_icon_surf.get_rect(bottomright = OVERLAY_POSITIONS['backpack'])

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

        #vẽ backpack icon
        self.display_surface.blit(self.backpack_icon_surf, self.backpack_icon_rect)

        #vẽ Icon weather
        if self.level.raining:
            self.display_surface.blit(self.rainy_icon_surf, self.weather_icon_rect)
        else:
            self.display_surface.blit(self.sunny_icon_surf, self.weather_icon_rect)

        #Vẽ UI weather
        self.display_surface.blit(self.weather_ui_surf, self.weather_ui_rect)

        #vẽ coin info
        self.display_surface.blit(self.coin_info_surf, self.coin_info_rect)

        #vẽ số coin
        coin_text_surf = self.font.render(f"{self.player.money}", False, (170, 121, 89))
        coin_text_rect = coin_text_surf.get_rect(midright =(SCREEN_WIDTH -33, 223))
        self.display_surface.blit(coin_text_surf, coin_text_rect)

    def time_on(self):
        # Cập nhật phút nếu thời gian đang chạy
        if self.time_running and not self.ui_opened:
            current_time = pygame.time.get_ticks()  # Lấy thời gian hiện tại

            if current_time - self.last_time_update >= self.time_speed:  # Kiểm tra nếu đủ thời gian để cập nhật
                self.last_time_update = current_time  # Cập nhật thời gian lần cập nhật cuối

                self.current_minute += 10  # Tăng phút
                if self.current_minute >= 60:  # Nếu phút đạt 60
                    self.current_minute = 0  # Reset phút
                    self.current_hour += 1  # Tăng giờ

                    # Reset giờ nếu đạt 24
                    if self.current_hour >= 24:  # Quay về 0:00
                        self.current_hour = 0

                    # Dừng khi đạt 4:00
                    if self.current_hour == 4:
                        self.time_running = False  # Dừng chạy thời gian

        # Kiểm tra nếu người chơi đang ngủ
        if self.player.sleep:
            # Kích hoạt Timer để thiết lập giờ, phút và trạng thái
            if not self.sleep_timer.active:  # Nếu Timer chưa hoạt động
                self.sleep_timer.activate()  # Kích hoạt Timer

            # Kích hoạt Timer để thay đổi ngày
            if not self.day_change_timer.active:  # Nếu Timer chưa hoạt động
                self.day_change_timer.activate()  # Kích hoạt Timer

    def set_sleep_time(self):
        # Thiết lập giờ và phút sau khi người chơi ngủ
        self.current_hour = 6  # Đặt lại giờ về 6:00 sáng
        self.current_minute = 0  # Đặt lại phút về 0
        self.time_running = True  # Bắt đầu lại thời gian chạy

    def change_day(self):
        # Tăng ngày mỗi khi Timer hoàn tất
        self.current_day += 1  # Tăng ngày

    def draw_time(self):
            # Chuyển đổi giờ và phút thành định dạng chuỗi
            time_text = f"{int(self.current_hour)}:{int(self.current_minute):02d}"
            self.draw_text_with_outline(time_text, 100, 50)  # Vẽ giờ ở vị trí (100, 50)

            # Vẽ ngày
            day_text = f"Day {self.current_day}"  # Định dạng chuỗi ngày
            self.draw_text_with_outline(day_text, 100, 80)  # Vẽ ngày ở vị trí (100, 80)

    def add_item_display(self, item_image):
        self.item_display.append(item_image)
        if not self.active:
            self.start_time = pygame.time.get_ticks()
            self.active = True

    def update_item_display(self):
        if self.active:
            current_time = pygame.time.get_ticks()
            if current_time - self.start_time >= self.display_time:
                self.active = False
                self.item_display.clear()  # Xóa danh sách khi hết thời gian

    def draw_item_display(self):
        if self.active and self.item_display:
            for index, item in enumerate(self.item_display):
                # Tính toán độ mờ dần
                alpha = 255 - (255 * (pygame.time.get_ticks() - self.start_time) / self.display_time)
                item.set_alpha(alpha)  # Áp dụng độ mờ

                # Vẽ item ở góc dưới bên trái
                self.display_surface.blit(item, (50, SCREEN_HEIGHT - 100 - index * 32))  # Điều chỉnh vị trí nếu cần


    def draw_ui_backpack(self):
        #vẽ background backpack
        self.display_surface.blit(self.ui_backpack_surf, self.ui_backpack_rect)
        if self.ui_backpack_rect not in self.active_ui_rects:
            self.active_ui_rects.append(self.ui_backpack_rect)
        self.draw_exit_button()

        self.draw_inventory_items()

    def draw_inventory_items(self):
        # Tọa độ bắt đầu để vẽ item
        start_x = self.ui_backpack_rect.left + 100  # Bỏ qua một chút từ bên trái
        start_y = self.ui_backpack_rect.top + 230  # Bỏ qua một chút từ trên xuống

        # Khoảng cách giữa các mục
        item_spacing = 96  # Điều chỉnh khoảng cách giữa các mục theo chiều ngang

        # Tạo danh sách chứa các item và seed cần hiển thị
        items_and_seeds = []

        # Lấy các item từ inventory
        for item_name, amount in self.player.item_inventory.items():
            items_and_seeds.append(f"{amount}")

        # Lấy các seed từ seed_inventory
        for seed_name, amount in self.player.seed_inventory.items():
            items_and_seeds.append(f"{amount}")

        # Vẽ các items trong inventory
        for index, item in enumerate(items_and_seeds):
            # Vẽ chữ có viền
            self.draw_text_with_outline(item, start_x + index * item_spacing, start_y)

    def draw_text_with_outline(self, text, x, y):
        # Vẽ viền
        outline_text_surf = self.font.render(text, False, (255,255,255))  # Màu viền (đen)
        outline_rect = outline_text_surf.get_rect(center=(x, y))

        # Vẽ viền xung quanh bằng cách dịch chuyển
        self.display_surface.blit(outline_text_surf, outline_rect.move(-3, 0))
        self.display_surface.blit(outline_text_surf, outline_rect.move(3, 0))
        self.display_surface.blit(outline_text_surf, outline_rect.move(0, -3))
        self.display_surface.blit(outline_text_surf, outline_rect.move(0, 3))

        # Vẽ chữ chính
        text_surf = self.font.render(text, False, COLOR_MAIN)  # Màu chữ chính
        self.display_surface.blit(text_surf, outline_rect)



    def draw_exit_button(self):
        # vẽ nút exit
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
        keys = pygame.key.get_pressed()
        if mouses[0] == 1:
            #neu ui dang dong:
            if not self.ui_opened:
                if self.check_hover(self.backpack_button_rect):
                    self.opening_backpack = True
                    self.ui_opened = True
            #neu ui dang mo
            else:

                if self.check_hover(self.exit_button_rect):
                    #nếu đang mở backpack
                    if self.opening_backpack:
                        self.opening_backpack = False
                        self.ui_opened = False
                        self.remove_backpack_ui.activate()
        elif keys[pygame.K_ESCAPE]:
            if self.opening_backpack:
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



        # Vẽ giờ
        self.time_on()
        self.draw_time()
        self.day_change_timer.update()
        self.sleep_timer.update()

        # Cập nhật và vẽ item hiển thị
        self.update_item_display()
        self.draw_item_display()


        if self.opening_backpack:
            self.draw_ui_backpack()

        #delay 0.5s trước khi tắt UI backpack
        self.remove_backpack_ui.update()


        # Draw mouse cursor
        mouse_x, mouse_y = pygame.mouse.get_pos()  # Get mouse position
        self.cursor_rect.topleft = (mouse_x, mouse_y)  # Update position
        self.display_surface.blit(self.cursor_surf, self.cursor_rect)


