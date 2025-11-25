import pygame
import sys
import os

# Configurações básicas
ROWS, COLS = 4, 4
CELL_SIZE = 120
WIDTH, HEIGHT = COLS * CELL_SIZE, ROWS * CELL_SIZE
ICON_PADDING = 10  # espaço interno para ícones

# Cores
WHITE = (255, 255, 255)
GRAY = (220, 220, 220)
BLACK = (0, 0, 0)
PERCEPTION_COLOR = BLACK


class MundoWumpusGUI:
    def __init__(self, search_method):
        self.search_method = search_method

        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Mundo de Wumpus")

        # Caminho dos assets
        self.assets_path = os.path.join(os.path.dirname(__file__), "assets")

        # Fonte
        self.font = pygame.font.SysFont("arial", 14, bold=True)

        # Carrega imagens
        self.images = {}
        self._load_images()

        # Mapa fixo
        self.map = [
            [None, None, None, "pit"],
            ["wumpus", "gold", "pit", None],
            [None, None, None, None],
            ["agent", None, "pit", None]
        ]

        # Agente começa em (3,0)
        self.agent_pos = (3, 0)

        # Marca quais células já foram reveladas
        self.visited = [[False for _ in range(COLS)] for _ in range(ROWS)]
        self.visited[self.agent_pos[0]][self.agent_pos[1]] = True  # revela posição inicial

        # Percepções
        self.perceptions = self._gerar_percepcoes()

    # -------------------------------------------------------
    # LOADING
    # -------------------------------------------------------
    def _safe_load(self, filename):
        path = os.path.join(self.assets_path, filename)
        if os.path.exists(path):
            try:
                img = pygame.image.load(path).convert_alpha()
                return img
            except Exception as e:
                print(f"Erro ao carregar {path}: {e}")

        # Placeholder caso falhe
        placeholder = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
        placeholder.fill((180, 180, 180))
        pygame.draw.rect(placeholder, (120, 120, 120), placeholder.get_rect(), 3)
        txt = pygame.font.SysFont("arial", 12, bold=True).render(filename.split('.')[0], True, (80, 80, 80))
        placeholder.blit(txt, (6, 6))
        return placeholder

    def _load_images(self):
        # ground
        ground = self._safe_load("ground.png")
        self.images["ground"] = pygame.transform.smoothscale(ground, (CELL_SIZE, CELL_SIZE))

        # imagem de célula não explorada
        unexplored = self._safe_load("unexplored.png")
        self.images["unexplored"] = pygame.transform.smoothscale(unexplored, (CELL_SIZE, CELL_SIZE))

        # icons
        icon_size = CELL_SIZE - ICON_PADDING * 2
        for name, fname in [
            ("agent", "agent.png"),
            ("wumpus", "wumpus.png"),
            ("gold", "gold.png"),
            ("pit", "pit.png")
        ]:
            img = self._safe_load(fname)
            img = pygame.transform.smoothscale(img, (icon_size, icon_size))
            self.images[name] = img

    # -------------------------------------------------------
    # PERCEPÇÕES
    # -------------------------------------------------------
    def adjacentes(self, row, col):
        v = []
        if row > 0: v.append((row - 1, col))
        if row < ROWS - 1: v.append((row + 1, col))
        if col > 0: v.append((row, col - 1))
        if col < COLS - 1: v.append((row, col + 1))
        return v

    def _gerar_percepcoes(self):
        p = [[set() for _ in range(COLS)] for _ in range(ROWS)]

        for r in range(ROWS):
            for c in range(COLS):
                cell = self.map[r][c]

                if cell == "wumpus":
                    for nr, nc in self.adjacentes(r, c):
                        p[nr][nc].add("Fedor")

                elif cell == "pit":
                    for nr, nc in self.adjacentes(r, c):
                        p[nr][nc].add("Brisa")

                elif cell == "gold":
                    p[r][c].add("Brilho")

        return [[sorted(list(s)) for s in row] for row in p]

    # -------------------------------------------------------
    # DRAWING
    # -------------------------------------------------------
    def draw_cell(self, r, c):
        x = c * CELL_SIZE
        y = r * CELL_SIZE
        rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

        # sempre desenha ground primeiro
        self.screen.blit(self.images["ground"], (x, y))

        # se NÃO visitada → desenha unexplored e sai
        if not self.visited[r][c]:
            self.screen.blit(self.images["unexplored"], (x, y))
            return

        # desenha elemento da célula
        element = self.map[r][c]
        if element:
            img = self.images[element]
            iw, ih = img.get_width(), img.get_height()
            ox = x + (CELL_SIZE - iw) // 2
            oy = y + (CELL_SIZE - ih) // 2
            self.screen.blit(img, (ox, oy))

        # desenha percepções
        perceps = self.perceptions[r][c]
        if perceps:
            line_h = 16
            y_start = y + CELL_SIZE - 4 - (len(perceps) * line_h)
            for idx, p in enumerate(perceps):
                text = self.font.render(p, True, PERCEPTION_COLOR)
                self.screen.blit(text, (x + 6, y_start + idx * line_h))

        # grid por cima
        pygame.draw.rect(self.screen, (50, 50, 50), rect, 2)

    # -------------------------------------------------------
    # LOOP PRINCIPAL
    # -------------------------------------------------------
    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill(WHITE)

            # desenha tudo célula por célula com fog of war
            for r in range(ROWS):
                for c in range(COLS):
                    self.draw_cell(r, c)

            pygame.display.flip()
            clock.tick(30)

        pygame.quit()
        sys.exit()


# Debug
if __name__ == "__main__":
    gui = MundoWumpusGUI("bfs")
    gui.run()
