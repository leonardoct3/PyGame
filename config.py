from os import path

# Estabelece a pasta que contem as figuras e sons.
IMG_DIR = path.join(path.dirname(__file__), 'assets', 'img')
SND_DIR = path.join(path.dirname(__file__), 'assets', 'snd')
FNT_DIR = path.join(path.dirname(__file__), 'assets', 'font')

# Criação da Window Principal
WIDTH = 900
HEIGHT = 700

# Define Dimensões
FPS = 30
CROCODILO_LATERAL_WIDTH = 150
CROCODILO_LATERAL_HEIGHT = 100
CROCODILO_VERTICAL_WIDTH = 100
CROCODILO_VERTICAL_HEIGHT = 150
FIGURA_WIDTH = 150
FIGURA_HEIGHT = 100
ILHA_WIDTH = 900
ILHA_HEIGHT = 700
BALA_WIDTH = 100
BALA_HEIGHT = 100

# Define algumas variáveis com as cores básicas
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Estados para controle do fluxo da aplicação
INIT = 0
GAME = 1
QUIT = 2
