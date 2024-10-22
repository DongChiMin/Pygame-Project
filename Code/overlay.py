import pygame
from settings import *

class Overlay:
    def __init__(self, player):
        self.display_surface = pygame.display.get_surface();
        self.player = player

        #{tool:surface}
        overlay_path = '../graphics/overlay/'
        self.tools_surf = {tool: pygame.image.load(f'{overlay_path}{tool}.png').convert_alpha() for tool in player.tools}
        self.seeds_surf ={seed: pygame.image.load(f'{overlay_path}{seed}.png').convert_alpha() for seed in player.seeds}

        #square
        self.default_square_surf = pygame.image.load(f'{overlay_path}square.png').convert_alpha()
        self.center_tool_surf = self.default_square_surf
        self.center_seed_surf = self.default_square_surf
        self.highlight_square_surf = pygame.image.load(f'{overlay_path}squareOnMouse.png').convert_alpha()

        #key_of_square(q,e)
        self.corner_q_surf = pygame.image.load(
            f'{overlay_path}q.png').convert_alpha()
        self.corner_e_surf = pygame.image.load(
            f'{overlay_path}e.png').convert_alpha()

        #setting_UI
        self.setting_UI_surf = pygame.image.load(f'{overlay_path}setting_ui.png').convert_alpha()

        #Mouse_Cursor
        self.cursor_surf = pygame.image.load(f'{overlay_path}mouse_cursor.png').convert_alpha()
        self.cursor_rect = self.cursor_surf.get_rect()
        pygame.mouse.set_visible(False)

        #kiem tra trạng thái
        self.clicked = False
        self.Q_pressed = False
        self.E_pressed = False

    def display (self):
        #tools
        tool_surf = self.tools_surf[self.player.selected_tool]
        tool_rect = tool_surf.get_rect(midbottom = OVERLAY_POSITIONS['tool'])

        #seeds
        seed_surf = self.seeds_surf[self.player.selected_seed]
        seed_rect = seed_surf.get_rect(midbottom=OVERLAY_POSITIONS['seed'])

        #square_tool
        self.center_tool_rect = self.center_tool_surf.get_rect(midbottom=OVERLAY_POSITIONS['square_tool'])

        #square_seed
        self.center_seed_rect = self.center_seed_surf.get_rect(midbottom=OVERLAY_POSITIONS['square_seed'])

        #Quản lý hiệu ứng button
        #Tương tác bàn phím (tool + seed)
        self.handle_keyboard_interaction()
        #Tương tác chuột (tool)
        self.center_tool_surf = self.handle_mouse_interaction(
            self.center_tool_rect, self.default_square_surf, self.highlight_square_surf, self.player.change_tool
        )


        # Tương tác chuột (seed)
        self.center_seed_surf = self.handle_mouse_interaction(
            self.center_seed_rect, self.default_square_surf, self.highlight_square_surf, self.player.change_seed
        )


        #key_of_square_tool
        corner_q_rect = self.corner_q_surf.get_rect(topright=(
        self.center_tool_rect.right + 10, self.center_tool_rect.top - 10))
        corner_e_rect = self.corner_e_surf.get_rect(topright=(
            self.center_seed_rect.right + 10, self.center_seed_rect.top - 10))

        #setting_UI
        setting_UI_rect = self.setting_UI_surf.get_rect(topleft= OVERLAY_POSITIONS['setting_UI'])
        self.display_surface.blit(self.setting_UI_surf, setting_UI_rect)

        #Draw square
        self.display_surface.blit(self.center_tool_surf, self.center_tool_rect)
        self.display_surface.blit(self.center_seed_surf, self.center_seed_rect)

        #Draw tool and seed
        self.display_surface.blit(seed_surf, seed_rect)
        self.display_surface.blit(tool_surf, tool_rect)

        #Draw key of square
        self.display_surface.blit(self.corner_q_surf, corner_q_rect)
        self.display_surface.blit(self.corner_e_surf, corner_e_rect)

        #Draw mouse cursor
        mouse_x, mouse_y = pygame.mouse.get_pos()  # Get mouse position
        self.cursor_rect.topleft = (mouse_x, mouse_y)  # Update position
        self.display_surface.blit(self.cursor_surf, self.cursor_rect)

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # Kiểm tra nếu chuột trái được bấm khi không hover
        if pygame.mouse.get_pressed()[0] == 1 and not self.center_tool_rect.collidepoint(mouse_x,
        mouse_y) and not self.center_seed_rect.collidepoint(
                mouse_x, mouse_y):
            self.player.timers['tool use'].activate()
            self.player.direction = pygame.math.Vector2()
            self.player.frame_index = 0

        # Kiểm tra nếu chuột phải được bấm khi không hover
        if pygame.mouse.get_pressed()[2] == 1 and not self.center_tool_rect.collidepoint(mouse_x,
        mouse_y) and not self.center_seed_rect.collidepoint(
                mouse_x, mouse_y):
            self.player.timers['seed use'].activate()
            self.player.input_seed_use()

    def handle_mouse_interaction(self, rect, default_surf, highlight_surf, action):
        """Handle mouse interaction for tool and seed."""
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if rect.collidepoint(mouse_x, mouse_y):
            # Change to highlight surface when mouse hovers
            surf = highlight_surf

            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                rect.y += 10
                rect.x -= 5
                self.clicked = True
                action()  # Perform the action (change tool or seed)
        elif not self.Q_pressed or not self.E_pressed:
            # Return to default surface when not hovering
            surf = default_surf
        else:
            surf = highlight_surf

        return surf

    def handle_keyboard_interaction(self):
        keys = pygame.key.get_pressed()

        # Khi nhấn Q
        if keys[pygame.K_q] and not self.Q_pressed:
            self.E_pressed = True
            # Chuyển đổi tool và thay đổi hiệu ứng hình ảnh
            self.center_tool_surf = self.highlight_square_surf
            self.center_tool_rect.y += 10  # Hiệu ứng di chuyển khi nhấn
            self.center_tool_rect.x -= 5

        # Khi nhấn E
        if keys[pygame.K_e] and not self.E_pressed:
            self.Q_pressed = True
            # Chuyển đổi seed và thay đổi hiệu ứng hình ảnh
            self.center_seed_surf = self.highlight_square_surf
            self.center_seed_rect.y += 10  # Hiệu ứng di chuyển khi nhấn
            self.center_seed_rect.x -= 5

        if pygame.KEYUP:
            self.Q_pressed = False
            self.E_pressed = False