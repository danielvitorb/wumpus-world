# src/gui/game_over.py

import pygame
import sys
from src.utils.constants import WHITE, BLACK, GREEN, RED, BLUE

# Dimensões específicas para a tela de relatório (para caber o texto confortavelmente)
WIDTH, HEIGHT = 500, 450


class GameOverScreen:
    """
    Tela de relatório final.
    Exibe o resultado (Vitória/Derrota) e as métricas coletadas pelo agente.
    """

    def __init__(self, metrics):
        """
        metrics: dicionário contendo:
        - 'resultado': 'VITÓRIA' ou 'DERROTA'
        - 'metodo': 'BFS', 'A*', etc.
        - 'nos': int
        - 'custo': int (passos)
        - 'tempo': string (ex: "12.5s")
        """
        self.metrics = metrics
        pygame.init()
        pygame.display.set_caption("Fim de Jogo")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        # Fontes
        self.title_font = pygame.font.SysFont("arial", 40, bold=True)
        self.text_font = pygame.font.SysFont("arial", 22)
        self.btn_font = pygame.font.SysFont("arial", 20, bold=True)

    def draw_text(self, text, font, color, y_pos):
        surf = font.render(text, True, color)
        rect = surf.get_rect(center=(WIDTH // 2, y_pos))
        self.screen.blit(surf, rect)

    def run(self):
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Se clicar em qualquer lugar ou apertar tecla, fecha o jogo
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    return

            self.screen.fill(WHITE)

            # 1. Título (Vitória ou Derrota)
            if self.metrics['resultado'] == "VITÓRIA":
                titulo = "MISSÃO CUMPRIDA!"
                cor_titulo = GREEN
            else:
                titulo = "FIM DE JOGO"
                cor_titulo = RED

            self.draw_text(titulo, self.title_font, cor_titulo, 50)

            # 2. Métricas
            infos = [
                f"Método Utilizado: {self.metrics['metodo']}",
                f"Nós Expandidos: {self.metrics['nos']}",
                f"Custo do Caminho (Passos): {self.metrics['custo']}",
                f"Tempo de Execução: {self.metrics['tempo']}"
            ]

            start_y = 120
            for i, info in enumerate(infos):
                bg_rect = pygame.Rect(50, start_y + (i * 40) - 10, 400, 35)
                pygame.draw.rect(self.screen, (240, 240, 240), bg_rect, border_radius=5)

                self.draw_text(info, self.text_font, BLACK, start_y + (i * 40))

            # 3. Instrução Final
            self.draw_text("Pressione qualquer tecla para sair...", self.btn_font, BLUE, 400)

            pygame.display.flip()
            clock.tick(30)