class WumpusEnvironment:
    def __init__(self, layout=None):
        """
        Inicializa o ambiente.
        :param layout: Uma matriz (lista de listas) representando o grid.
                       Strings aceitas: 'P' (Poço), 'W' (Wumpus), 'G' (Ouro), '.' (Vazio), 'A' (Agente)
        """
        self.grid = []
        self.rows = 4
        self.cols = 4
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
        # Mapa padrão para testes (igual ao que você tinha na interface)
        # '.' = Vazio, 'P' = Poço, 'W' = Wumpus, 'G' = Ouro
        self.grid = [
            ['.', '.', '.', 'P'],
            ['W', 'G', 'P', '.'],
            ['.', '.', '.', '.'],
            ['.', '.', 'P', '.']
        ]
        # Atualiza as listas de posições baseadas no grid acima
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
        # Cima
        if r > 0: adj.append((r - 1, c))
        # Baixo
        if r < self.rows - 1: adj.append((r + 1, c))
        # Esquerda
        if c > 0: adj.append((r, c - 1))
        # Direita
        if c < self.cols - 1: adj.append((r, c + 1))
        return adj

    def get_percepts(self, pos):
        """
        O ORÁCULO: Retorna o que o agente sente na posição atual.
        Essa é a função mais importante para a IA.
        """
        r, c = pos
        percepts = set()  # Usamos set para evitar duplicatas

        # 1. Verifica se está na posição do Ouro
        if self.grid[r][c] == 'G':
            percepts.add("Brilho")

        # 2. Verifica vizinhos para Brisa e Fedor
        adjacentes = self.get_adjacents(r, c)

        for (nr, nc) in adjacentes:
            vizinho = self.grid[nr][nc]
            if vizinho == 'P':
                percepts.add("Brisa")
            elif vizinho == 'W':
                percepts.add("Fedor")

        # Converte para lista e ordena para ficar bonito na interface
        return sorted(list(percepts))

    def step(self, action):
        """
        Executa um movimento.
        Action: Tupla (delta_row, delta_col) ex: (-1, 0) para subir.
        Retorna: (nova_pos, percepts, game_over)
        """
        if self.game_over:
            return self.agent_pos, [], True

        dr, dc = action
        nr, nc = self.agent_pos[0] + dr, self.agent_pos[1] + dc

        # 1. Verifica Paredes (Limites do Grid)
        if not (0 <= nr < self.rows and 0 <= nc < self.cols):
            return self.agent_pos, ["Batida"], False  # Bateu na parede

        # 2. Move o agente
        self.agent_pos = (nr, nc)
        current_cell = self.grid[nr][nc]
        percepts = self.get_percepts((nr, nc))

        # 3. Verifica Morte ou Vitória
        if current_cell == 'W':
            self.message = "MORREU! Comido pelo Wumpus."
            self.game_over = True
        elif current_cell == 'P':
            self.message = "MORREU! Caiu no poço."
            self.game_over = True
        elif current_cell == 'G':
            self.message = "Achou o Ouro!"
            # Nota: O jogo geralmente só acaba quando ele volta pro início,
            # mas podemos simplificar ou implementar isso no Agente.

        return self.agent_pos, percepts, self.game_over