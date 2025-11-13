class World:
    def __init__(self):
        self.rows = 4
        self.cols = 4

        # Mapa fixo
        self.map = [
            ["wumpus", None, None, "pit"],
            [None, "gold", "pit", None],
            [None, None, None, None],
            ["agent", None, "pit", None]
        ]

        # Posição inicial do agente
        self.agent_pos = (0, 3)

        # Células visíveis (inicialmente apenas o agente e vizinhos)
        self.visible = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        self.reveal_initial()

    def reveal_initial(self):
        x, y = self.agent_pos
        self.visible[y][x] = True

        # Vizinho à direita
        if x + 1 < self.cols:
            self.visible[y][x + 1] = True
        # Vizinho acima
        if y - 1 >= 0:
            self.visible[y - 1][x] = True
