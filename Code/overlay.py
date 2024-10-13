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
        self.center_tool_surf = pygame.image.load(f'{overlay_path}square1.png').convert_alpha()
        self.center_seed_surf = pygame.image.load(f'{overlay_path}square2.png').convert_alpha()

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

    def display (self):
        #tools
        tool_surf = self.tools_surf[self.player.selected_tool]
        tool_rect = tool_surf.get_rect(midbottom = OVERLAY_POSITIONS['tool'])

        #seeds
        seed_surf = self.seeds_surf[self.player.selected_seed]
        seed_rect = seed_surf.get_rect(midbottom=OVERLAY_POSITIONS['seed'])

        #square_tool
        center_tool_rect = self.center_tool_surf.get_rect(midbottom=OVERLAY_POSITIONS['square_tool'])

        #square_seed
        center_seed_rect = self.center_seed_surf.get_rect(midbottom=OVERLAY_POSITIONS['square_seed'])

        #key_of_square_tool
        corner_q_rect = self.corner_q_surf.get_rect(topright=(
        center_tool_rect.right + 10, center_tool_rect.top - 10))
        corner_e_rect = self.corner_e_surf.get_rect(topright=(
            center_seed_rect.right + 10, center_seed_rect.top - 10))

        #setting_UI
        setting_UI_rect = self.setting_UI_surf.get_rect(topleft= OVERLAY_POSITIONS['setting_UI'])
        self.display_surface.blit(self.setting_UI_surf, setting_UI_rect)

        #Draw square
        self.display_surface.blit(self.center_tool_surf, center_tool_rect)
        self.display_surface.blit(self.center_seed_surf, center_seed_rect)

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

