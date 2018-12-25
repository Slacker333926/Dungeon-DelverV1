#Load module
import pygame

#Name and define class
class Key(pygame.sprite.Sprite):

    #Define sprite image and shape
    def __init__(self, x, y):
        super(Key, self).__init__()
        self.image = pygame.image.load("images/key.png").convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))

    #Define update
    def update(self):
        self.rect.y += 5
        if self.rect.y >= 600:
            self.rect.y = 0

    #Define collision
    def collision(self):
        self.rect.y = 0