# gui.py
import pygame
from game.world import World

class WorldGUI:
    def __init__(self, world: World, cell_size=64):
        pygame.init()

        self.world = world
        self.cell_size = cell_size

        # Dimensões da janela baseadas no mundo
        width = world.cols * cell_size
        height = world.rows * cell_size

        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Wumpus World - Visualização")

        self.clock = pygame.time.Clock()

    def run(self):
        running = True

        while running:
            # --- EVENTOS ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # --- DESENHO ---
            self.screen.fill((0, 0, 0))  # fundo preto

            self.world.draw(self.screen, self.cell_size)

            pygame.display.flip()
            self.clock.tick(30)  # 30 FPS

        pygame.quit()
