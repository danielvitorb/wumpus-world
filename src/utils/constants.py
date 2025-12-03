# src/utils/constants.py

# --- CONFIGURAÇÕES DO GRID ---
CELL_SIZE = 120  # Tamanho de cada célula em pixels
ROWS = 4
COLS = 4

# --- DIMENSÕES DA TELA ---
HUD_HEIGHT = 100
WIDTH = COLS * CELL_SIZE
HEIGHT = (ROWS * CELL_SIZE) + HUD_HEIGHT

# --- CORES (RGB) ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BG_COLOR = (20, 20, 20)
TEXT_COLOR = (255, 255, 255)
PERCEPTION_COLOR = (255, 255, 0) # Amarelo
GREEN = (34, 139, 34)
RED = (178, 34, 34)
BLUE = (70, 130, 180)
LIGHT_GRAY = (200, 200, 200)

# --- CONFIGURAÇÕES DE JOGO ---
MOVE_DELAY = 5000 # Tempo entre movimentos (ms)