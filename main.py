import pygame
import os
from gui.interface import MundoWumpusGUI
from gui.start_menu import StartMenu
from gui.asset_loader import ASSET_PATHS


def main():
    pygame.init()
    pygame.mixer.init()

    music_path = ASSET_PATHS.get("BG_MUSIC")

    pygame.mixer.music.load(music_path)
    pygame.mixer.music.play(-1)

    menu = StartMenu()

    search_method = menu.run()

    print(f"Método escolhido pelo usuário: {search_method}")

    app = MundoWumpusGUI(search_method)
    app.run()

    pygame.mixer.music.stop()


if __name__ == "__main__":
    main()