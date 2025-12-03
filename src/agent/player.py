from collections import deque
from src.agent.algorithms import SearchAlgorithms

class Agent:
    """
    Agente Inteligente.
    Gerencia a Base de Conhecimento (KB), inferência lógica e tomada de decisão.
    """

    def __init__(self, world):
        """
        Inicializa o agente conectado a um ambiente.
        """
        self.world = world
        self.rows = world.rows
        self.cols = world.cols
        self.pos = (3, 0)

        self.kb = [['UNKNOWN' for _ in range(self.cols)] for _ in range(self.rows)]
        self.kb[self.pos[0]][self.pos[1]] = 'SAFE'

        self.visited = set()
        self.visited.add(self.pos)
        self.path_queue = []
        self.has_gold = False
        self.game_over = False
        self.won = False
        self.message = "Explorando..."

        self.total_nodes = 0
        self.total_steps = 0

    def get_valid_neighbors(self, pos):
        """Retorna coordenadas vizinhas dentro dos limites do grid."""
        r, c = pos
        neighs = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                neighs.append((nr, nc))
        return neighs

    def infer_knowledge(self, percepts):
        """
        Atualiza a Base de Conhecimento (KB) baseado nas percepções atuais.
        Regra: Se não há Brisa nem Fedor, vizinhos são SAFE.
        Caso contrário, vizinhos desconhecidos tornam-se CAUTION.
        """
        is_safe_zone = "Brisa" not in percepts and "Fedor" not in percepts
        neighbors = self.get_valid_neighbors(self.pos)

        for nr, nc in neighbors:
            current = self.kb[nr][nc]

            if current in ['SAFE', 'UNSAFE']:
                continue

            if is_safe_zone:
                self.kb[nr][nc] = 'SAFE'
            else:
                if current == 'UNKNOWN':
                    self.kb[nr][nc] = 'CAUTION'

    def find_target(self):
        """
        Define o próximo objetivo estratégico.
        """
        if self.has_gold:
            return (3, 0), True

        target = self.bfs_find_nearest('SAFE')
        if target:
            return target, True

        target = self.bfs_find_nearest('CAUTION')
        if target:
            self.message = "Arriscando..."
            return target, False

        return None, True

    def bfs_find_nearest(self, type_target):
        """
        Busca em Largura (BFS) interna para encontrar a célula mais próxima
        de um determinado tipo (SAFE ou CAUTION) na KB.
        """
        queue = deque([self.pos])
        seen = {self.pos}
        while queue:
            curr = queue.popleft()
            # Se achou o tipo desejado e ainda não visitou
            if self.kb[curr[0]][curr[1]] == type_target and curr not in self.visited:
                return curr

            for n in self.get_valid_neighbors(curr):
                # O agente mentalmente só atravessa o que não é UNSAFE
                if n not in seen and self.kb[n[0]][n[1]] != 'UNSAFE':
                    seen.add(n)
                    queue.append(n)
        return None

    def think(self, algorithm_name="A*"):
        """
        Ciclo de decisão do agente (Perceber -> Raciocinar -> Planejar).
        """
        if self.game_over: return

        if self.has_gold and self.pos == (3, 0):
            self.message = "VITÓRIA! Ouro entregue em segurança."
            self.game_over = True
            self.won = True
            return

        percepts = self.world.get_percepts(self.pos)
        if "Brilho" in percepts:
            self.has_gold = True
            self.message = "OURO! Voltando..."
            self.path_queue = []

        self.infer_knowledge(percepts)

        if (("Brisa" in percepts or "Fedor" in percepts) and self.path_queue):
            next_step = self.path_queue[0]
            if self.kb[next_step[0]][next_step[1]] != 'SAFE':
                self.path_queue = []
                self.message = "Perigo! Recalculando..."

        if not self.path_queue:
            target, safe_only = self.find_target()

            if self.has_gold and not target:
                target = (3, 0)
                safe_only = False

            if target == self.pos:
                return

            if target:
                args = (self.pos, target, self.kb, self.rows, self.cols, safe_only)

                if algorithm_name == "bfs":
                    path, nodes = SearchAlgorithms.bfs(*args)
                elif algorithm_name == "dfs":
                    path, nodes = SearchAlgorithms.dfs(*args)
                else:
                    path, nodes = SearchAlgorithms.a_star(*args)

                if not path and safe_only:
                    self.message = "Sem rota segura. Tentando risco..."
                    args = (self.pos, target, self.kb, self.rows, self.cols, False)
                    if algorithm_name == "bfs": path, nodes = SearchAlgorithms.bfs(*args)
                    elif algorithm_name == "dfs": path, nodes = SearchAlgorithms.dfs(*args)
                    else: path, nodes = SearchAlgorithms.a_star(*args)

                self.total_nodes += nodes

                if path:
                    self.path_queue = path
                    modo = "SEGURO" if safe_only else "ARRISCADO"
                    self.message = f"Indo p/ {target} ({modo}). Nós: {nodes}"
                else:
                    self.message = "TRAVADO! Sem caminho."
            else:
                self.message = "Exploração Finalizada."

    def move(self):
        """Executa um passo físico no ambiente."""
        if self.path_queue and not self.game_over:
            next_pos = self.path_queue.pop(0)
            dr = next_pos[0] - self.pos[0]
            dc = next_pos[1] - self.pos[1]
            move_action = (dr, dc)

            new_pos, percepts, dead = self.world.step(move_action)

            self.pos = new_pos
            self.visited.add(self.pos)
            self.total_steps += 1

            if not dead:
                self.kb[self.pos[0]][self.pos[1]] = 'SAFE'
            else:
                self.game_over = True
                self.won = False
                self.kb[self.pos[0]][self.pos[1]] = 'UNSAFE'
                self.message = "MORREU NO CAMINHO!"

            return move_action
        return (0, 0)
