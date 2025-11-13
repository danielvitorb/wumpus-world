class World:
    def __init__(self):
        self.rows = 4
        self.cols = 4
        self.map = [
            [None, None, None, "pit"],
            ["wumpus", "gold", "pit", None],
            [None, None, None, None],
            ["agent", None, "pit", None]
        ]
        self.agent_pos = (0, 3)
        self.visible = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        self.reveal_initial()

        # Gera as percepções
        self.perceptions = [[[] for _ in range(self.cols)] for _ in range(self.rows)]
        self.generate_perceptions()

    def reveal_initial(self):
        x, y = self.agent_pos
        self.visible[y][x] = True
        if x + 1 < self.cols:
            self.visible[y][x + 1] = True
        if y - 1 >= 0:
            self.visible[y - 1][x] = True

    def generate_perceptions(self):
        """Gera percepções de brisa, fedor e brilho com base no mapa."""
        for y in range(self.rows):
            for x in range(self.cols):
                element = self.map[y][x]
                if element == "pit":
                    self.add_adjacent_perception(x, y, "brisa")
                elif element == "wumpus":
                    self.add_adjacent_perception(x, y, "fedor")
                elif element == "gold":
                    self.perceptions[y][x].append("brilho")

    def add_adjacent_perception(self, x, y, perception):
        """Adiciona a percepção nas células vizinhas de (x, y)."""
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.cols and 0 <= ny < self.rows:
                if perception not in self.perceptions[ny][nx]:
                    self.perceptions[ny][nx].append(perception)
