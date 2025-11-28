from game.cells import Cell

class World:
    """
    Classe responsável pelo mundo do Wumpus.
    Mantém o grid, calcula percepções e controla o movimento do agente.
    """

    def __init__(self, rows=4, cols=4):
        self.rows = rows
        self.cols = cols

        # Cria a grade de células
        self.grid = [[Cell() for _ in range(cols)] for _ in range(rows)]

        # Posição do agente
        self.agent_pos = (rows - 1, 0)  # default = canto inferior esquerdo
        self.grid[self.agent_pos[0]][self.agent_pos[1]].agent = True
        self.grid[self.agent_pos[0]][self.agent_pos[1]].is_revealed = True

        # Coordenadas fixas para default (pode ajustar depois)
        self.wumpus_pos = (1, 0)
        self.gold_pos = (1, 1)
        self.pits = [(0, 3), (1, 2), (3, 2)]

        # Coloca os elementos no grid
        self._place_elements()

        # Gera percepções nas células adjacentes
        self._generate_perceptions()

    # -----------------------------------------------------------------
    # CONFIGURAÇÃO DO MUNDO
    # -----------------------------------------------------------------

    def _place_elements(self):
        """Posiciona wumpus, ouro e poços na grid."""
        # wumpus
        wr, wc = self.wumpus_pos
        self.grid[wr][wc].wumpus = True

        # gold
        gr, gc = self.gold_pos
        self.grid[gr][gc].gold = True

        # pits
        for (pr, pc) in self.pits:
            self.grid[pr][pc].pit = True

    # -----------------------------------------------------------------

    def _adjacent_cells(self, r, c):
        """Retorna posições válidas adjacentes (4-direções)."""
        adj = []
        if r > 0: adj.append((r - 1, c))
        if r < self.rows - 1: adj.append((r + 1, c))
        if c > 0: adj.append((r, c - 1))
        if c < self.cols - 1: adj.append((r, c + 1))
        return adj

    # -----------------------------------------------------------------

    def _generate_perceptions(self):
        """Calcula percepções (Brisa, Fedor, Brilho)."""
        for r in range(self.rows):
            for c in range(self.cols):
                cell = self.grid[r][c]

                # se tem ouro → brilho apenas nela
                if cell.gold:
                    cell.perceptions.append("Brilho")

                # se é adjacente ao wumpus → fedor
                for (wr, wc) in [self.wumpus_pos]:
                    if (r, c) in self._adjacent_cells(wr, wc):
                        cell.perceptions.append("Fedor")

                # se é adjacente a poço → brisa
                for (pr, pc) in self.pits:
                    if (r, c) in self._adjacent_cells(pr, pc):
                        cell.perceptions.append("Brisa")

    # -----------------------------------------------------------------
    # MOVIMENTO DO AGENTE
    # -----------------------------------------------------------------

    def move_agent(self, action):
        """
        Move o agente.
        action: 0=UP, 1=DOWN, 2=LEFT, 3=RIGHT
        Retorna:
            (nova_posição, status, morreu_por_terreno)
        """
        r, c = self.agent_pos

        if action == 0:     new = (r - 1, c)
        elif action == 1:   new = (r + 1, c)
        elif action == 2:   new = (r, c - 1)
        elif action == 3:   new = (r, c + 1)
        else:
            return self.agent_pos, "INVALID_ACTION", False

        # movimento inválido
        nr, nc = new
        if nr < 0 or nr >= self.rows or nc < 0 or nc >= self.cols:
            return self.agent_pos, "WALL", False

        # remove agente da posição atual
        old_r, old_c = self.agent_pos
        self.grid[old_r][old_c].agent = False

        # coloca na nova
        self.agent_pos = (nr, nc)
        self.grid[nr][nc].agent = True
        self.grid[nr][nc].is_revealed = True  # revela automaticamente

        # checa perigos
        cell = self.grid[nr][nc]

        if cell.wumpus:
            return self.agent_pos, "DEAD_WUMPUS", True

        if cell.pit:
            return self.agent_pos, "DEAD_PIT", True

        if cell.gold:
            return self.agent_pos, "GOLD_FOUND", False

        return self.agent_pos, "OK", False

    # -----------------------------------------------------------------
    # UTILITÁRIOS PARA BUSCAS
    # -----------------------------------------------------------------

    def get_adjacent_positions(self, r, c):
        """Versão pública de adjacências, para busca."""
        return self._adjacent_cells(r, c)

    def is_safe(self, r, c):
        """Para busca não considerada percepções, apenas paredes/brancos."""
        if r < 0 or r >= self.rows or c < 0 or c >= self.cols:
            return False
        return True

    def is_goal(self, r, c):
        """Usado nas buscas — verifica se célula é ouro."""
        return self.grid[r][c].gold

