# Importa
import pygame
import random
from os import path
from config import IMG_DIR, BLACK, FPS, GAME, QUIT


def init_screen(screen):
    
    # Variável Ajuste da Velocidade
    clock = pygame.time.Clock()

    # Carrega Tela Inicial
    background = pygame.image.load(path.join(IMG_DIR, 'Tela_Inicial.png')).convert()
    background = pygame.transform.scale(background, (900, 700))
    background_rect = background.get_rect()

    running = True
    while running:

        # Ajusta a velocidade do jogo.
        clock.tick(FPS)

        # Processa Eventos
        for event in pygame.event.get():
            # Verifica se foi fechado.
            if event.type == pygame.QUIT:
                state = QUIT
                running = False

            if event.type == pygame.KEYUP:
                state = GAME
                running = False

        # Redesenha Fundo e Sprites
        screen.fill(BLACK)
        screen.blit(background, background_rect)

        # Depois de desenhar tudo, inverte o display.
        pygame.display.flip()

    return state

