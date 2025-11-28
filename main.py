import pygame
import os
from gui.interface import MundoWumpusGUI
from start_menu import StartMenu
# Importamos os caminhos para garantir que a música seja encontrada
from gui.asset_loader import ASSET_PATHS


def main():
    pygame.init()
    pygame.mixer.init()

    # --- 1. TOCAR TRILHA SONORA ---
    # Usamos o caminho que definimos no asset_loader (lá estava 'background.mp3')
    music_path = ASSET_PATHS.get("BG_MUSIC")

    # Verificação de segurança para não travar se o audio não existir
    if music_path and os.path.exists(music_path):
        try:
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play(-1)  # Loop infinito
            print(f"Tocando música: {music_path}")
        except pygame.error as e:
            print(f"Erro ao tocar música: {e}")
    else:
        print(f"AVISO: Arquivo de música não encontrado em: {music_path}")
        print("Verifique se o nome na pasta assets/audios é 'background.mp3' ou 'music.mp3'")

    # --- 2. MENU DE SELEÇÃO ---
    menu = StartMenu()

    # AQUI ESTAVA O ERRO: O menu.run() retorna a string ("bfs", "astar").
    # Precisamos capturar esse valor em uma variável.
    search_method = menu.run()

    print(f"Método escolhido pelo usuário: {search_method}")

    # --- 3. INICIAR O JOGO ---
    # Passamos a escolha para a interface
    app = MundoWumpusGUI(search_method)
    app.run()

    # Quando fechar o jogo
    pygame.mixer.music.stop()


if __name__ == "__main__":
    main()