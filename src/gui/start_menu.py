import pygame
import sys
from src.utils.constants import WHITE, BLACK, GRAY

# Configurações específicas do Menu (não precisam estar no constants.py global)
WIDTH, HEIGHT = 500, 400
DARK_GRAY = (100, 100, 100)

class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = GRAY
        self.hover_color = DARK_GRAY
        self.text_color = BLACK

    def draw(self, screen, font):
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color

        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        label = font.render(self.text, True, self.text_color)
        screen.blit(label, (self.rect.x + (self.rect.width - label.get_width()) // 2,
                            self.rect.y + (self.rect.height - label.get_height()) // 2))

    def clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)


class StartMenu:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Escolha o método de busca")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.font = pygame.font.SysFont("arial", 26, bold=True)

        # Botões centralizados
        self.buttons = [
            Button(150, 120, 200, 50, "Busca BFS"),
            Button(150, 190, 200, 50, "Busca DFS"),
            Button(150, 260, 200, 50, "Busca A*"),
        ]

    def run(self):
        """Exibe o menu e retorna o método escolhido como 'bfs', 'dfs' ou 'astar'."""
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                for i, button in enumerate(self.buttons):
                    if button.clicked(event):
                        if i == 0:
                            return "bfs"
                        elif i == 1:
                            return "dfs"
                        elif i == 2:
                            return "astar"

            self.screen.fill(WHITE)

            title = self.font.render("Selecione o método de busca", True, BLACK)
            self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 40))

            for btn in self.buttons:
                btn.draw(self.screen, self.font)

            pygame.display.flip()
            clock.tick(30)