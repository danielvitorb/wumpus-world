from src.utils.constants import ROWS, COLS


class WumpusEnvironment:
    def __init__(self, layout=None):
        """
        Inicializa o ambiente.
        :param layout: Uma matriz (lista de listas) representando o grid.
                       Strings aceitas: 'P' (Poço), 'W' (Wumpus), 'G' (Ouro), '.' (Vazio), 'A' (Agente)
        """
        self.grid = []
        # Agora usamos as constantes globais em vez de números fixos
        self.rows = ROWS
        self.cols = COLS

        self.agent_pos = (3, 0)  # Padrão: Canto inferior esquerdo
        self.gold_pos = None
        self.wumpus_pos = None
        self.pits = []

        self.game_over = False
        self.won = False
        self.message = ""

        # Se um layout for passado, carregamos ele. Senão, cria um padrão.
        if layout:
            self.load_custom_map(layout)
        else:
            self.load_default_map()

    def load_default_map(self):
        # Mapa padrão para testes
        # Nota: Se mudar ROWS/COLS em constants.py, precisará ajustar este mapa também!
        self.grid = [
            ['.', '.', '.', 'P'],
            ['W', 'G', 'P', '.'],
            ['.', '.', '.', '.'],
            ['.', '.', 'P', '.']
        ]
        self.scan_grid()

    def load_custom_map(self, layout):
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
                    self.grid[r][c] = '.'  # Limpa o agente do grid estático

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
        O ORÁCULO: Retorna o que o agente sente na posição atual.
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

        # 1. Verifica Paredes
        if not (0 <= nr < self.rows and 0 <= nc < self.cols):
            return self.agent_pos, ["Batida"], False

        # 2. Move o agente
        self.agent_pos = (nr, nc)
        current_cell = self.grid[nr][nc]

        percepts = self.get_percepts((nr, nc))

        # 3. Verifica interações
        if current_cell == 'W':
            self.message = "MORREU! Comido pelo Wumpus."
            self.game_over = True
        elif current_cell == 'P':
            self.message = "MORREU! Caiu no poço."
            self.game_over = True
        elif current_cell == 'G':
            self.message = "Achou o Ouro!"
            # Mantemos o ouro no grid lógico para o agente continuar sentindo "Brilho"
            # A interface é que vai esconder a imagem.

        return self.agent_pos, percepts, self.game_over