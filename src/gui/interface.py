import pygame
import sys
import time

# --- IMPORTS DA NOVA ESTRUTURA ---
from src.gui.asset_loader import load_all_assets, ASSET_PATHS
from src.core.environment import WumpusEnvironment
from src.agent.player import Agent
from src.gui.game_over import GameOverScreen

# Importamos TUDO de constants.py para limpar este arquivo
from src.utils.constants import (
    CELL_SIZE, ROWS, COLS, WIDTH, HEIGHT, HUD_HEIGHT,
    WHITE, GRAY, BG_COLOR, TEXT_COLOR, PERCEPTION_COLOR,
    MOVE_DELAY
)


class MundoWumpusGUI:
    def __init__(self, search_method):
        self.search_method = search_method

        pygame.init()
        pygame.font.init()
        pygame.mixer.init(frequency=44100, size=-16, channels=8, buffer=2048)

        # Usa as dimensões importadas de constants.py
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(f"Wumpus World AI - {search_method.upper()}")

        self.font_info = pygame.font.SysFont("arial", 16)
        self.font_percept = pygame.font.SysFont("arial", 12, bold=True)

        print("Carregando assets...")
        self.images = load_all_assets()

        # --- ÁUDIO ---
        self.sfx = {}
        try:
            self.sfx['gold'] = pygame.mixer.Sound(ASSET_PATHS["SND_GOLD"])
            self.sfx['breeze'] = pygame.mixer.Sound(ASSET_PATHS["SND_BREEZE"])
            self.sfx['stench'] = pygame.mixer.Sound(ASSET_PATHS["SND_STENCH"])
            self.sfx['breeze'].set_volume(0.5)
            self.sfx['stench'].set_volume(0.5)
        except Exception as e:
            print(f"Erro ao carregar sons: {e}")

        self.is_playing_breeze = False
        self.is_playing_stench = False
        self.gold_sound_played = False
        self.victory_music_started = False

        # Inicializa Ambiente e Agente
        self.world = WumpusEnvironment()
        self.agent = Agent(self.world)

        self.agent_direction = "UP"

        # Controle de Tempo
        self.last_move_time = pygame.time.get_ticks()
        self.move_delay = MOVE_DELAY  # Usa o valor centralizado (1000ms)

        self.start_time = time.time()
        self.end_time = None

    def process_audio(self):
        """Gerencia os sons baseado nas percepções."""
        if self.agent.game_over:
            if self.is_playing_breeze: self.sfx['breeze'].stop()
            if self.is_playing_stench: self.sfx['stench'].stop()
            return

        percepts = self.world.get_percepts(self.agent.pos)

        # Brisa
        if "Brisa" in percepts:
            if not self.is_playing_breeze:
                self.sfx['breeze'].play(loops=-1)
                self.is_playing_breeze = True
        else:
            if self.is_playing_breeze:
                self.sfx['breeze'].stop()
                self.is_playing_breeze = False

        # Fedor
        if "Fedor" in percepts:
            if not self.is_playing_stench:
                self.sfx['stench'].play(loops=-1)
                self.is_playing_stench = True
        else:
            if self.is_playing_stench:
                self.sfx['stench'].stop()
                self.is_playing_stench = False

        # Ouro
        if self.agent.has_gold and not self.gold_sound_played:
            self.sfx['gold'].play()
            self.gold_sound_played = True

    def draw_cell(self, r, c):
        x = c * CELL_SIZE
        y = r * CELL_SIZE
        rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

        # Chão
        self.screen.blit(self.images["GROUND"], (x, y))

        is_visited = (r, c) in self.agent.visited
        element = self.world.grid[r][c]

        # Elementos (Poço, Ouro, Wumpus)
        if element == 'P':
            self.screen.blit(self.images["PIT"], (x, y))
        elif element == 'G' and not self.agent.has_gold:
            self.screen.blit(self.images["GOLD"], (x, y))
        elif element == 'W':
            self.screen.blit(self.images["WUMPUS"], (x, y))

        # Nevoa (Fog of War)
        if not is_visited:
            if "UNEXPLORED" in self.images:
                self.screen.blit(self.images["UNEXPLORED"], (x, y))
            else:
                s = pygame.Surface((CELL_SIZE, CELL_SIZE))
                s.set_alpha(150)
                s.fill((0, 0, 0))
                self.screen.blit(s, (x, y))

        # Agente
        if (r, c) == self.agent.pos:
            key = f"AGENT_{self.agent_direction}"
            if key in self.images:
                self.screen.blit(self.images[key], (x, y))
            else:
                self.screen.blit(self.images["AGENT"], (x, y))

        # Percepções (Texto)
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

        # Borda da célula
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

            self.process_audio()

            # Lógica da IA (Temporizada)
            current_time = pygame.time.get_ticks()
            if not self.agent.game_over:
                if current_time - self.last_move_time > self.move_delay:
                    self.agent.think(self.search_method)
                    move_action = self.agent.move()
                    if move_action != (0, 0):
                        self.update_direction(move_action)
                    self.last_move_time = current_time
            else:
                # Fim de Jogo
                if self.agent.won and not self.victory_music_started:
                    pygame.mixer.music.stop()
                    try:
                        victory_path = ASSET_PATHS["SND_VICTORY"]
                        pygame.mixer.music.load(victory_path)
                        pygame.mixer.music.play(-1)
                    except Exception as e:
                        print(f"Erro ao tocar vitória: {e}")
                    self.victory_music_started = True

                pygame.time.delay(1000)

                if self.end_time is None:
                    self.end_time = time.time()

                duration = self.end_time - self.start_time

                metrics = {
                    "resultado": "VITÓRIA" if self.agent.won else "DERROTA",
                    "metodo": self.search_method.upper(),
                    "nos": self.agent.total_nodes,
                    "custo": self.agent.total_steps,
                    "tempo": f"{duration:.2f}s"
                }

                screen_over = GameOverScreen(metrics)
                screen_over.run()
                return

            self.screen.fill(BG_COLOR)
            for r in range(ROWS):
                for c in range(COLS):
                    self.draw_cell(r, c)
            self.draw_hud()

            pygame.display.flip()
            clock.tick(30)

        pygame.quit()
        sys.exit()