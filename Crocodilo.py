#Importa
import pygame
from assets import load_assets
from config import HEIGHT, WIDTH
import random

# Define a Classe do Corocdilo
class Crocodilo(pygame.sprite.Sprite):
    
    def __init__(self, assets):
     
        pygame.sprite.Sprite.__init__(self)

        self.image = assets['crocodilo_img']
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.direcao = random.randint(1,4)
        
        if self.direcao == 1:
            self.rect.y = -HEIGHT/2
            self.rect.centerx = WIDTH / 2
            self.speedy = random.randint(2, 7)
            self.speedx = 0
        
        elif self.direcao == 2:
            self.rect.y = HEIGHT + HEIGHT / 2
            self.rect.centerx = WIDTH / 2
            self.speedy = random.randint(-7, -2)
            self.speedx = 0
        
        elif self.direcao == 3:
            self.rect.centery = HEIGHT / 2
            self.rect.x = -WIDTH / 2
            self.speedx = random.randint(2, 7)
            self.speedy = 0
        
        elif self.direcao == 4:
            self.rect.centery = HEIGHT / 2
            self.rect.x = WIDTH + WIDTH /2
            self.speedx = random.randint(-7, -2)
            self.speedy = 0

    def update(self):

        self.rect.x += self.speedx
        self.rect.y += self.speedy