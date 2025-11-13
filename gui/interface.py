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

        # Carregar imagens (se não existir, o pygame vai lançar erro — mantenha os arquivos em assets/)
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

        # Gerar percepções (agora sem duplicatas)
        self.perceptions = self.gerar_percepcoes()

    def adjacentes(self, row, col):
        """Retorna as posições adjacentes válidas (ordem: cima, baixo, esquerda, direita)."""
        vizinhos = []
        if row > 0: vizinhos.append((row - 1, col))
        if row < ROWS - 1: vizinhos.append((row + 1, col))
        if col > 0: vizinhos.append((row, col - 1))
        if col < COLS - 1: vizinhos.append((row, col + 1))
        return vizinhos

    def gerar_percepcoes(self):
        """
        Cria o mapa de percepções com base na posição de Wumpus, ouro e poços.
        Usa sets temporariamente para evitar duplicatas.
        Retorna uma matriz de listas (percepções por célula).
        """
        percep_sets = [[set() for _ in range(COLS)] for _ in range(ROWS)]

        for i in range(ROWS):
            for j in range(COLS):
                cell = self.map[i][j]
                if cell == "wumpus":
                    for (r, c) in self.adjacentes(i, j):
                        percep_sets[r][c].add("Fedor")
                elif cell == "pit":
                    for (r, c) in self.adjacentes(i, j):
                        percep_sets[r][c].add("Brisa")
                elif cell == "gold":
                    percep_sets[i][j].add("Brilho")

        # Converte sets para listas (mantendo ordem estável)
        percep_list = [[sorted(list(s)) for s in row] for row in percep_sets]
        return percep_list

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
        """Desenha as percepções em cada célula (preto), posicionando verticalmente para não extrapolar."""
        for row in range(ROWS):
            for col in range(COLS):
                percep = self.perceptions[row][col]
                if percep:
                    # vertical layout: alinhar a lista de percepções acima da borda inferior da célula
                    max_lines = len(percep)
                    # espaço entre linhas
                    line_h = 16
                    # y inicial de modo que o último texto fique a 6px do fundo da célula
                    y_start = row * CELL_SIZE + CELL_SIZE - 6 - (max_lines * line_h)
                    for idx, p in enumerate(percep):
                        text = self.font.render(p, True, BLACK)  # mudou para preto
                        x = col * CELL_SIZE + 8
                        y = y_start + idx * line_h
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
            self.draw_perceptions()
            pygame.display.flip()
            clock.tick(30)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    gui = MundoWumpusGUI()
    gui.run()
