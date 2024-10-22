import pygame
from pygame import Surface
from six import text_type

from settings import *

class Menu:
    def __init__(self, player, toggle_UI):

        #general setup
        self.player = player
        self.toggle_UI = toggle_UI
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font('../font/SproutLand.ttf', size = 28)
        self.exit_stroke = pygame.font.Font('../font/SproutLand.ttf', size = 32)

        #options
        self.width = 400
        self.space = 10
        self.padding = 8

        #entries
        self.options = list(self.player.item_inventory.keys()) + list(self.player.seed_inventory.keys())
        self.sell_border = len(self.player.item_inventory) - 1
            #sell border: kiem tra index neu < sell thi la vat pham sell duoc,
        self.setup()

        #movement
        self.index = 0

    def setup(self):
        #create the text surfaces
        self.text_surfs = []
        #total_height: tính toán độ cao khi in hết text là bao nhiêu
        self.total_height = 0

        for item in self.options:
            text_surf = self.font.render(item, False, (170, 121, 89))
            self.text_surfs.append(text_surf)
            #padding: khoảng cách giữa các dòng
            self.total_height += text_surf.get_height() + (self.padding * 2)

        #tạo thêm khoảng cách giữa hai text_surf
        self.total_height += (len(self.text_surfs) - 1) * self.space
        #lấy điểm neo chính giữa màn hình + dịch lên trên nửa total_height
        self.menu_top = SCREEN_HEIGHT / 2 - self.total_height / 2

        #lấy khung chữ nhật bao quanh menu
        self.main_rect = pygame.Rect(SCREEN_WIDTH / 2 - self.width / 2, self.menu_top,self.width,self.total_height)

    def display_money(self):
        text_surf = self.font.render( f"money: {self.player.money}",False,(170,121,89))
        text_rect = text_surf.get_rect(midtop = (SCREEN_WIDTH / 2, 25) )

        #inflate: hình chữ nhật bao quanh, 6: bo tròn
        pygame.draw.rect(self.display_surface, (170, 121, 89), text_rect.inflate(30, 30), 0, 6)
        pygame.draw.rect(self.display_surface, (232,207,166), text_rect.inflate(20,20),0 , 6)
        self.display_surface.blit(text_surf, text_rect)

    def input(self):
        #get the input
        #if the player press esc close the menu
        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            self.toggle_UI()


    def show_entry(self,text_surf ,amount, top, selected):
        #background
        bg_rect = pygame.Rect(self.main_rect.left + 15, top, self.width - 30, text_surf.get_height() + (self.padding * 2))
        pygame.draw.rect(self.display_surface, (232, 207, 166), bg_rect, 0, 4)

        #text
        text_rect = text_surf.get_rect(midleft = (self.main_rect.left + 30, bg_rect.centery))
        self.display_surface.blit(text_surf, text_rect)

        #amout
        amount_surf = self.font.render(str(amount), False, (170, 121, 89))
        amount_rect = amount_surf.get_rect(midright = (self.main_rect.right - 30, bg_rect.centery))
        self.display_surface.blit(amount_surf, amount_rect)

        #selected
        if selected:
            pygame.draw.rect(self.display_surface, 'White', bg_rect, 4, 4)

    def update(self):
        self.input()
        self.display_money()
        #enumerate: de lay ra duoc index cua item

        #in ra nền background
        bg_surf = pygame.image.load('../graphics/UI/rect_1.png').convert_alpha()
        bg_rect = bg_surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 30 ))
        self.display_surface.blit(bg_surf, bg_rect)

        exit_surf = pygame.image.load("../graphics/UI/exit_menu.png").convert_alpha()
        exit_rect = exit_surf.get_rect(topleft=(bg_rect.left + 12, bg_rect.top + 12))
        self.display_surface.blit(exit_surf, exit_rect)


        for text_index, text_surf in enumerate(self.text_surfs):
            top = self.main_rect.top + text_index * (text_surf.get_height() + (self.padding * 2) + self.space)
            amount_list = list(self.player.item_inventory.values()) + list(self.player.seed_inventory.values())
            amount = amount_list[text_index]
            self.show_entry(text_surf, amount, top, self.index == text_index)
