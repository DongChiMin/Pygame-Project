import pygame
from settings import *

class DialogueManager:
    def __init__(self, screen):
        self.screen = screen
        self.dialogue_box = pygame.image.load('../graphics/UI/dialogue_box.png')
        self.dialogue_box_rect = self.dialogue_box.get_rect(midbottom=(SCREEN_WIDTH // 2 + 100, SCREEN_HEIGHT - 60))

        # Trạng thái hội thoại
        self.dialogues = []  # Danh sách các câu thoại
        self.current_sentence = 0
        self.char_index = 0
        self.display_text = ""
        self.lines = []  # Lưu các dòng văn bản đã được ngắt dòng
        self.text_speed = 0.005  # Thời gian giữa mỗi ký tự
        self.time_since_last_char = 0
        self.in_dialogue = False
        self.can_advance = False  # Cờ để kiểm soát việc nhấn Enter
        self.max_line_length = 25  # Số ký tự tối đa mỗi dòng
        self.callback = None  # Hàm callback

    def start_dialogue(self, dialogues, callback=None):
        """Bắt đầu hội thoại mới với danh sách câu truyền vào"""
        self.dialogues = dialogues
        self.current_sentence = 0
        self.char_index = 0
        self.display_text = ""
        self.lines = []  # Khởi tạo lại các dòng mới khi bắt đầu câu mới
        self.in_dialogue = True
        self.can_advance = False  # Không cho phép nhấn Enter ngay
        self.callback = callback  # Lưu hàm callback

    def advance_sentence(self):
        """Chuyển sang câu tiếp theo hoặc kết thúc hội thoại"""
        if self.can_advance:
            self.current_sentence += 1
            if self.current_sentence < len(self.dialogues):
                self.char_index = 0
                self.display_text = ""
                self.lines = []  # Xóa các dòng khi bắt đầu câu mới
                self.can_advance = False  # Đặt lại cờ
            else:
                self.in_dialogue = False  # Kết thúc hội thoại
                if self.callback:  # Gọi hàm callback nếu có
                    self.callback()
                self.in_dialogue = False  # Kết thúc hội thoại
                self.can_advance = False  # Không cho phép nhấn Enter nữa

    def handle_input(self):
        """Xử lý đầu vào từ người dùng"""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN] and self.can_advance:
            self.advance_sentence()

    def update(self, dt):
        """Cập nhật số ký tự cần hiển thị"""
        if self.in_dialogue:
            self.time_since_last_char += dt
            if self.time_since_last_char > self.text_speed and self.char_index < len(
                    self.dialogues[self.current_sentence]):
                self.display_text += self.dialogues[self.current_sentence][self.char_index]
                self.char_index += 1
                self.time_since_last_char = 0

            # Nếu đã hiện hết câu, cho phép nhấn Enter
            if self.char_index >= len(self.dialogues[self.current_sentence]):
                self.can_advance = True

            # Chia văn bản thành các dòng khi cần thiết
            self.lines = self.split_text_to_lines(self.display_text)

    def split_text_to_lines(self, text):
        """Chia văn bản thành các dòng, giữ các từ nguyên vẹn"""
        words = text.split(' ')
        lines = []
        current_line = ""

        for word in words:
            if len(current_line) + len(word) <= self.max_line_length:
                current_line += word + " "
            else:
                lines.append(current_line.strip())
                current_line = word + " "

        # Thêm dòng cuối cùng nếu có
        if current_line:
            lines.append(current_line.strip())

        return lines

    def draw(self):
        """Vẽ hộp hội thoại và văn bản lên màn hình"""
        if self.in_dialogue:
            self.screen.blit(self.dialogue_box, self.dialogue_box_rect)
            font = pygame.font.Font('../font/SproutLand.ttf', size=28)

            # Vẽ từng dòng ở vị trí thích hợp trong hộp hội thoại
            for i, line in enumerate(self.lines):
                text_surface = font.render(line, False, (170, 121, 89))
                self.screen.blit(
                    text_surface,
                    (self.dialogue_box_rect.x + 45, self.dialogue_box_rect.y + 30 + i * 35)  # Điều chỉnh khoảng cách dòng
                )
