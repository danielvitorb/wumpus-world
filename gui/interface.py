import pygame
import sys
from gui.asset_loader import load_all_assets, CELL_SIZE

# Configurações de Cores e Tela
ROWS, COLS = 4, 4
WIDTH, HEIGHT = COLS * CELL_SIZE, ROWS * CELL_SIZE

# Cores
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
PERCEPTION_COLOR = (0, 0, 0)  # Preto para o texto


class MundoWumpusGUI:
    def __init__(self, search_method):
        self.search_method = search_method

        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(f"Mundo de Wumpus - {search_method}")

        # Fonte para desenhar percepções (Brisa, Fedor)
        self.font = pygame.font.SysFont("arial", 14, bold=True)

        # 1. CARREGAMENTO DOS ASSETS (A Mágica acontece aqui)
        # Importamos do asset_loader corrigido
        print("Carregando assets...")
        self.images = load_all_assets()

        # -----------------------------------------------------------
        # ESTADO DO JOGO (TEMPORÁRIO - Será movido para environment.py)
        # -----------------------------------------------------------
        # Estamos mantendo aqui só para você ver a tela funcionar agora.
        # No futuro, o 'self.map' virá do objeto 'world' passado no __init__
        self.map = [
            [None, None, None, "pit"],
            ["wumpus", "gold", "pit", None],
            [None, None, None, None],
            ["agent", None, "pit", None]
        ]

        # Estado do Agente
        self.agent_pos = (3, 0)
        self.agent_direction = "UP"  # UP, DOWN, LEFT, RIGHT

        # Fog of War (quais células eu já vi)
        self.visited = [[False for _ in range(COLS)] for _ in range(ROWS)]
        self.visited[3][0] = True

        # Percepções (Isso deve vir do Environment, mas mantive placeholder para não quebrar)
        self.perceptions = [[[] for _ in range(COLS)] for _ in range(ROWS)]
        # Exemplo hardcoded só para teste visual:
        self.perceptions[2][0] = ["Fedor"]
        self.perceptions[3][1] = ["Brisa"]

    # -------------------------------------------------------
    # DESENHO
    # -------------------------------------------------------
    def draw_cell(self, r, c):
        x = c * CELL_SIZE
        y = r * CELL_SIZE
        rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

        # 1. Desenha o CHÃO em tudo
        self.screen.blit(self.images["GROUND"], (x, y))

        # 2. Lógica de Fog of War (Não visitado = Nevoa)
        if not self.visited[r][c]:
            # Se tiver a imagem UNEXPLORED carregada, usa ela, senão desenha cinza
            if "UNEXPLORED" in self.images:
                self.screen.blit(self.images["UNEXPLORED"], (x, y))
            else:
                pygame.draw.rect(self.screen, (30, 30, 30), rect)  # Retângulo cinza escuro

            pygame.draw.rect(self.screen, GRAY, rect, 1)  # Borda
            return  # Não desenha o conteúdo se não visitou

        # 3. Conteúdo da Célula
        element = self.map[r][c]

        if element == "pit":
            self.screen.blit(self.images["PIT"], (x, y))
        elif element == "gold":
            self.screen.blit(self.images["GOLD"], (x, y))
        elif element == "wumpus":
            self.screen.blit(self.images["WUMPUS"], (x, y))

        # 4. Desenhar o Agente (Sobreposto aos elementos)
        # Verifica se o agente está nesta célula
        if (r, c) == self.agent_pos:
            # Pega a imagem baseada na direção: AGENT_UP, AGENT_LEFT...
            key = f"AGENT_{self.agent_direction}"
            if key in self.images:
                self.screen.blit(self.images[key], (x, y))
            else:
                # Fallback se a direção falhar
                self.screen.blit(self.images["AGENT"], (x, y))

        # 5. Desenhar Texto das Percepções (Brisa, Fedor)
        perceps = self.perceptions[r][c]
        if perceps:
            line_h = 16
            y_start = y + CELL_SIZE - 4 - (len(perceps) * line_h)
            for idx, p in enumerate(perceps):
                # Desenha um fundo semitransparente para ler melhor o texto
                text = self.font.render(p, True, PERCEPTION_COLOR)
                self.screen.blit(text, (x + 6, y_start + idx * line_h))

        # Borda da célula
        pygame.draw.rect(self.screen, GRAY, rect, 1)

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            # Eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # TESTE RÁPIDO: Setas mudam a direção do agente (apenas visual)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP: self.agent_direction = "UP"
                    if event.key == pygame.K_DOWN: self.agent_direction = "DOWN"
                    if event.key == pygame.K_LEFT: self.agent_direction = "LEFT"
                    if event.key == pygame.K_RIGHT: self.agent_direction = "RIGHT"

            # Renderização
            self.screen.fill(WHITE)

            for r in range(ROWS):
                for c in range(COLS):
                    self.draw_cell(r, c)

            pygame.display.flip()
            clock.tick(30)

        pygame.quit()
        sys.exit()


# Bloco de execução direta para teste
if __name__ == "__main__":
    # Para rodar isso diretamente, você precisaria estar na raiz e rodar: python -m gui.interface
    try:
        gui = MundoWumpusGUI("teste")
        gui.run()
    except Exception as e:
        print(f"Erro ao rodar interface: {e}")
        print("Dica: Rode a partir do arquivo main.py na raiz do projeto.")
