import pygame
import sys
import os

# Configurações básicas
ROWS, COLS = 4, 4
CELL_SIZE = 120
WIDTH, HEIGHT = COLS * CELL_SIZE, ROWS * CELL_SIZE

# Cores
WHITE = (255, 255, 255)
GRAY = (220, 220, 220)
BLACK = (0, 0, 0)
BLUE = (0, 100, 200)

class MundoWumpusGUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Mundo de Wumpus")

        # Caminho dos assets
        self.assets_path = os.path.join(os.path.dirname(__file__), "assets")

        # Carregar imagens
        self.images = {
            "agent": pygame.image.load(os.path.join(self.assets_path, "agent.png")),
            "wumpus": pygame.image.load(os.path.join(self.assets_path, "wumpus.png")),
            "gold": pygame.image.load(os.path.join(self.assets_path, "gold.png")),
            "pit": pygame.image.load(os.path.join(self.assets_path, "pit.png"))
        }

        # Redimensionar imagens
        for key in self.images:
            self.images[key] = pygame.transform.scale(self.images[key], (CELL_SIZE - 10, CELL_SIZE - 10))

        # Fonte para percepções
        self.font = pygame.font.SysFont("arial", 14, bold=True)

        # Mapa fixo conforme definido
        self.map = [
            [None, None, None, "pit"],
            ["wumpus", "gold", "pit", None],
            [None, None, None, None],
            ["agent", None, "pit", None]
        ]

        # Gerar percepções
        self.perceptions = self.gerar_percepcoes()

    def adjacentes(self, row, col):
        """Retorna as posições adjacentes válidas"""
        vizinhos = []
        if row > 0: vizinhos.append((row - 1, col))
        if row < ROWS - 1: vizinhos.append((row + 1, col))
        if col > 0: vizinhos.append((row, col - 1))
        if col < COLS - 1: vizinhos.append((row, col + 1))
        return vizinhos

    def gerar_percepcoes(self):
        """Cria o mapa de percepções com base na posição de Wumpus, ouro e poços"""
        percep = [[[] for _ in range(COLS)] for _ in range(ROWS)]

        for i in range(ROWS):
            for j in range(COLS):
                cell = self.map[i][j]
                if cell == "wumpus":
                    for (x, y) in self.adjacentes(i, j):
                        percep[x][y].append("Fedor")
                elif cell == "pit":
                    for (x, y) in self.adjacentes(i, j):
                        percep[x][y].append("Brisa")
                elif cell == "gold":
                    percep[i][j].append("Brilho")

        return percep

    def draw_grid(self):
        """Desenha o tabuleiro"""
        for row in range(ROWS):
            for col in range(COLS):
                x = col * CELL_SIZE
                y = row * CELL_SIZE
                pygame.draw.rect(self.screen, GRAY, (x, y, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(self.screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE), 2)

    def draw_elements(self):
        """Desenha os elementos do mapa"""
        for row in range(ROWS):
            for col in range(COLS):
                element = self.map[row][col]
                if element:
                    x = col * CELL_SIZE + 5
                    y = row * CELL_SIZE + 5
                    self.screen.blit(self.images[element], (x, y))

    def draw_perceptions(self):
        """Desenha as percepções em cada célula"""
        for row in range(ROWS):
            for col in range(COLS):
                percep = self.perceptions[row][col]
                if percep:
                    for idx, p in enumerate(percep):
                        text = self.font.render(p, True, BLUE)
                        x = col * CELL_SIZE + 8
                        y = row * CELL_SIZE + 80 + (idx * 15)
                        self.screen.blit(text, (x, y))

    def run(self):
        """Loop principal do jogo"""
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill(WHITE)
            self.draw_grid()
            self.draw_elements()
            self.draw_perceptions()  # <-- Novo método
            pygame.display.flip()
            clock.tick(30)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    gui = MundoWumpusGUI()
    gui.run()
