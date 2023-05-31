# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame
import random
from config import WIDTH, HEIGHT, INIT, GAME, QUIT
from init_screen import init_screen
from game_screen import game_screen
from game_over_screen import game_over_screen


pygame.init()
pygame.mixer.init()

# ----- Gera tela principal
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('CrocoQuest: A Caçada Mortal')

state = INIT
score = 0
while state != QUIT:
    if state == INIT:
        state = init_screen(window)
    elif state == GAME:
        lista = game_screen(window)
        state = lista[0]
        score = lista[1]
if state == QUIT:
    print(score)
    state = game_over_screen(window, score)

# ===== Finalização =====
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados

