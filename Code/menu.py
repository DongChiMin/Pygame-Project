import pygame
from debugpy.common.timestamp import current
from pygame import Surface
from six import text_type
from timer import Timer
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
        self.timer = Timer(200)


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

        #buy/sell text
        self.buy_text = self.font.render('buy', False, (170, 121, 89))
        self.sell_text = self.font.render('sell', False, (170, 121, 89))

    def display_money(self):
        text_surf = self.font.render( f"money: {self.player.money}",False,(170,121,89))
        text_rect = text_surf.get_rect(midtop = (SCREEN_WIDTH / 2, 25) )

        #inflate: hình chữ nhật bao quanh, 6: bo tròn
        pygame.draw.rect(self.display_surface, (170, 121, 89), text_rect.inflate(30, 30), 0, 6)
        pygame.draw.rect(self.display_surface, (232,207,166), text_rect.inflate(20,20),0 , 6)
        self.display_surface.blit(text_surf, text_rect)

    def input(self):
        # Lấy vị trí chuột và trạng thái các nút
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        keys = pygame.key.get_pressed()
        self.timer.update()

        # nếu nhấn esc: tắt ui
        if keys[pygame.K_ESCAPE]:
            self.toggle_UI()

        # Kiểm tra xem chuột có hover vào mục nào trong danh sách không
        for text_index, text_surf in enumerate(self.text_surfs):
            # Tính toán tọa độ y của mục đó
            top = self.main_rect.top + text_index * (text_surf.get_height() + (self.padding * 2) + self.space) + 50
            entry_rect = pygame.Rect(self.main_rect.left + 15, top, self.width - 30,
                                     text_surf.get_height() + (self.padding * 2))

            # Nếu chuột hover vào mục này, cập nhật self.index thành text_index
            if entry_rect.collidepoint(mouse_pos):
                self.index = text_index  # Cập nhật index để đánh dấu mục đang hover

                if not self.timer.active:
                    # Nếu nhấn chuột trái (click chuột)
                    if mouse_click[0]:  # [0] là chuột trái
                        current_item = self.options[self.index]
                        self.timer.activate()

                        # Sell
                        if self.index <= self.sell_border:
                            if self.player.item_inventory[current_item] > 0:
                                self.player.item_inventory[current_item] -= 1
                                self.player.money += SALE_PRICES[current_item]
                        # Buy
                        else:
                            seed_price = PURCHASE_PRICES[current_item]
                            if self.player.money >= seed_price:
                                self.player.seed_inventory[current_item] += 1
                                self.player.money -= PURCHASE_PRICES[current_item]



    # def input(self):
    #     #get the input
    #     #if the player press esc close the menu
    #     keys = pygame.key.get_pressed()
    #     self.timer.update()
    #
    #     if keys[pygame.K_ESCAPE]:
    #         self.toggle_UI()
    #
    #     if not self.timer.active:
    #         if keys[pygame.K_UP]:
    #             self.index -= 1
    #             self.timer.activate()
    #
    #         if keys[pygame.K_DOWN]:
    #             self.index += 1
    #             self.timer.activate()
    #         if keys[pygame.K_SPACE]:
    #             self.timer.activate()
    #
    #             #get item
    #             current_item = self.options[self.index]
    #
    #             #sell
    #             if self.index <= self.sell_border:
    #                 if self.player.item_inventory[current_item] > 0:
    #                     self.player.item_inventory[current_item] -=1
    #                     self.player.money += SALE_PRICES[current_item]
    #             #buy
    #             else:
    #                 seed_price = PURCHASE_PRICES[current_item]
    #                 if self.player.money >= seed_price:
    #                     self.player.seed_inventory[current_item]+=1
    #                     self.player.money -= PURCHASE_PRICES[current_item]
    #
    #     if self.index < 0:
    #         self.index = len(self.options) -1
    #     if self.index > len(self.options) -1:
    #         self.index = 0

    def show_entry(self, text_surf, amount, top, text_index, selected):
        # background
        bg_rect = pygame.Rect(self.main_rect.left + 15, top, self.width - 30,
                              text_surf.get_height() + (self.padding * 2))
        pygame.draw.rect(self.display_surface, (232, 207, 166), bg_rect, 0, 4)

        # text (tên item)
        text_rect = text_surf.get_rect(midleft=(self.main_rect.left + 30, bg_rect.centery))
        self.display_surface.blit(text_surf, text_rect)

        # amount (số lượng)
        amount_surf = self.font.render(str(amount), False, (170, 121, 89))
        amount_rect = amount_surf.get_rect(
            midright=(self.main_rect.right - 120, bg_rect.centery))
        self.display_surface.blit(amount_surf, amount_rect)

        # price (giá)
        current_item = self.options[text_index]  # Sử dụng text_index để lấy tên item
        if text_index <= self.sell_border:
            price = SALE_PRICES[current_item]  # Lấy giá bán
        else:
            price = PURCHASE_PRICES[current_item]  # Lấy giá mua
        price_surf = self.font.render(f"${price}", False, (170, 121, 89))
        price_rect = price_surf.get_rect(midright=(self.main_rect.right - 30, bg_rect.centery))
        self.display_surface.blit(price_surf, price_rect)

        # selected (được chọn)
        if selected:
            pygame.draw.rect(self.display_surface, 'White', bg_rect, 4, 4)
            if self.index <= self.sell_border:  # sell
                pos_rect = self.sell_text.get_rect(midleft=(self.main_rect.left + 150, bg_rect.centery))
                self.display_surface.blit(self.sell_text, pos_rect)
            else:  # buy
                pos_rect = self.buy_text.get_rect(midleft=(self.main_rect.left + 150, bg_rect.centery))
                self.display_surface.blit(self.buy_text, pos_rect)

    def update(self):
        self.input()
        self.display_money()


        #in ra nền background
        bg_surf = pygame.image.load('../graphics/UI/rect_1.png').convert_alpha()
        bg_rect = bg_surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 30 ))
        self.display_surface.blit(bg_surf, bg_rect)

        exit_surf = pygame.image.load("../graphics/UI/exit_menu.png").convert_alpha()
        exit_rect = exit_surf.get_rect(topleft=(bg_rect.left + 12, bg_rect.top + 12))
        self.display_surface.blit(exit_surf, exit_rect)

        #enumerate: de lay ra duoc index cua item
        for text_index, text_surf in enumerate(self.text_surfs):
            top = self.main_rect.top + text_index * (text_surf.get_height() + (self.padding * 2) + self.space) + 50
            amount_list = list(self.player.item_inventory.values()) + list(self.player.seed_inventory.values())
            amount = amount_list[text_index]
            self.show_entry(text_surf, amount, top,text_index, self.index == text_index)
