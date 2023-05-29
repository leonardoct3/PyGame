from config import assets,WIDTH,HEIGHT
import pygame

class Figura(pygame.sprite.Sprite):
    
    def __init__(self, groups, assets):
        # Construtor do Sprite
        pygame.sprite.Sprite.__init__(self)

        # Define as Imagens da Figura
        self.humano_down = assets['figuras_img'][3]
        self.humano_up = assets['figuras_img'][1]
        self.humano_left = assets['figuras_img'][2]
        self.humano_right = assets['figuras_img'][0]

        self.image = self.humano_down
        self.d = 'down'

        self.animation_sprite = 0
        self.animation_speed = 6

        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.centery = HEIGHT / 2
        self.speedx = 0
        self.groups = groups
        self.assets = assets

        # Define Intervalo Entre Tiros
        self.last_shot = pygame.time.get_ticks()
        self.shoot_ticks = 300
    
    def update(self):
        # Define as Teclas que Mudam a Posição da Figura
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.image = self.humano_left
            self.d = 'left'
        elif keys[pygame.K_RIGHT]:
            self.image = self.humano_right
            self.d = 'right'
        elif keys[pygame.K_UP]:
            self.image = self.humano_up
            self.d = 'up'
        elif keys[pygame.K_DOWN]:
            self.image = self.humano_down
            self.d= 'down'

    def shoot(self):

        # Confere se é Possível Atirar
        now = pygame.time.get_ticks()
        elapsed_ticks = now - self.last_shot
        
        if elapsed_ticks > self.shoot_ticks:
            self.last_shot = now

            new_bullet = Bullet(self.assets, self.rect.top, self.rect.centerx, self.d)
            self.groups['all_sprites'].add(new_bullet)
            self.groups['all_bullets'].add(new_bullet)
            self.assets['arma'].play()
