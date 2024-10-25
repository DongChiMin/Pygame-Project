import pygame
from settings import *

class DialogueManager:
    def __init__(self, screen):
        self.screen = screen
        self.dialogue_box = pygame.image.load('../graphics/UI/dialogue_box.png')
        self.dialogue_box_rect = self.dialogue_box.get_rect(midbottom=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20))

        # Trạng thái hội thoại
        self.dialogues = []  # Danh sách các câu thoại
        self.current_sentence = 0
        self.char_index = 0
        self.display_text = ""
        self.text_speed = 50  # Tốc độ hiển thị ký tự (khoảng thời gian giữa các ký tự)
        self.time_since_last_char = 0
        self.in_dialogue = False

    def start_dialogue(self, dialogues):
        """Bắt đầu hội thoại mới với danh sách câu truyền vào"""

        self.dialogues = dialogues
        self.current_sentence = 0
        self.char_index = 0
        self.display_text = ""
        self.in_dialogue = True

    def advance_sentence(self):
        """Chuyển sang câu tiếp theo hoặc kết thúc hội thoại"""
        if self.char_index < len(self.dialogues[self.current_sentence]):
            # Nếu câu chưa hiển thị hết, hiện toàn bộ
            self.display_text = self.dialogues[self.current_sentence]
            self.char_index = len(self.display_text)
        else:
            # Chuyển câu
            self.current_sentence += 1
            if self.current_sentence < len(self.dialogues):
                self.char_index = 0
                self.display_text = ""
            else:
                self.in_dialogue = False  # Kết thúc hội thoại

    def update(self, dt):
        """Cập nhật số ký tự cần hiển thị"""
        if self.in_dialogue:
            self.time_since_last_char += dt
            if self.time_since_last_char > self.text_speed and self.char_index < len(
                    self.dialogues[self.current_sentence]):
                self.display_text += self.dialogues[self.current_sentence][self.char_index]
                self.char_index += 1
                self.time_since_last_char = 0

    def draw(self):
        """Vẽ hộp hội thoại và văn bản lên màn hình"""
        if self.in_dialogue:
            self.screen.blit(self.dialogue_box, self.dialogue_box_rect)
            font = pygame.font.Font(None, 24)
            text_surface = font.render(self.display_text, True, (0, 0, 0))
            self.screen.blit(text_surface, (self.dialogue_box_rect.x + 10, self.dialogue_box_rect.y + 10))
