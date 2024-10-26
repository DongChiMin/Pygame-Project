import pygame
import random

class Sound:
    def __init__(self):
        pygame.mixer.init()

        self.path = "../audio/"
        self.axe_sound = pygame.mixer.Sound(f"{self.path}axe.wav")
        # self.hoe_sound = pygame.mixer.Sound(f"{self.path}hoe.mp3")
        self.collect_sound = pygame.mixer.Sound(f"{self.path}collect.wav")
        self.watering_sound = pygame.mixer.Sound(f"{self.path}watering.wav")

    def play_axe_sound(self):
        self.axe_sound.play()

    def play_collect_sound(self):
        self.collect_sound.play()


    def play_hoe_sound(self):
        pass
        #self.hoe_sound.play()

    def play_watering_sound(self):
        self.watering_sound.play()

