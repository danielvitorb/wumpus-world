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

        # Mapa fixo conforme sua imagem
        self.map = [
            ["wumpus", None, None, "pit"],
            [None, "gold", "pit", None],
            [None, None, None, None],
            ["agent", None, "pit", None]
        ]

    def draw_grid(self):
        for row in range(ROWS):
            for col in range(COLS):
                x = col * CELL_SIZE
                y = row * CELL_SIZE
                pygame.draw.rect(self.screen, GRAY, (x, y, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(self.screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE), 2)

    def draw_elements(self):
        for row in range(ROWS):
            for col in range(COLS):
                element = self.map[row][col]
                if element:
                    x = col * CELL_SIZE + 5
                    y = row * CELL_SIZE + 5
                    self.screen.blit(self.images[element], (x, y))

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill(WHITE)
            self.draw_grid()
            self.draw_elements()
            pygame.display.flip()
            clock.tick(30)

        pygame.quit()
        sys.exit()
