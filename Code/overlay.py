import pygame
from settings import *
from ui import ui

class Overlay:
    def __init__(self, player):
        self.display_surface = pygame.display.get_surface()
        self.player = player

        # {tool:surface}
        overlay_path = '../graphics/overlay/'
        self.tools_surf = {tool: pygame.image.load(f'{overlay_path}{tool}.png').convert_alpha() for tool in player.tools}
        self.seeds_surf = {seed: pygame.image.load(f'{overlay_path}{seed}.png').convert_alpha() for seed in player.seeds}

        # square
        self.default_square_surf = pygame.image.load(f'{overlay_path}square.png').convert_alpha()
        self.center_tool_surf = self.default_square_surf
        self.center_seed_surf = self.default_square_surf
        self.highlight_square_surf = pygame.image.load(f'{overlay_path}highlight_square.png').convert_alpha()

        # square_tool
        self.center_tool_rect = self.center_tool_surf.get_rect(midbottom=OVERLAY_POSITIONS['square_tool'])

        # square_seed
        self.center_seed_rect = self.center_seed_surf.get_rect(midbottom=OVERLAY_POSITIONS['square_seed'])

        # key_of_square(q,e,b)
        self.corner_q_surf = pygame.image.load(f'{overlay_path}q.png').convert_alpha()
        self.corner_e_surf = pygame.image.load(f'{overlay_path}e.png').convert_alpha()



        # kiểm tra trạng thái
        self.clicked = False
        self.Q_pressed = False
        self.E_pressed = False

        #sound
        self.button2_sound = pygame.mixer.Sound('../audio/button2.wav')

    def display(self):
        # tools
        tool_surf = self.tools_surf[self.player.selected_tool]
        tool_rect = tool_surf.get_rect(midbottom=OVERLAY_POSITIONS['tool'])

        # seeds
        seed_surf = self.seeds_surf[self.player.selected_seed]
        seed_rect = seed_surf.get_rect(midbottom=OVERLAY_POSITIONS['seed'])

        # Tương tác bàn phím (tool + seed)
        self.handle_keyboard_interaction()

        # Tương tác chuột (tool)
        self.center_tool_surf = self.handle_mouse_interaction(
            self.center_tool_rect, self.default_square_surf, self.highlight_square_surf, self.player.change_tool
        )

        # Tương tác chuột (seed)
        self.center_seed_surf = self.handle_mouse_interaction(
            self.center_seed_rect, self.default_square_surf, self.highlight_square_surf, self.player.change_seed
        )

        # key_of_square_tool
        corner_q_rect = self.corner_q_surf.get_rect(topright=(
            self.center_tool_rect.right + 10, self.center_tool_rect.top - 10))
        corner_e_rect = self.corner_e_surf.get_rect(topright=(
            self.center_seed_rect.right + 10, self.center_seed_rect.top - 10))

        # Draw square
        self.display_surface.blit(self.center_tool_surf, self.center_tool_rect)
        self.display_surface.blit(self.center_seed_surf, self.center_seed_rect)

        # Draw tool and seed
        self.display_surface.blit(seed_surf, seed_rect)
        self.display_surface.blit(tool_surf, tool_rect)

        # Draw key of square
        self.display_surface.blit(self.corner_q_surf, corner_q_rect)
        self.display_surface.blit(self.corner_e_surf, corner_e_rect)

        #mouse
        mouse_x, mouse_y = pygame.mouse.get_pos()

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False



    def handle_mouse_interaction(self, rect, default_surf, highlight_surf, action):
        """Handle mouse interaction for tool and seed."""
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if rect.collidepoint(mouse_x, mouse_y):
            # Change to highlight surface when mouse hovers
            surf = highlight_surf

            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.button2_sound.play()
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
            self.center_tool_surf = self.highlight_square_surf

        # Khi nhấn E
        if keys[pygame.K_e] and not self.E_pressed:
            self.Q_pressed = True
            self.center_seed_surf = self.highlight_square_surf

        if not keys[pygame.K_q]:
            self.Q_pressed = False

        if not keys[pygame.K_e]:
            self.E_pressed = False
