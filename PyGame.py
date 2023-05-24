# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame
import random
import time

pygame.init()
pygame.mixer.init()

# ----- Gera tela principal
WIDTH = 900
HEIGHT = 700
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Mata Crocodilo')

# ----- Inicia assets
FPS = 30
CROCODILO_WIDTH = 300
CROCODILO_HEIGHT = 179
FIGURA_WIDTH = 150
FIGURA_HEIGHT = 100
ILHA_WIDTH = 900
ILHA_HEIGHT = 700
BALA_WIDTH = 75
BALA_HEIGHT = 100
def load_assets():
    assets = {}
    assets['background'] = pygame.image.load('assets/img/Ilha.png').convert()
    assets['background'] = pygame.transform.scale(assets['background'], (ILHA_WIDTH, ILHA_HEIGHT))
    assets['crocodilo_img'] = pygame.image.load('assets/img/Crocodilo.png').convert_alpha()
    assets['crocodilo_img'] = pygame.transform.scale(assets['crocodilo_img'], (CROCODILO_WIDTH, CROCODILO_HEIGHT))
    # # assets['figura_img'] = pygame.image.load('assets/img/Humano.png').convert_alpha()
    # assets['figura_img'] = pygame.transform.scale(assets['figura_img'], (FIGURA_WIDTH, FIGURA_HEIGHT))
    # assets['bullet_img'] = pygame.image.load('assets/img/laserRed16.png').convert_alpha()
    # assets['bullet_img'] = pygame.transform.scale(assets['bullet_img'], (50,100))
    figuras_img = []
    for i in range (1,5):
        name = 'assets/img/Humano{}.png'.format(i)
        img = pygame.image.load(name).convert_alpha()
        img = pygame.transform.scale(img, (FIGURA_WIDTH, FIGURA_HEIGHT))
        figuras_img.append(img)
    assets['figuras_img'] = figuras_img
    balas_img = []
    for e in range (1,5):
        name = 'assets/img/bala{}.png'.format(e)
        img = pygame.image.load(name).convert_alpha()
        img = pygame.transform.scale(img, (BALA_WIDTH, BALA_HEIGHT))
        balas_img.append(img)
    assets['balas_img'] = balas_img
    #Sons
    pygame.mixer.music.load('assets/snd/tgfcoder-FrozenJam-SeamlessLoop.ogg')
    pygame.mixer.music.set_volume(0.4)
    assets['boom_sound'] = pygame.mixer.Sound('assets/snd/expl3.wav')
    assets['destroy_sound'] = pygame.mixer.Sound('assets/snd/expl6.wav')
    assets['pew_sound'] = pygame.mixer.Sound('assets/snd/pew.wav')

    return assets

# ----- Inicia estruturas de dados
# Definindo os novos tipos
class Figura(pygame.sprite.Sprite):
    def __init__(self, groups, assets):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)
        keys = pygame.key.get_pressed()
        self.humano_down = assets['figuras_img'][3]
        self.humano_up = assets['figuras_img'][1]
        self.humano_left = assets['figuras_img'][2]
        self.humano_right = assets['figuras_img'][0]

        self.image = self.humano_down
        self.d = 'down'
        # if keys[pygame.K_LEFT]:
        #     self.image = self.humano_left
        #     self.d = 'left'
        # elif keys[pygame.K_RIGHT]:
        #     self.image = self.humano_right
        #     self.d = 'right'
        # elif keys[pygame.K_UP]:
        #     self.image = self.humano_up
        #     self.d = 'up'
        # elif keys[pygame.K_DOWN]:
        #     self.image = self.humano_down
        #     self.d= 'down'
        self.animation_sprite = 0
        self.animation_speed = 6

        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.centery = HEIGHT / 2
        self.speedx = 0
        self.groups = groups
        self.assets = assets

        # Só será possível atirar uma vez a cada 250 milissegundos
        self.last_shot = pygame.time.get_ticks()
        self.shoot_ticks = 250
    def update(self):
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
        # Verifica se pode atirar
        now = pygame.time.get_ticks()
        # Verifica quantos ticks se passaram desde o último tiro.
        elapsed_ticks = now - self.last_shot

        # Se já pode atirar novamente...
        if elapsed_ticks > self.shoot_ticks:
            # Marca o tick da nova imagem.
            self.last_shot = now
            # A nova bala vai ser criada logo acima e no centro horizontal da nave
            new_bullet = Bullet(self.assets, self.rect.top, self.rect.centerx, self.d)
            self.groups['all_sprites'].add(new_bullet)
            self.groups['all_bullets'].add(new_bullet)
            self.assets['pew_sound'].play()

