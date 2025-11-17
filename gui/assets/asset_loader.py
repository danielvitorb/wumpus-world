import os
import pygame

# -------------------------------------------------------
#  PATHS DAS IMAGENS
# -------------------------------------------------------
BASE_PATH = os.path.dirname(os.path.abspath(__file__))

ASSET_PATHS = {
    "GROUND": os.path.join(BASE_PATH, "ground.png"),
    "AGENT": os.path.join(BASE_PATH, "agent.png"),
    "WUMPUS": os.path.join(BASE_PATH, "wumpus.png"),
    "PIT": os.path.join(BASE_PATH, "pit.png"),
    "GOLD": os.path.join(BASE_PATH, "gold.png"),
}

# -------------------------------------------------------
#  TAMANHO DAS CÉLULAS
# -------------------------------------------------------
CELL_SIZE = 64


# -------------------------------------------------------
#  CARREGAR IMAGEM PADRÃO
# -------------------------------------------------------
def load_image(name, full_cell=True):
    """
    Carrega imagem e opcionalmente escala para ocupar a célula inteira.
    """
    path = ASSET_PATHS[name]
    image = pygame.image.load(path).convert_alpha()

    if full_cell:
        image = pygame.transform.scale(image, (CELL_SIZE, CELL_SIZE))

    return image


# -------------------------------------------------------
#  CARREGAR TODOS OS ASSETS UMA VEZ
# -------------------------------------------------------
def load_all_assets():
    """
    Retorna um dicionário com todas as imagens carregadas e prontas.
    """
    assets = {
        "GROUND": load_image("GROUND", full_cell=True),
        "PIT": load_image("PIT", full_cell=True),     # pits ocupam a célula inteira
        "GOLD": load_image("GOLD", full_cell=True),
        "WUMPUS": load_image("WUMPUS", full_cell=True),

        # O agente é especial: não queremos escalar direto para CELL_SIZE
        "AGENT_BASE": pygame.image.load(ASSET_PATHS["AGENT"]).convert_alpha(),
    }

    return assets


# -------------------------------------------------------
#  ROTACIONAR A IMAGEM DO AGENTE COM BASE NA DIREÇÃO
# -------------------------------------------------------
def get_agent_sprite(assets, direction):
    """
    Retorna a sprite do agente rotacionada conforme sua direção:
        UP, RIGHT, DOWN, LEFT
    """
    base = assets["AGENT_BASE"]

    if direction == "UP":
        rotated = pygame.transform.rotate(base, 0)
    elif direction == "RIGHT":
        rotated = pygame.transform.rotate(base, -90)
    elif direction == "DOWN":
        rotated = pygame.transform.rotate(base, 180)
    elif direction == "LEFT":
        rotated = pygame.transform.rotate(base, 90)
    else:
        rotated = base

    # Reduz para caber bonitinho dentro da célula
    size = int(CELL_SIZE * 0.75)
    rotated = pygame.transform.scale(rotated, (size, size))

    return rotated
