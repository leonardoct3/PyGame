# ===== Inicialização =====

# Importa Bibliotecas
import pygame
import random
import time

pygame.init()
pygame.mixer.init()

# Criação da Window Principal
WIDTH = 900
HEIGHT = 700
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Mata Crocodilo')

# Define Dimensões
FPS = 30
CROCODILO_LATERAL_WIDTH = 300
CROCODILO_LATERAL_HEIGHT = 179
CROCODILO_VERTICAL_WIDTH = 179
CROCODILO_VERTICAL_HEIGHT = 300
FIGURA_WIDTH = 150
FIGURA_HEIGHT = 100
ILHA_WIDTH = 900
ILHA_HEIGHT = 700
BALA_WIDTH = 100
BALA_HEIGHT = 100

# Carrega Assets
def load_assets():
    
    assets = {}
    assets['background'] = pygame.image.load('assets/img/Ilha.png').convert()
    assets['background'] = pygame.transform.scale(assets['background'], (ILHA_WIDTH, ILHA_HEIGHT))
    assets['crocodilo_img'] = pygame.image.load('assets/img/Crocodilo.png').convert_alpha()
    assets['crocodilo_img'] = pygame.transform.scale(assets['crocodilo_img'], (CROCODILO_LATERAL_WIDTH, CROCODILO_LATERAL_HEIGHT))
    crocodilos_img = []
    
    for i in range (0,3):
        nome = 'assets/img/crocodilo_desce({}).png'.format(i)
        img = pygame.image.load(nome).convert_alpha()
        img = pygame.transform.scale(img, (CROCODILO_VERTICAL_WIDTH, CROCODILO_VERTICAL_HEIGHT))
        crocodilos_img.append(img)
    for i in range (0,3):
        nome = 'assets/img/crocodilo_direita({}).png'.format(i)
        img = pygame.image.load(nome).convert_alpha()
        img = pygame.transform.scale(img, (CROCODILO_LATERAL_WIDTH, CROCODILO_LATERAL_HEIGHT))
        crocodilos_img.append(img)
    for i in range (0,3):
        nome = 'assets/img/crocodilo_esquerda({}).png'.format(i)
        img = pygame.image.load(nome).convert_alpha()
        img = pygame.transform.scale(img, (CROCODILO_LATERAL_WIDTH, CROCODILO_LATERAL_HEIGHT))
        crocodilos_img.append(img)
    for i in range (0,3):
        nome = 'assets/img/crocodilo_sobe({}).png'.format(i)
        img = pygame.image.load(nome).convert_alpha()
        img = pygame.transform.scale(img, (CROCODILO_VERTICAL_WIDTH, CROCODILO_VERTICAL_HEIGHT))
        crocodilos_img.append(img)
    assets['crocodilos_img'] = crocodilos_img
    # Animação Humano
    figuras_img = []
    for i in range (1,5):
        name = 'assets/img/Humano{}.png'.format(i)
        img = pygame.image.load(name).convert_alpha()
        img = pygame.transform.scale(img, (FIGURA_WIDTH, FIGURA_HEIGHT))
        figuras_img.append(img)
    assets['figuras_img'] = figuras_img
    
    # Animação Bala
    balas_img = []
    for e in range (1,5):
        name = 'assets/img/bala{}.png'.format(e)
        img = pygame.image.load(name).convert_alpha()
        img = pygame.transform.scale(img, (BALA_WIDTH, BALA_HEIGHT))
        balas_img.append(img)
    assets['balas_img'] = balas_img
    
    # Carrega Sons
    pygame.mixer.music.load('assets/snd/mar.ogg')
    pygame.mixer.music.set_volume(0.6)
    assets['dead'] = pygame.mixer.Sound('assets/snd/dead.ogg')
    assets['arma'] = pygame.mixer.Sound('assets/snd/arma.ogg')

    #Carrega Fonte
    assets["score_font"] = pygame.font.Font('assets/font/PressStart2P.ttf', 36)

    return assets

# Define a Classe da Figura Principal
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


def game_screen(window):
    # Variável para o ajuste de velocidade
    clock = pygame.time.Clock()

    assets = load_assets()

    # Grupo de crocodilos
    all_sprites = pygame.sprite.Group()
    all_crocodilos = pygame.sprite.Group()
    all_bullets = pygame.sprite.Group()
    groups = {}
    groups['all_sprites'] = all_sprites
    groups['all_crocodilos'] = all_crocodilos
    groups['all_bullets'] = all_bullets

    # Criando o jogador
    player = Figura(groups, assets)
    all_sprites.add(player)
    
    # Criando os crocodilos
    for i in range(8):
        crocodilo = Crocodilo(assets)
        all_sprites.add(crocodilo)
        all_crocodilos.add(crocodilo)

    INIT = 0
    DONE = 2
    PLAYING = 1
    state = PLAYING

    keys_down = {}
    score = 0

    # ===== Loop principal =====
    pygame.mixer.music.play(loops=-1)
    while state != DONE:
        clock.tick(FPS)

        # ----- Trata eventos
        for event in pygame.event.get():
            # ----- Verifica consequências
            if event.type == pygame.QUIT:
                state = DONE
            # Só verifica o teclado se está no estado de jogo
            if state == PLAYING:
                # Verifica se apertou alguma tecla.
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        player.shoot()

        # ----- Atualiza estado do jogo

        all_sprites.update()

        if state == PLAYING:
        
            hits = pygame.sprite.groupcollide(all_crocodilos, all_bullets, True, True, pygame.sprite.collide_mask)
            
            for crocodilo in hits:
                m = Crocodilo(assets)
                all_sprites.add(m)
                all_crocodilos.add(m)

                score += 10

            # Verifica se houve colisão entre nave e meteoro
            hits = pygame.sprite.spritecollide(player, all_crocodilos, True, pygame.sprite.collide_mask)
            if len(hits) > 0:
                # Toca o som da colisão
                assets['dead'].play()
                score = 0 
                player.kill()
                time.sleep(1) 

                state = DONE

        # ----- Gera saídas
        window.fill((0, 0, 0))  
        window.blit(assets['background'], (0, 0))
     
        all_sprites.draw(window)

        text_surface = assets['score_font'].render("{:02d}".format(score), True, (250, 250, 0))
        text_rect = text_surface.get_rect()
        text_rect.midtop = (90,  10)
        window.blit(text_surface, text_rect)

        pygame.display.update()  

    return 

game_screen(window)

# ===== Finalização =====
pygame.quit()  


