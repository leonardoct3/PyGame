import pygame
from Figura import Figura
from Crocodilo import Crocodilo
from Bullet import Bullet
import time
from assets import load_assets
from config import FPS


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

    QUIT = 0
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

                state = QUIT

        # ----- Gera saídas
        window.fill((0, 0, 0))  
        window.blit(assets['background'], (0, 0))
     
        all_sprites.draw(window)

        text_surface = assets['score_font'].render("{:02d}".format(score), True, (250, 250, 0))
        text_rect = text_surface.get_rect()
        text_rect.midtop = (90,  10)
        window.blit(text_surface, text_rect)

        pygame.display.update()  

    return state
