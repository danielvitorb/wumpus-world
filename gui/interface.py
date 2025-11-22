import pygame
import sys
import os

# Configurações básicas
ROWS, COLS = 4, 4
CELL_SIZE = 120
WIDTH, HEIGHT = COLS * CELL_SIZE, ROWS * CELL_SIZE
ICON_PADDING = 10  # espaço interno para ícones (20 px total em largura/altura)

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

        # Caminho dos assets (pasta gui/assets)
        self.assets_path = os.path.join(os.path.dirname(__file__), "assets")

        # Fonte para percepções
        self.font = pygame.font.SysFont("arial", 14, bold=True)

        # Carrega imagens (com fallback)
        self.images = {}
        self._load_images()

        # Mapa fixo conforme definido
        # OBS: índices [row][col], row 0 é topo da janela
        self.map = [
            [None, None, None, "pit"],
            ["wumpus", "gold", "pit", None],
            [None, None, None, None],
            ["agent", None, "pit", None]
        ]

        # Gerar percepções (sem duplicatas)
        self.perceptions = self._gerar_percepcoes()

    def _safe_load(self, filename):
        """
        Carrega a imagem se existir; caso contrário cria um placeholder surface.
        """
        path = os.path.join(self.assets_path, filename)
        if os.path.exists(path):
            try:
                img = pygame.image.load(path).convert_alpha()
                return img
            except Exception as e:
                print(f"Erro ao carregar {path}: {e}")
        # Placeholder: surface simples com cor
        placeholder = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
        placeholder.fill((180, 180, 180))
        pygame.draw.rect(placeholder, (120, 120, 120), placeholder.get_rect(), 3)
        txt = pygame.font.SysFont("arial", 12, bold=True).render(filename.split('.')[0], True, (80, 80, 80))
        placeholder.blit(txt, (6, 6))
        return placeholder

    def _load_images(self):
        """
        Carrega e redimensiona imagens:
        - ground -> CELL_SIZE x CELL_SIZE
        - icons (agent, wumpus, gold, pit) -> (CELL_SIZE - ICON_PADDING*2)
        """
        # ground
        ground_img = self._safe_load("ground.png")
        self.images["ground"] = pygame.transform.smoothscale(ground_img, (CELL_SIZE, CELL_SIZE))

        # icons: smaller than cell to avoid overflow
        icon_size = CELL_SIZE - ICON_PADDING * 2
        for name, fname in [("agent", "agent.png"),
                             ("wumpus", "wumpus.png"),
                             ("gold", "gold.png"),
                             ("pit", "pit.png")]:
            img = self._safe_load(fname)
            # mantém proporção ao redimensionar
            img = pygame.transform.smoothscale(img, (icon_size, icon_size))
            self.images[name] = img

    def adjacentes(self, row, col):
        """Retorna as posições adjacentes válidas (cima, baixo, esquerda, direita)."""
        vizinhos = []
        if row > 0: vizinhos.append((row - 1, col))
        if row < ROWS - 1: vizinhos.append((row + 1, col))
        if col > 0: vizinhos.append((row, col - 1))
        if col < COLS - 1: vizinhos.append((row, col + 1))
        return vizinhos

    def _gerar_percepcoes(self):
        """Gera percepções sem duplicatas e retorna matriz de listas."""
        percep_sets = [[set() for _ in range(COLS)] for _ in range(ROWS)]
        for r in range(ROWS):
            for c in range(COLS):
                cell = self.map[r][c]
                if cell == "wumpus":
                    for (nr, nc) in self.adjacentes(r, c):
                        percep_sets[nr][nc].add("Fedor")
                elif cell == "pit":
                    for (nr, nc) in self.adjacentes(r, c):
                        percep_sets[nr][nc].add("Brisa")
                elif cell == "gold":
                    percep_sets[r][c].add("Brilho")
        # converter para lista ordenada (para consistência)
        return [[sorted(list(s)) for s in row] for row in percep_sets]

    def draw_ground(self):
        """Desenha o ground (fundo) em todas as células."""
        for row in range(ROWS):
            for col in range(COLS):
                x = col * CELL_SIZE
                y = row * CELL_SIZE
                self.screen.blit(self.images["ground"], (x, y))

    def draw_grid_lines(self):
        """Desenha as linhas do grid sobre o ground."""
        for row in range(ROWS):
            for col in range(COLS):
                x = col * CELL_SIZE
                y = row * CELL_SIZE
                pygame.draw.rect(self.screen, (50,50,50), (x, y, CELL_SIZE, CELL_SIZE), 2)

    def draw_elements(self):
        """Desenha ícones centralizados dentro da célula."""
        for row in range(ROWS):
            for col in range(COLS):
                element = self.map[row][col]
                if element:
                    x = col * CELL_SIZE
                    y = row * CELL_SIZE
                    img = self.images.get(element)
                    if img:
                        iw, ih = img.get_width(), img.get_height()
                        # centraliza o ícone na célula
                        offset_x = x + (CELL_SIZE - iw) // 2
                        offset_y = y + (CELL_SIZE - ih) // 2
                        self.screen.blit(img, (offset_x, offset_y))

    def draw_perceptions(self):
        """Desenha as percepções em cada célula (preto), posicionando verticalmente sem extrapolar."""
        for row in range(ROWS):
            for col in range(COLS):
                percep = self.perceptions[row][col]
                if percep:
                    max_lines = len(percep)
                    line_h = 16
                    # deixar um pequeno padding inferior (6 px)
                    y_start = row * CELL_SIZE + CELL_SIZE - 6 - (max_lines * line_h)
                    x = col * CELL_SIZE + 6
                    for idx, p in enumerate(percep):
                        text = self.font.render(p, True, PERCEPTION_COLOR)
                        y = y_start + idx * line_h
                        self.screen.blit(text, (x, y))

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # ordem de desenho: ground -> elementos -> grid lines -> percepções (ou percepções por cima das linhas se preferir)
            self.screen.fill(WHITE)
            self.draw_ground()
            self.draw_elements()
            self.draw_grid_lines()
            self.draw_perceptions()

            pygame.display.flip()
            clock.tick(30)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    gui = MundoWumpusGUI()
    gui.run()