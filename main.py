from start_menu import StartMenu
from gui.interface import MundoWumpusGUI

def main():
    # --- 1) Exibir tela inicial com botões ---
    menu = StartMenu()
    search_method = menu.run()   # retorna "bfs", "dfs" ou "astar"

    print(f"Método escolhido: {search_method}")

    # --- 2) Executar a interface passando o método de busca ---
    app = MundoWumpusGUI(search_method=search_method)
    app.run()

if __name__ == "__main__":
    main()
