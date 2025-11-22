import pygame
from gui.interface import MundoWumpusGUI
from start_menu import StartMenu

def main():
    pygame.init()

    # --- TOCAR TRILHA SONORA ASSIM QUE O PROGRAMA INICIA ---
    pygame.mixer.init()
    pygame.mixer.music.load("gui/assets/background.mp3")  # coloque aqui o caminho do seu áudio
    pygame.mixer.music.play(-1)  # -1 = loop infinito

    # Exibe o menu de seleção de busca
    running = True
    search_method = None

    def on_select(method):
        nonlocal search_method, running
        search_method = method
        running = False

    menu = StartMenu()
    menu.run()

    # Agora inicia o jogo com o método escolhido
    app = MundoWumpusGUI(search_method)
    app.run()

    # Quando o programa terminar, pare a música
    pygame.mixer.music.stop()

if __name__ == "__main__":
    main()
