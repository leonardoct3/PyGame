class Bullet(pygame.sprite.Sprite):
    
    def __init__(self, assets, centery, centerx, facing):
        pygame.sprite.Sprite.__init__(self)
        self.bala_down = assets['balas_img'][3]
        self.bala_up = assets['balas_img'][1]
        self.bala_left = assets['balas_img'][2]
        self.bala_right = assets['balas_img'][0]
        
        self.facing = facing  # Armazena a direção da bala

        if self.facing == 'left':
            self.image = self.bala_left
        elif self.facing =='right':
            self.image = self.bala_right
        elif self.facing == 'up':
            self.image = self.bala_up
        elif self.facing == 'down':
            self.image = self.bala_down

        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.last_update = 0
        self.rect.centerx = centerx
        self.rect.centery = centery

    def update(self):
        keys = pygame.key.get_pressed()

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

        if self.rect.bottom < 0:
            self.kill()

        if self.rect.bottom < 0:
            self.kill()

        if self.rect.bottom < 0:
            self.kill()