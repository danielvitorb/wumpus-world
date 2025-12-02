import pygame
import sys
import time
from gui.asset_loader import load_all_assets, CELL_SIZE
from core.environment import WumpusEnvironment
from agent.player import Agent
from gui.game_over import GameOverScreen  # Importa a nova tela

HUD_HEIGHT = 100
ROWS, COLS = 4, 4
WIDTH = COLS * CELL_SIZE
HEIGHT = (ROWS * CELL_SIZE) + HUD_HEIGHT

WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
BG_COLOR = (20, 20, 20)
TEXT_COLOR = (255, 255, 255)
PERCEPTION_COLOR = (255, 255, 0)


class MundoWumpusGUI:
    def __init__(self, search_method):
        self.search_method = search_method

        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(f"Wumpus World AI - {search_method.upper()}")

        self.font_info = pygame.font.SysFont("arial", 16)
        self.font_percept = pygame.font.SysFont("arial", 12, bold=True)

        print("Carregando assets...")
        self.images = load_all_assets()

        self.world = WumpusEnvironment()
        self.agent = Agent(self.world)

        self.agent_direction = "UP"

        # Controle de Tempo e Animação
        self.last_move_time = pygame.time.get_ticks()
        self.move_delay = 1000

        # Para calcular métrica de tempo total
        self.start_time = time.time()
        self.end_time = None

    def draw_cell(self, r, c):
        x = c * CELL_SIZE
        y = r * CELL_SIZE
        rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

        self.screen.blit(self.images["GROUND"], (x, y))

        is_visited = (r, c) in self.agent.visited

        element = self.world.grid[r][c]
        if element == 'P':
            self.screen.blit(self.images["PIT"], (x, y))
        elif element == 'G' and not self.agent.has_gold:
            self.screen.blit(self.images["GOLD"], (x, y))
        elif element == 'W':
            self.screen.blit(self.images["WUMPUS"], (x, y))

        if not is_visited:
            if "UNEXPLORED" in self.images:
                self.screen.blit(self.images["UNEXPLORED"], (x, y))
            else:
                s = pygame.Surface((CELL_SIZE, CELL_SIZE))
                s.set_alpha(150)
                s.fill((0, 0, 0))
                self.screen.blit(s, (x, y))

        if (r, c) == self.agent.pos:
            key = f"AGENT_{self.agent_direction}"
            if key in self.images:
                self.screen.blit(self.images[key], (x, y))
            else:
                self.screen.blit(self.images["AGENT"], (x, y))

        if is_visited:
            percepts = self.world.get_percepts((r, c))
            if self.agent.has_gold and "Brilho" in percepts:
                percepts.remove("Brilho")

            line_h = 14
            y_start = y + CELL_SIZE - 4 - (len(percepts) * line_h)
            for idx, p in enumerate(percepts):
                txt_shadow = self.font_percept.render(p, True, (0, 0, 0))
                txt = self.font_percept.render(p, True, PERCEPTION_COLOR)
                self.screen.blit(txt_shadow, (x + 7, y_start + idx * line_h + 1))
                self.screen.blit(txt, (x + 6, y_start + idx * line_h))

        pygame.draw.rect(self.screen, GRAY, rect, 1)

    def draw_hud(self):
        base_y = ROWS * CELL_SIZE
        pygame.draw.rect(self.screen, BG_COLOR, (0, base_y, WIDTH, HUD_HEIGHT))

        status_txt = f"Algoritmo: {self.search_method.upper()} | Status: {self.agent.message}"
        surf = self.font_info.render(status_txt, True, TEXT_COLOR)
        self.screen.blit(surf, (10, base_y + 10))

        gold_txt = "Sim" if self.agent.has_gold else "Não"
        info_txt = f"Posição: {self.agent.pos} | Tem Ouro? {gold_txt}"
        surf2 = self.font_info.render(info_txt, True, TEXT_COLOR)
        self.screen.blit(surf2, (10, base_y + 35))

        # Mostra métricas em tempo real também
        metrics_txt = f"Nós: {self.agent.total_nodes} | Passos: {self.agent.total_steps}"
        surf3 = self.font_info.render(metrics_txt, True, (200, 200, 200))
        self.screen.blit(surf3, (10, base_y + 65))

    def update_direction(self, move_action):
        dr, dc = move_action
        if dr == -1:
            self.agent_direction = "UP"
        elif dr == 1:
            self.agent_direction = "DOWN"
        elif dc == -1:
            self.agent_direction = "LEFT"
        elif dc == 1:
            self.agent_direction = "RIGHT"

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Lógica da IA
            current_time = pygame.time.get_ticks()
            if not self.agent.game_over:
                if current_time - self.last_move_time > self.move_delay:
                    self.agent.think(self.search_method)
                    move_action = self.agent.move()
                    if move_action != (0, 0):
                        self.update_direction(move_action)
                    self.last_move_time = current_time
            else:
                # JOGO ACABOU!
                # Espera 1 segundo para o usuário ler a mensagem de status e depois muda de tela
                pygame.time.delay(1000)

                # Calcula tempo final
                if self.end_time is None:
                    self.end_time = time.time()

                duration = self.end_time - self.start_time

                # Prepara dados para a tela final
                metrics = {
                    "resultado": "VITÓRIA" if self.agent.won else "DERROTA",
                    "metodo": self.search_method.upper(),
                    "nos": self.agent.total_nodes,
                    "custo": self.agent.total_steps,
                    "tempo": f"{duration:.2f}s"
                }

                # Abre tela de game over
                screen_over = GameOverScreen(metrics)
                screen_over.run()
                return  # Encerra o jogo

            self.screen.fill(BG_COLOR)
            for r in range(ROWS):
                for c in range(COLS):
                    self.draw_cell(r, c)
            self.draw_hud()

            pygame.display.flip()
            clock.tick(30)

        pygame.quit()
        sys.exit()
