# Importa
import pygame
from os import path
from game_screen import game_screen
from config import IMG_DIR, BLACK, FPS, GAME, QUIT


def game_over_screen(screen):
    # Variável para o ajuste de velocidade
    clock = pygame.time.Clock()

    # Carrega o fundo da tela inicial
    background = pygame.image.load(path.join(IMG_DIR, 'Crocodilo_final.png')).convert()
    background = pygame.transform.scale(background, (900, 700))
    background_rect = background.get_rect()

    running = True
    while running:

        # Ajusta a velocidade do jogo.
        clock.tick(FPS)

        # Processa os eventos (mouse, teclado, botão, etc).
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = QUIT
                running = False
                
            keys = pygame.key.get_pressed()
            if keys[pygame.K_BACKSPACE]:
                state = GAME
                game_screen(screen)

        # A cada loop, redesenha o fundo e os sprites
        screen.fill(BLACK)
        screen.blit(background, background_rect)

        # Depois de desenhar tudo, inverte o display.
        pygame.display.flip()

    return state