import pygame
import sys
from gui.asset_loader import load_all_assets, CELL_SIZE
from core.environment import WumpusEnvironment
from agent.player import Agent

# Configurações de Tela
# Vamos dar um espaço extra na altura para o texto de status
HUD_HEIGHT = 60
ROWS, COLS = 4, 4
WIDTH = COLS * CELL_SIZE
HEIGHT = (ROWS * CELL_SIZE) + HUD_HEIGHT

# Cores
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
BG_COLOR = (20, 20, 20)
TEXT_COLOR = (255, 255, 255)
PERCEPTION_COLOR = (255, 255, 0)  # Amarelo para destacar alertas


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

        # --- ALTERAÇÕES AQUI ---
        # 1. Inicializa com o tempo atual para forçar a espera inicial
        self.last_move_time = pygame.time.get_ticks()

        # 2. Aumentamos o delay para 800ms (quase 1 segundo por passo)
        # Se quiser ainda mais lento, coloque 1000 ou 1200
        self.move_delay = 2000

    # -------------------------------------------------------
    # DESENHO
    # -------------------------------------------------------
    def draw_cell(self, r, c):
        x = c * CELL_SIZE
        y = r * CELL_SIZE
        rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

        # 1. Chão Base
        self.screen.blit(self.images["GROUND"], (x, y))

        # 2. Fog of War (Opcional - Para debug, mostramos tudo, mas escurecemos o não visitado)
        # Se quiser esconder totalmente, descomente a lógica abaixo
        is_visited = (r, c) in self.agent.visited

        # Desenha o conteúdo REAL do mundo (Trapaça visual para quem assiste)
        element = self.world.grid[r][c]
        if element == 'P':
            self.screen.blit(self.images["PIT"], (x, y))
        elif element == 'G' and not self.agent.has_gold:
            self.screen.blit(self.images["GOLD"], (x, y))
        elif element == 'W':
            self.screen.blit(self.images["WUMPUS"], (x, y))

        # Se não visitado, desenha uma camada semi-transparente ou ícone 'unexplored'
        if not is_visited:
            if "UNEXPLORED" in self.images:
                # Desenha com transparência se possível, ou opaco
                self.screen.blit(self.images["UNEXPLORED"], (x, y))
            else:
                s = pygame.Surface((CELL_SIZE, CELL_SIZE))
                s.set_alpha(150)
                s.fill((0, 0, 0))
                self.screen.blit(s, (x, y))

        # 3. Agente
        if (r, c) == self.agent.pos:
            key = f"AGENT_{self.agent_direction}"
            if key in self.images:
                self.screen.blit(self.images[key], (x, y))
            else:
                self.screen.blit(self.images["AGENT"], (x, y))

        # 4. Percepções (Brisa, Fedor) - Baseado no que o AGENTE sentiu
        # Só desenhamos percepções se o agente estiver lá ou já visitou
        if is_visited:
            # Pegamos do mundo o que existe de verdade nessa célula
            percepts = self.world.get_percepts((r, c))

            if self.agent.has_gold and "Brilho" in percepts:
                percepts.remove("Brilho")

            line_h = 14
            y_start = y + CELL_SIZE - 4 - (len(percepts) * line_h)
            for idx, p in enumerate(percepts):
                # Desenha sombra preta para ler melhor
                txt_shadow = self.font_percept.render(p, True, (0, 0, 0))
                txt = self.font_percept.render(p, True, PERCEPTION_COLOR)
                self.screen.blit(txt_shadow, (x + 7, y_start + idx * line_h + 1))
                self.screen.blit(txt, (x + 6, y_start + idx * line_h))

        # Borda
        pygame.draw.rect(self.screen, GRAY, rect, 1)

    def draw_hud(self):
        """Desenha o painel de informações na parte inferior."""
        base_y = ROWS * CELL_SIZE
        pygame.draw.rect(self.screen, BG_COLOR, (0, base_y, WIDTH, HUD_HEIGHT))

        # Linha 1: Algoritmo e Status
        status_txt = f"Algoritmo: {self.search_method.upper()} | Status: {self.agent.message}"
        surf = self.font_info.render(status_txt, True, TEXT_COLOR)
        self.screen.blit(surf, (10, base_y + 10))

        # Linha 2: Posição e Ouro
        gold_txt = "Sim" if self.agent.has_gold else "Não"
        info_txt = f"Posição: {self.agent.pos} | Tem Ouro? {gold_txt}"
        surf2 = self.font_info.render(info_txt, True, TEXT_COLOR)
        self.screen.blit(surf2, (10, base_y + 35))

    def update_direction(self, move_action):
        """Atualiza a variável de direção baseada no movimento (dr, dc)."""
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
            # 1. Eventos (Fechar janela)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # 2. Lógica da IA (Temporizada)
            current_time = pygame.time.get_ticks()
            if not self.agent.game_over:
                if current_time - self.last_move_time > self.move_delay:

                    # Passo A: O agente Pensa (Planeja o caminho)
                    self.agent.think(self.search_method)

                    # Passo B: O agente Executa um movimento do plano
                    move_action = self.agent.move()

                    # Atualiza visual do boneco virando
                    if move_action != (0, 0):
                        self.update_direction(move_action)

                    self.last_move_time = current_time

            # 3. Renderização
            self.screen.fill(BG_COLOR)

            for r in range(ROWS):
                for c in range(COLS):
                    self.draw_cell(r, c)

            self.draw_hud()

            pygame.display.flip()
            clock.tick(30)

        pygame.quit()
        sys.exit()


# Bloco de teste direto
if __name__ == "__main__":
    # Para testar apenas a interface sem o menu
    try:
        app = MundoWumpusGUI("astar")
        app.run()
    except Exception as e:
        print(e)
