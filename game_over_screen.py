# Importa
import pygame
from os import path
from game_screen import game_screen
from config import IMG_DIR, BLACK, FPS, GAME, QUIT


def game_over_screen(screen, score):
    # Variável para o ajuste de velocidade
    clock = pygame.time.Clock()

    # Carrega o fundo da tela inicial
    background = pygame.image.load(path.join(IMG_DIR, 'Crocodilo_final.png')).convert()
    background = pygame.transform.scale(background, (900, 700))
    background_rect = background.get_rect()

    running = True
    username = ''

    font_g =  pygame.font.Font('assets/font/PressStart2P.ttf', 24)
    font_m =  pygame.font.Font('assets/font/PressStart2P.ttf', 24)

    while running:

        # Ajusta a velocidade do jogo.
        clock.tick(FPS)

        # Processa os eventos (mouse, teclado, botão, etc).
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = QUIT
                running = False
                
            # keys = pygame.key.get_pressed()
            # if keys[pygame.K_BACKSPACE]:
            #     state = GAME
            #     game_screen(screen)

            #quando usuário digita algo
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    state = GAME
                    game_screen(screen)

                elif event.key == pygame.K_BACKSPACE and len(username) > 0:
                    # Quando usuário aperta a tecla para apagar o texto
                    username = username[:len(username)-1]  
                                      
                else:
                    # Concatena a letra digitada pelo jogador
                    username += event.unicode

        # A cada loop, redesenha o fundo e os sprites
        screen.fill(BLACK)
        screen.blit(background, background_rect)

        # Texto Usuário
        text = font_g.render(f'{username}', True, (255, 255, 255))
        screen.blit(text, (450, 10))

        text = font_g.render(f'{score}', True, (255, 255, 255))
        screen.blit(text, (320, 55))
        
        # Depois de desenhar tudo, inverte o display.
        pygame.display.flip()

    # Salvando informações no arquivo
    with open('score.txt', 'a') as arquivo:
        conteudo = f'{username} - {score}\n'
        arquivo.write(conteudo)

    return state