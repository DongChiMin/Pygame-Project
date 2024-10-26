# UI.py
from idna import check_hyphen_ok

from settings import *
from timer import *
from dialogue_manager import DialogueManager
import pygame

COLOR_BASE_1 = (232, 207, 166)
COLOR_BASE_2 = (220, 185, 138)
COLOR_BASE_1_LIGHT = (244,227,200)
COLOR_MAIN = (170, 121, 89)
WHITE = (255,255,255)


class ui:
    def __init__(self, player, overlay, level):
        self.player = player  # Giả sử bạn cần truy cập vào đối tượng player
        self.overlay = overlay

        self.level = level

        #font chữ
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font('../font/SproutLand.ttf', size=30)

        #hội thoại
        self.dialogue_manager = DialogueManager(self.display_surface)
        # Tải hình ảnh cho nền hội thoại và khung hình chữ nhật
        self.dialogue_bg = pygame.image.load('../graphics/ui/dialogue_bg.png').convert_alpha()
        self.dialogue_frame = pygame.image.load('../graphics/ui/dialogue_frame.png').convert_alpha()
        self.trader_avt = pygame.image.load('../graphics/ui/trader_avt.png').convert_alpha()
        self.guide_avt = pygame.image.load('../graphics/ui/guide_avt.png').convert_alpha()


        # Thêm thuộc tính cho ngày
        self.current_day = 1  # Ngày bắt đầu
        self.day_changing = False

        # Thời gian ban đầu
        self.current_hour = 6  # 6:00 sáng
        self.current_minute = 0  # 0 phút
        self.time_running = True  # Biến để kiểm soát thời gian chạy
        # Biến để điều chỉnh tốc độ thời gian
        self.time_speed = 1200  # Số mili giây giữa các lần cập nhật phút
        self.last_time_update = pygame.time.get_ticks()  # Thời gian của lần cập nhật cuối

        # Khởi tạo danh sách hiển thị item
        self.item_display = []  # Danh sách chứa các item hiển thị
        self.display_time = 4000  # Thời gian hiển thị (ms)
        self.start_time = None  # Thời gian bắt đầu hiển thị
        self.active = False  # Trạng thái hiển thị
        self.item_display = []  # Danh sách quản lý hiển thị item

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

    def set_sleep_time(self):
        # Thiết lập giờ và phút sau khi người chơi ngủ
        self.current_hour = 6  # Đặt lại giờ về 6:00 sáng
        self.current_minute = 0  # Đặt lại phút về 0
        self.time_running = True  # Bắt đầu lại thời gian chạy

    def change_day(self):
        if self.player.sleep:
            self.day_changing = True
        if self.day_changing and self.level.time_changeable:
            self.day_changing = False
            self.level.time_changeable = False
            self.current_day +=1
            self.set_sleep_time()

    def draw_time(self):
            # Chuyển đổi giờ và phút thành định dạng chuỗi
            time_text = f"{int(self.current_hour)}:{int(self.current_minute):02d}"
            self.draw_text_with_outline(time_text, 100, 50, WHITE, COLOR_MAIN)  # Vẽ giờ ở vị trí (100, 50)

            # Vẽ ngày
            day_text = f"Day {self.current_day}"  # Định dạng chuỗi ngày
            self.draw_text_with_outline(day_text, 100, 80, WHITE, COLOR_MAIN)  # Vẽ ngày ở vị trí (100, 80)

    def add_item_display(self, item_image):
        # Mỗi item là một dictionary chứa thông tin về hình ảnh, alpha, và thời gian
        item_info = {
            'image': item_image,  # Thay 'image' thành 'item_image' cho đúng với tham số
            'alpha': 255,  # Độ mờ bắt đầu từ 255 (hoàn toàn hiển thị)
            'timer': Timer(2000),  # Thời gian hiển thị là 2 giây
            'position': (50, SCREEN_HEIGHT - 100 - len(self.item_display) * 70),  # Tính vị trí để không chồng lên
        }
        self.item_display.append(item_info)
        item_info['timer'].activate()  # Kích hoạt timer

    def update_item_display(self):
        for item in self.item_display[:]:  # Duyệt qua từng item trong danh sách
            if item['timer'].active:
                item['timer'].update()  # Cập nhật thời gian
            else:
                item['alpha'] -= 5  # Giảm alpha dần sau khi hết thời gian hiển thị
                if item['alpha'] <= 0:  # Nếu alpha <= 0 thì loại bỏ item
                    self.item_display.remove(item)

    def draw_item_display(self):
        for item in self.item_display:
            # Tạo bản sao của hình ảnh để chỉnh alpha
            item_image = item['image'].copy()
            item_image.set_alpha(item['alpha'])  # Cập nhật độ mờ (alpha)

            # Vẽ hình ảnh tại vị trí cụ thể
            self.display_surface.blit(item_image, item['position'])

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
            self.draw_text_with_outline(item, start_x + index * item_spacing, start_y, WHITE, COLOR_MAIN)

    def draw_text_with_outline(self, text, x, y, stroke, color):
        # Vẽ viền
        outline_text_surf = self.font.render(text, False, stroke)  # Màu viền (color)
        outline_rect = outline_text_surf.get_rect(center=(x, y))

        # Vẽ viền xung quanh bằng cách dịch chuyển
        self.display_surface.blit(outline_text_surf, outline_rect.move(-3, 0))
        self.display_surface.blit(outline_text_surf, outline_rect.move(3, 0))
        self.display_surface.blit(outline_text_surf, outline_rect.move(0, -3))
        self.display_surface.blit(outline_text_surf, outline_rect.move(0, 3))

        # Vẽ chữ chính
        text_surf = self.font.render(text, False, color)  # Màu chữ chính
        self.display_surface.blit(text_surf, outline_rect)

    def draw_exit_button(self):
        # vẽ nút exit
        if self.check_hover(self.exit_button_rect):
            self.display_surface.blit(self.exit_button_hover_surf, self.exit_button_rect)
        else:
            self.display_surface.blit(self.exit_button_surf, self.exit_button_rect)
        if self.exit_button_rect not in self.active_ui_rects:
            self.active_ui_rects.append(self.exit_button_rect)

    #HỘI THOẠI
    def start_dialogue(self, dialogues, action):
        """Gọi hội thoại từ lớp DialogueManager"""
        self.dialogue_manager.start_dialogue(dialogues, action)

    def update_dialogue(self, dt):
        """Cập nhật hội thoại"""
        self.dialogue_manager.update(dt)

    def draw_dialogue(self):
        """Hiển thị UI"""
        if self.dialogue_manager.in_dialogue:
            # Vẽ nền hội thoại
            bg_rect = self.dialogue_bg.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150))
            self.display_surface.blit(self.dialogue_bg, bg_rect)

            # Vẽ khung hình chữ nhật cho hội thoại
            frame_rect = self.dialogue_frame.get_rect(center=(SCREEN_WIDTH // 2 - 240, SCREEN_HEIGHT - 150))
            self.display_surface.blit(self.dialogue_frame, frame_rect)

            # Vẽ hình đại diện của Trader hoặc Guide
            collied_interaction_sprite = pygame.sprite.spritecollide(self.player, self.player.interaction, False)
            if collied_interaction_sprite:
                if collied_interaction_sprite[0].name == 'Trader':
                    avt_rect = self.trader_avt.get_rect(center=frame_rect.center)
                    self.display_surface.blit(self.trader_avt, avt_rect)
                    # Vẽ tên Trader dưới hình đại diện
                    self.draw_text_with_outline("Trader", frame_rect.centerx,
                                                avt_rect.bottom + 20, COLOR_MAIN, COLOR_BASE_1_LIGHT)  # Điều chỉnh vị trí nếu cần
                elif collied_interaction_sprite[0].name == 'Guide':
                    avt_rect = self.guide_avt.get_rect(center=frame_rect.center)
                    self.display_surface.blit(self.guide_avt, avt_rect)
                    # Vẽ tên Guide dưới hình đại diện
                    self.draw_text_with_outline("Guide", frame_rect.centerx,
                                                avt_rect.bottom + 20, COLOR_MAIN, COLOR_BASE_1_LIGHT)  # Điều chỉnh vị trí nếu cần

        self.dialogue_manager.draw()  # Vẽ hội thoại

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

    def player_keyboard(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_f]:
            collied_interaction_sprite = pygame.sprite.spritecollide(self.player, self.player.interaction, False)
            if collied_interaction_sprite:
                if collied_interaction_sprite[0].name == 'Trader':
                    dialogues = ["Chao ban!", "Ban khoe chu!", "Toi co mot vai mon hang can trao doi day." , "Xem di nhe!"]
                    self.start_dialogue(dialogues, self.player.open_trader)  # Bắt đầu hội thoại mới
                elif collied_interaction_sprite[0].name == 'Guide':
                    dialogues = ["Chao ban!", "Cong viec hom nay the nao roi", "Ban hay trong va thu hoach 5 lua mi va 5 ca chua truoc nhe" , "Toi se doi!"]
                    self.start_dialogue(dialogues, self.player.end_conservation)  # Bắt đầu hội thoại mới
        if keys[pygame.K_RETURN] and self.dialogue_manager.in_dialogue:
            self.dialogue_manager.advance_sentence()  # Chuyển câu thoại

    def remove_ui_elements(self):
        if self.exit_button_rect in self.active_ui_rects:
            self.active_ui_rects.remove(self.exit_button_rect)
        if self.ui_backpack_rect in self.active_ui_rects:
            self.active_ui_rects.remove(self.ui_backpack_rect)

    def run(self):

        self.draw_UI()
        self.handle_event()

        self.player_click()
        self.player_keyboard()
        self.check_mouse_collision()
        # print(self.active_ui_rects)



        # Vẽ giờ
        self.time_on()
        self.draw_time()

        #cập nhật ngày
        self.change_day()

        # Cập nhật và vẽ item hiển thị
        self.update_item_display()
        self.draw_item_display()


        if self.opening_backpack:
            self.draw_ui_backpack()

        #delay 0.5s trước khi tắt UI backpack
        self.remove_backpack_ui.update()

        #hội thoại
        self.dialogue_manager.handle_input()
        dt = pygame.time.Clock().tick(165) / 1000
        self.update_dialogue(dt)
        self.draw_dialogue()



        # Draw mouse cursor
        mouse_x, mouse_y = pygame.mouse.get_pos()  # Get mouse position
        self.cursor_rect.topleft = (mouse_x, mouse_y)  # Update position
        self.display_surface.blit(self.cursor_surf, self.cursor_rect)