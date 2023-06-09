# Importa
from assets import load_assets
import pygame

# Balas Atiradas Pelo Player
class Bullet(pygame.sprite.Sprite):

    # Construtor da Classe
    def __init__(self, assets, centery, centerx, facing):
        
        # Constrói a Classe Mãe (Sprite)
        pygame.sprite.Sprite.__init__(self)
        
        # Define a Imagem das Balas para Cada Direção
        self.bala_down = assets['balas_img'][3]
        self.bala_up = assets['balas_img'][1]
        self.bala_left = assets['balas_img'][2]
        self.bala_right = assets['balas_img'][0]
        
        self.facing = facing  # Armazena a direção da bala

        # Define as Posições Iniciais de Cada Bala
        if self.facing == 'left':
            self.image = self.bala_left
            centerx -= 65
            centery += 15
        elif self.facing =='right':
            self.image = self.bala_right
            centerx += 60
            centery += 85
        elif self.facing == 'up':
            self.image = self.bala_up
            centerx += 45
            centery += 20
        elif self.facing == 'down':
            self.image = self.bala_down
            centerx -= 40
            centery += 85

        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.last_update = 0
        self.rect.centerx = centerx
        self.rect.centery = centery

    
    def update(self):
        keys = pygame.key.get_pressed()

        # Define as Velocidades dos Tiros
        if self.facing == 'left':
            self.speedx = -10
            self.rect.x += self.speedx
        elif self.facing == 'right':
            self.speedx = 10
            self.rect.x += self.speedx
        elif self.facing == 'up':
            self.speedy = -10
            self.rect.y += self.speedy
        elif self.facing == 'down':
            self.speedy = 10
            self.rect.y += self.speedy

        # A Bala "Morre" se Sair da Tela
        if self.rect.bottom < 0:
            self.kill()

        
        