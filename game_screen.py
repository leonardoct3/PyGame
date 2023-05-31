# Importa
import pygame
from Figura import Figura
from Crocodilo import Crocodilo
import time
from assets import load_assets
from config import FPS, QUIT, GAME, INIT


def game_screen(window):
    
    # Variável para o ajuste de velocidade
    clock = pygame.time.Clock()

    # Carrega Assets Utilizados
    assets = load_assets()

    # Atualiza Sprites
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

    state = GAME

    keys_down = {}
    score = 0

    # Loop principal 
    
    # Aplicação dos Sons de Fundo
    pygame.mixer.music.play(loops=-1)
    while state != QUIT:
        clock.tick(FPS)

        # Trata eventos
        for event in pygame.event.get():
            
            # Consequências
            if event.type == pygame.QUIT:
                state = QUIT
            
            # Verifica Se Teclado Está no Estado de Jogo
            if state == GAME:
                
                # Verifica se Apertou o Espaço (Tiro)
                if event.type == pygame.KEYDOWN:
                    keys_down[event.key] = True
                    if event.key == pygame.K_SPACE:
                        player.shoot()

        # Atualização do Estado do Jogo
        all_sprites.update()

        if state == GAME:
        
            hits = pygame.sprite.groupcollide(all_crocodilos, all_bullets, True, True, pygame.sprite.collide_mask)
            
            for crocodilo in hits:
                m = Crocodilo(assets)
                all_sprites.add(m)
                all_crocodilos.add(m)

                score += 10

            # Verifica Colisão do Player e Crocodilo
            hits = pygame.sprite.spritecollide(player, all_crocodilos, True, pygame.sprite.collide_mask)
            
            if len(hits) > 0:
                # Toca Som
                assets['dead'].play()
                score = 0 
                player.kill()
                time.sleep(1) 

                state = QUIT
                

        # Saídas
        window.fill((0, 0, 0))  
        window.blit(assets['background'], (0, 0))
     
        all_sprites.draw(window)

        # Pontuação
        text_surface = assets['score_font'].render("{:02d}".format(score), True, (250, 250, 0))
        text_rect = text_surface.get_rect()
        text_rect.midtop = (90,  10)
        window.blit(text_surface, text_rect)

        pygame.display.update()  

    return state
