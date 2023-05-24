# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame
import random

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
FIGURA_WIDTH = 200
FIGURA_HEIGHT = 179
ILHA_WIDTH = 900
ILHA_HEIGHT = 700

def load_assets():
    assets = {}
    assets['background'] = pygame.image.load('assets/img/Ilha.png').convert()
    assets['background'] = pygame.transform.scale(assets['background'], (ILHA_WIDTH, ILHA_HEIGHT))
    assets['crocodilo_img'] = pygame.image.load('assets/img/Crocodilo.png').convert_alpha()
    assets['crocodilo_img'] = pygame.transform.scale(assets['crocodilo_img'], (CROCODILO_WIDTH, CROCODILO_HEIGHT))
    assets['figura_img'] = pygame.image.load('assets/img/Humano.png').convert_alpha()
    assets['figura_img'] = pygame.transform.scale(assets['figura_img'], (FIGURA_WIDTH, FIGURA_HEIGHT))
    assets['bullet_img'] = pygame.image.load('assets/img/laserRed16.png').convert_alpha()

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

        self.image = assets['figura_img']
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT / 2
        self.speedx = 0
        self.groups = groups
        self.assets = assets

        # Só será possível atirar uma vez a cada 250 milissegundos
        self.last_shot = pygame.time.get_ticks()
        self.shoot_ticks = 250

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
            new_bullet = Bullet(self.assets, self.rect.top, self.rect.centerx)
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
            self.rect.y = -50
            self.rect.centerx = WIDTH / 2
            self.speedy = random.randint(2, 9)
            self.speedx = 0
        elif self.direcao == 2:
            self.rect.y = 650
            self.rect.centerx = WIDTH / 2
            self.speedy = random.randint(-9, -2)
            self.speedx = 0
        elif self.direcao == 3:
            self.rect.centery = HEIGHT / 2
            self.rect.x = -50
            self.speedx = random.randint(2, 9)
            self.speedy = 0
        elif self.direcao == 4:
            self.rect.centery = HEIGHT / 2
            self.rect.x = WIDTH + 50
            self.speedy = random.randint(-9, -2)
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
    def __init__(self, assets, bottom, centerx):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.image = assets['bullet_img']
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()

        # Coloca no lugar inicial definido em x, y do constutor
        self.rect.centerx = centerx
        self.rect.bottom = bottom
        self.speedy = -10  # Velocidade fixa para cima

    def update(self):
        # A bala só se move no eixo y 
        #Arrumar no eixo x
        self.rect.y += self.speedy
        self.rect.x += self.speedx

        # Se o tiro passar do inicio da tela, morre.
        if self.rect.bottom < 0:
            self.kill()

    def update(self):
        # Verifica o tick atual.
        now = pygame.time.get_ticks()
        # Verifica quantos ticks se passaram desde a ultima mudança de frame.
        elapsed_ticks = now - self.last_update

        # Se já está na hora de mudar de imagem...
        if elapsed_ticks > self.frame_ticks:
            # Marca o tick da nova imagem.
            self.last_update = now

            # Avança um quadro.
            self.frame += 1

            # Verifica se já chegou no final da animação.
            if self.frame == len(self.explosion_anim):
                # Se sim, tchau explosão!
                self.kill()
            else:
                # Se ainda não chegou ao fim da explosão, troca de imagem.
                center = self.rect.center
                self.image = self.explosion_anim[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

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
    EXPLODING = 2
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
            for crocodilo in hits:
                assets['destroy_sound'].play()
                m = crocodilo(assets)
                all_sprites.add(m)
                all_crocodilos.add(m)

                # No lugar do meteoro antigo, adicionar uma explosão.
                explosao = Explosion(meteor.rect.center, assets)
                all_sprites.add(explosao)

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
                lives -= 1
                explosao = Explosion(player.rect.center, assets)
                all_sprites.add(explosao)
                state = EXPLODING
                keys_down = {}
                explosion_tick = pygame.time.get_ticks()
                explosion_duration = explosao.frame_ticks * len(explosao.explosion_anim) + 400
        elif state == EXPLODING:
            now = pygame.time.get_ticks()
            if now - explosion_tick > explosion_duration:
                if lives == 0:
                    state = DONE
                else:
                    state = PLAYING
                    player = Figura(groups, assets)
                    all_sprites.add(player)

        # ----- Gera saídas
        window.fill((0, 0, 0))  # Preenche com a cor branca
        window.blit(assets['background'], (0, 0))
        # Desenhando meteoros
        all_sprites.draw(window)

        pygame.display.update()  # Mostra o novo frame para o jogador

game_screen(window)

# ===== Finalização =====
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados


