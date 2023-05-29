#Importa
import pygame
from assets import load_assets
from config import HEIGHT, WIDTH
import random

# Define a Classe do Crocdilo
class Crocodilo(pygame.sprite.Sprite):
    def __init__(self, assets):
        pygame.sprite.Sprite.__init__(self)

        self.direcao = random.randint(1, 4)
        
        if self.direcao == 1:
            self.anim_images = assets['crocodilos_desce_img']
            self.rect = self.anim_images[0].get_rect()
            self.rect.y = -HEIGHT / 2
            self.rect.centerx = WIDTH / 2
            self.speedy = random.randint(2, 8)
            self.speedx = 0
        
        elif self.direcao == 2:
            self.anim_images = assets['crocodilos_sobe_img']
            self.rect = self.anim_images[0].get_rect()
            self.rect.y = HEIGHT + HEIGHT / 2
            self.rect.centerx = WIDTH / 2
            self.speedy = random.randint(-8, -2)
            self.speedx = 0
        
        elif self.direcao == 3:
            self.anim_images = assets['crocodilos_esquerda_img']
            self.rect = self.anim_images[0].get_rect()
            self.rect.centery = HEIGHT / 2 - 10
            self.rect.x = -WIDTH / 2
            self.speedx = random.randint(2, 8)
            self.speedy = 0
        
        elif self.direcao == 4:
            self.anim_images = assets['crocodilos_direita_img']
            self.rect = self.anim_images[0].get_rect()
            self.rect.centery = HEIGHT / 2 - 10
            self.rect.x = WIDTH + WIDTH / 2
            self.speedx = random.randint(-8, -2)
            self.speedy = 0

        self.image = self.anim_images[0]
        self.mask = pygame.mask.from_surface(self.image)

        self.anim_frame = 0
        self.anim_speed = 250
        self.last_update = pygame.time.get_ticks()

    def update(self):

        self.rect.x += self.speedx
        self.rect.y += self.speedy

        now = pygame.time.get_ticks()
        elapsed_time = now - self.last_update

        if elapsed_time > self.anim_speed:
            self.last_update = now
            self.anim_frame = (self.anim_frame + 1) % len(self.anim_images)
            self.image = self.anim_images[self.anim_frame]