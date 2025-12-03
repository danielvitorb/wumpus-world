from src.utils.constants import ROWS, COLS


class WumpusEnvironment:
    def __init__(self, layout=None):
        """
        Inicializa o ambiente.
        """
        self.grid = []
        self.rows = ROWS
        self.cols = COLS

        self.agent_pos = (3, 0)
        self.gold_pos = None
        self.wumpus_pos = None
        self.pits = []

        self.game_over = False
        self.won = False
        self.message = ""

        if layout:
            self.load_custom_map(layout)
        else:
            self.load_default_map()

    def load_default_map(self):
        # Mapa padrão
        self.grid = [
            ['.', '.', '.', 'P'],
            ['W', 'G', 'P', '.'],
            ['.', '.', '.', '.'],
            ['.', '.', 'P', '.']
        ]
        self.scan_grid()

    def load_custom_map(self, layout):
        # Mapa customizado, para implementações futuras
        self.grid = layout
        self.rows = len(layout)
        self.cols = len(layout[0])
        self.scan_grid()

    def scan_grid(self):
        """Varre o grid para guardar as coordenadas de tudo."""
        self.pits = []
        for r in range(self.rows):
            for c in range(self.cols):
                item = self.grid[r][c]
                if item == 'W':
                    self.wumpus_pos = (r, c)
                elif item == 'G':
                    self.gold_pos = (r, c)
                elif item == 'P':
                    self.pits.append((r, c))
                elif item == 'A':
                    self.agent_pos = (r, c)
                    self.grid[r][c] = '.'

    def reset(self):
        self.game_over = False
        self.won = False
        self.message = "Jogo Iniciado"
        return self.agent_pos

    def get_adjacents(self, r, c):
        """Retorna lista de coordenadas vizinhas válidas (Cima, Baixo, Esq, Dir)."""
        adj = []
        if r > 0: adj.append((r - 1, c))
        if r < self.rows - 1: adj.append((r + 1, c))
        if c > 0: adj.append((r, c - 1))
        if c < self.cols - 1: adj.append((r, c + 1))
        return adj

    def get_percepts(self, pos):
        """
        Retorna o que o agente sente na posição atual.
        """
        r, c = pos
        percepts = set()

        # 1. Verifica Ouro
        if self.grid[r][c] == 'G':
            percepts.add("Brilho")

        # 2. Verifica vizinhos (Brisa, Fedor)
        adjacentes = self.get_adjacents(r, c)
        for (nr, nc) in adjacentes:
            vizinho = self.grid[nr][nc]
            if vizinho == 'P':
                percepts.add("Brisa")
            elif vizinho == 'W':
                percepts.add("Fedor")

        return sorted(list(percepts))

    def step(self, action):
        """
        Executa um movimento e retorna (nova_pos, percepts, game_over).
        """
        if self.game_over:
            return self.agent_pos, [], True

        dr, dc = action
        nr, nc = self.agent_pos[0] + dr, self.agent_pos[1] + dc

        if not (0 <= nr < self.rows and 0 <= nc < self.cols):
            return self.agent_pos, ["Batida"], False

        self.agent_pos = (nr, nc)
        current_cell = self.grid[nr][nc]

        percepts = self.get_percepts((nr, nc))

        if current_cell == 'W':
            self.message = "MORREU! Comido pelo Wumpus."
            self.game_over = True
        elif current_cell == 'P':
            self.message = "MORREU! Caiu no poço."
            self.game_over = True
        elif current_cell == 'G':
            self.message = "Achou o Ouro!"

        return self.agent_pos, percepts, self.game_over