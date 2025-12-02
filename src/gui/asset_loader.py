import os
import pygame
from src.utils.constants import CELL_SIZE

# -------------------------------------------------------
#  CONFIGURAÇÃO DE CAMINHOS (PATHS)
# -------------------------------------------------------
# 1. Pega o diretório onde ESTE arquivo está: .../Wumpus_Project/src/gui
GUI_DIR = os.path.dirname(os.path.abspath(__file__))

# 2. Sobe um nível para chegar em src: .../Wumpus_Project/src
SRC_DIR = os.path.dirname(GUI_DIR)

# 3. Sobe mais um nível para chegar na raiz: .../Wumpus_Project/
ROOT_DIR = os.path.dirname(SRC_DIR)

# 4. Define onde estão as pastas de imagens e audios
IMG_DIR = os.path.join(ROOT_DIR, "assets", "images")
AUDIO_DIR = os.path.join(ROOT_DIR, "assets", "audios")

# Dicionário com o caminho COMPLETO de cada arquivo
ASSET_PATHS = {
    # Ambiente
    "GROUND": os.path.join(IMG_DIR, "ground.png"),
    "PIT": os.path.join(IMG_DIR, "pit.png"),
    "GOLD": os.path.join(IMG_DIR, "gold.png"),
    "WUMPUS": os.path.join(IMG_DIR, "wumpus.png"),

    # Agente
    "AGENT_UP": os.path.join(IMG_DIR, "agent_up.png"),
    "AGENT_DOWN": os.path.join(IMG_DIR, "agent_down.png"),
    "AGENT_LEFT": os.path.join(IMG_DIR, "agent_left.png"),
    "AGENT_RIGHT": os.path.join(IMG_DIR, "agent_right.png"),

    # UI / Outros
    "UNEXPLORED": os.path.join(IMG_DIR, "unexplored.png"),

    # Áudio
    "BG_MUSIC": os.path.join(AUDIO_DIR, "music.mp3"),
    "SND_GOLD": os.path.join(AUDIO_DIR, "gold.mp3"),
    "SND_BREEZE": os.path.join(AUDIO_DIR, "breeze.mp3"),
    "SND_STENCH": os.path.join(AUDIO_DIR, "stench.mp3"),
    "SND_VICTORY": os.path.join(AUDIO_DIR, "victory.wav") # Mantendo .wav como combinamos
}

# -------------------------------------------------------
#  FUNÇÃO PARA CARREGAR UMA IMAGEM
# -------------------------------------------------------
def load_image(key, width=CELL_SIZE, height=CELL_SIZE):
    """
    Carrega uma imagem pelo nome da chave (key) e redimensiona.
    Usa o CELL_SIZE importado de utils.constants.
    """
    path = ASSET_PATHS.get(key)

    if not path or not os.path.exists(path):
        print(f"ERRO: Imagem não encontrada no caminho: {path}")
        error_surf = pygame.Surface((width, height))
        error_surf.fill((255, 0, 255)) # Rosa choque
        return error_surf

    try:
        image = pygame.image.load(path).convert_alpha()
        image = pygame.transform.scale(image, (width, height))
        return image
    except pygame.error as e:
        print(f"ERRO ao carregar {key}: {e}")
        return pygame.Surface((width, height))

# -------------------------------------------------------
#  CARREGAR TODOS OS ASSETS
# -------------------------------------------------------
def load_all_assets():
    """
    Retorna um dicionário com todas as imagens já carregadas.
    """
    assets = {}

    assets["GROUND"] = load_image("GROUND")
    assets["PIT"] = load_image("PIT")
    assets["GOLD"] = load_image("GOLD")
    assets["WUMPUS"] = load_image("WUMPUS")

    if "UNEXPLORED" in ASSET_PATHS:
        assets["UNEXPLORED"] = load_image("UNEXPLORED")

    assets["AGENT_UP"] = load_image("AGENT_UP")
    assets["AGENT_DOWN"] = load_image("AGENT_DOWN")
    assets["AGENT_LEFT"] = load_image("AGENT_LEFT")
    assets["AGENT_RIGHT"] = load_image("AGENT_RIGHT")

    # Default
    assets["AGENT"] = assets["AGENT_UP"]

    return assets