class Crocodilo(pygame.sprite.Sprite):
    def __init__(self, assets):
        # Construtor da classe mãe (Sprite).
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
            self.speedy = random.randint(-7, -2)
            self.speedx = 0

    def update(self):
        # Atualizando a posição do meteoro
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        # Se o meteoro passar do final da tela, volta para cima e sorteia
        # novas posições e velocidades
        # if self.rect.top > HEIGHT or self.rect.right < 0 or self.rect.left > WIDTH:
        #     self.rect.x = random.randint(0, WIDTH-CROCODILO_WIDTH)
        #     self.rect.y = random.randint(-100, -CROCODILO_HEIGHT)
        #     self.speedx = random.randint(-3, 3)
        #     self.speedy = random.randint(2, 9)

# Classe Bullet que representa os tiros
class Bullet(pygame.sprite.Sprite):
    # Construtor da classe.
    def __init__(self, assets, centery, centerx, facing):
        
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)
        self.bala_down = assets['balas_img'][3]
        self.bala_up = assets['balas_img'][1]
        self.bala_left = assets['balas_img'][2]
        self.bala_right = assets['balas_img'][0]
        if facing == 'left':
            self.image = self.bala_left
        elif facing =='right':
            self.image = self.bala_right
        elif facing == 'up':
            self.image = self.bala_up
        elif facing == 'down':
            self.image = self.bala_down
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.last_update = 0
        # Coloca no lugar inicial definido em x, y do constutor
        self.rect.centerx = centerx
        self.rect.centery = centery

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.image = self.bala_left
            self.speedx = -10
            self.rect.x += self.speedx
        elif keys[pygame.K_RIGHT]:
            self.image = self.bala_right
            self.speedx = 10
            self.rect.x += self.speedx
        elif keys[pygame.K_UP]:
            self.image = self.bala_up
            self.speedy = -10
            self.rect.y += self.speedy
        elif keys[pygame.K_DOWN]:
            self.image = self.bala_down
            self.speedy = 10
            self.rect.y += self.speedy
        # A bala só se move no eixo y 
        #Arrumar no eixo x
        # self.rect.x += self.speedx
        # Se o tiro passar do inicio da tela, morre.
        if self.rect.bottom < 0:
            self.kill()


def game_screen(window):
    # Variável para o ajuste de velocidade
    clock = pygame.time.Clock()

    assets = load_assets()

    # Criando um grupo de meteoros
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
    # Criando os meteoros
    for i in range(8):
        crocodilo = Crocodilo(assets)
        all_sprites.add(crocodilo)
        all_crocodilos.add(crocodilo)

    DONE = 0
    PLAYING = 1
    state = PLAYING

    keys_down = {}
    score = 0
    lives = 3

    # ===== Loop principal =====
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
                    # Dependendo da tecla, altera a velocidade.
                    keys_down[event.key] = True
                    if event.key == pygame.K_LEFT:
                        player.speedx -= 8
                    if event.key == pygame.K_RIGHT:
                        player.speedx += 8
                    if event.key == pygame.K_SPACE:
                        player.shoot()
                # Verifica se soltou alguma tecla.
                if event.type == pygame.KEYUP:
                    # Dependendo da tecla, altera a velocidade.
                    if event.key in keys_down and keys_down[event.key]:
                        if event.key == pygame.K_LEFT:
                            player.speedx += 8
                        if event.key == pygame.K_RIGHT:
                            player.speedx -= 8

        # ----- Atualiza estado do jogo
        # Atualizando a posição dos meteoros
        all_sprites.update()

        if state == PLAYING:
            # Verifica se houve colisão entre tiro e meteoro
            hits = pygame.sprite.groupcollide(all_crocodilos, all_bullets, True, True, pygame.sprite.collide_mask)
            for crocodilo in hits: # As chaves são os elementos do primeiro grupo (meteoros) que colidiram com alguma bala
                # O meteoro e destruido e precisa ser recriado
                assets['destroy_sound'].play()
                m = Crocodilo(assets)
                all_sprites.add(m)
                all_crocodilos.add(m)

                # Ganhou pontos!
                score += 100
                if score % 1000 == 0:
                    lives += 1

            # Verifica se houve colisão entre nave e meteoro
            hits = pygame.sprite.spritecollide(player, all_crocodilos, True, pygame.sprite.collide_mask)
            if len(hits) > 0:
                # Toca o som da colisão
                assets['boom_sound'].play()
                player.kill()
                time.sleep(1) # Precisa esperar senão fecha

                state = DONE

        # ----- Gera saídas
        window.fill((0, 0, 0))  # Preenche com a cor branca
        window.blit(assets['background'], (0, 0))
        # Desenhando meteoros
        all_sprites.draw(window)

        pygame.display.update()  # Mostra o novo frame para o jogador

game_screen(window)

# ===== Finalização =====
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados


