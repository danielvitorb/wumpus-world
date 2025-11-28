import pygame

class Cell:
    def __init__(self):
        # Conteúdo da célula
        self.gold = False
        self.wumpus = False
        self.pit = False
        self.agent = False

        # Percepções que serão calculadas pelo World
        # Exemplos: ["Fedor", "Brisa", "Brilho"]
        self.perceptions = []

        # Controle visual (para revelar o mapa aos poucos)
        self.is_revealed = False

    def draw(self, screen, images, font, x, y, cell_size):
        """
        Desenha a célula na tela.

        screen: superfície onde desenhar
        images: dicionário de assets (ground, gold, wumpus, pit, agent, unexplored)
        font: fonte usada para percepções
        x, y: posição em pixels onde desenhar a célula
        cell_size: tamanho da célula em pixels
        """

        # Se não foi revelada ainda → desenhar como bloqueada/unexplorada
        if not self.is_revealed:
            unexplored = images.get("unexplored")
            if unexplored:
                unexplored = pygame.transform.smoothscale(unexplored, (cell_size, cell_size))
                screen.blit(unexplored, (x, y))
            else:
                # fallback caso não exista imagem
                pygame.draw.rect(screen, (0, 0, 0), (x, y, cell_size, cell_size))
            return

        # 1. Desenha o chão (ground)
        ground = images.get("ground")
        if ground:
            ground = pygame.transform.smoothscale(ground, (cell_size, cell_size))
            screen.blit(ground, (x, y))
        else:
            pygame.draw.rect(screen, (200, 200, 200), (x, y, cell_size, cell_size))

        # 2. Desenha o conteúdo (se existir)
        icon_size = cell_size - 20  # margem
        offset = 10  # centralizar

        if self.wumpus:
            img = images.get("wumpus")
            if img:
                img = pygame.transform.smoothscale(img, (icon_size, icon_size))
                screen.blit(img, (x + offset, y + offset))

        if self.pit:
            img = images.get("pit")
            if img:
                img = pygame.transform.smoothscale(img, (icon_size, icon_size))
                screen.blit(img, (x + offset, y + offset))

        if self.gold:
            img = images.get("gold")
            if img:
                img = pygame.transform.smoothscale(img, (icon_size, icon_size))
                screen.blit(img, (x + offset, y + offset))

        if self.agent:
            img = images.get("agent")
            if img:
                img = pygame.transform.smoothscale(img, (icon_size, icon_size))
                screen.blit(img, (x + offset, y + offset))

        # 3. Desenha percepções (Fedor, Brisa, Brilho)
        if self.perceptions:
            line_h = 16
            text_x = x + 4
            text_y = y + cell_size - (line_h * len(self.perceptions)) - 4

            for idx, p in enumerate(self.perceptions):
                txt = font.render(p, True, (0, 0, 0))
                screen.blit(txt, (text_x, text_y + idx * line_h))
