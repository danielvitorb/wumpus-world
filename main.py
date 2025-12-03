import pygame
import sys
import os
from src.gui.start_menu import StartMenu
from src.gui.interface import MundoWumpusGUI
from src.gui.asset_loader import ASSET_PATHS


def main():
    pygame.init()
    pygame.mixer.init(frequency=44100, size=-16, channels=8, buffer=2048)

    music_path = ASSET_PATHS.get("BG_MUSIC")

    if music_path and os.path.exists(music_path):
        try:
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play(-1)
        except Exception as e:
            print(f"Erro ao carregar música: {e}")
    else:
        print(f"AVISO: Música não encontrada em: {music_path}")

    menu = StartMenu()
    search_method = menu.run()

    if not search_method:
        print("Usuário fechou o jogo no menu.")
        pygame.quit()
        sys.exit()

    app = MundoWumpusGUI(search_method)
    app.run()

    pygame.mixer.music.stop()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()