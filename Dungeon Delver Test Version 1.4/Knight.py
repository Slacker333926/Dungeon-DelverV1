#Load module
import pygame

#Name and define class
class Knight(pygame.sprite.Sprite):

    #Define sprite image and shape
    def __init__(self):
        super(Knight, self).__init__()
        self.image = pygame.image.load("images/knight.png").convert_alpha()
        self.rect = self.image.get_rect(center=(0, 600))
        self.lives = 3

    #Define directional controls
    def update(self, direction):
        if direction == 1:
            self.rect.x -= 5
        elif direction == 0:
            self.rect.x += 5
        elif direction == 2:
            self.rect.y -= 5
        elif direction == 3:
            self.rect.y += 5
        elif direction == 4:
            self.rect.y += 3