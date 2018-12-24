#THIS IS SMALL CODE FOR THE KNIGHT THAT I BARELY UNDERSTAND
import pygame

class Knight(pygame.sprite.Sprite):

    def __init__(self):
        super(Knight, self).__init__()
        self.image = pygame.image.load("images/knight.png").convert_alpha()
        self.rect = self.image.get_rect(center=(0, 600))
        self.lives = 3

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