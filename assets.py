# Importa
import pygame
from config import ILHA_WIDTH, ILHA_HEIGHT, CROCODILO_LATERAL_WIDTH, CROCODILO_LATERAL_HEIGHT, CROCODILO_VERTICAL_HEIGHT, CROCODILO_VERTICAL_WIDTH, FIGURA_HEIGHT, FIGURA_WIDTH, BALA_HEIGHT, BALA_WIDTH

# Carrega as Assets
def load_assets():
    
    assets = {}
    
    # Ilha de Fundo
    assets['background'] = pygame.image.load('assets/img/Ilha.png').convert()
    assets['background'] = pygame.transform.scale(assets['background'], (ILHA_WIDTH, ILHA_HEIGHT))
    
    # Crocodilo
    crocodilos_desce_img = []
    crocodilos_direita_img = []
    crocodilos_esquerda_img = []
    crocodilos_sobe_img = []
    
    for i in range (0,3):
        nome = 'assets/img/crocodilo_desce({}).png'.format(i)
        img = pygame.image.load(nome).convert_alpha()
        img = pygame.transform.scale(img, (CROCODILO_VERTICAL_WIDTH, CROCODILO_VERTICAL_HEIGHT))
        crocodilos_desce_img.append(img)
    
    for i in range (0,3):
        nome = 'assets/img/crocodilo_direita({}).png'.format(i)
        img = pygame.image.load(nome).convert_alpha()
        img = pygame.transform.scale(img, (CROCODILO_LATERAL_WIDTH, CROCODILO_LATERAL_HEIGHT))
        crocodilos_direita_img.append(img)
    
    for i in range (0,3):
        nome = 'assets/img/crocodilo_esquerda({}).png'.format(i)
        img = pygame.image.load(nome).convert_alpha()
        img = pygame.transform.scale(img, (CROCODILO_LATERAL_WIDTH, CROCODILO_LATERAL_HEIGHT))
        crocodilos_esquerda_img.append(img)
    
    for i in range (0,3):
        nome = 'assets/img/crocodilo_sobe({}).png'.format(i)
        img = pygame.image.load(nome).convert_alpha()
        img = pygame.transform.scale(img, (CROCODILO_VERTICAL_WIDTH, CROCODILO_VERTICAL_HEIGHT))
        crocodilos_sobe_img.append(img)
    
    assets['crocodilos_desce_img'] = crocodilos_desce_img
    assets['crocodilos_sobe_img'] = crocodilos_sobe_img
    assets['crocodilos_esquerda_img'] = crocodilos_esquerda_img
    assets['crocodilos_direita_img'] = crocodilos_direita_img
    
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
