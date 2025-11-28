from collections import deque
import random
from agent.algorithms import SearchAlgorithms


class Agent:
    def __init__(self, world):
        self.world = world
        self.rows = world.rows
        self.cols = world.cols
        self.pos = (3, 0)

        # KB agora terá: 'UNKNOWN', 'SAFE', 'CAUTION', 'UNSAFE'
        self.kb = [['UNKNOWN' for _ in range(self.cols)] for _ in range(self.rows)]
        self.kb[self.pos[0]][self.pos[1]] = 'SAFE'

        self.visited = set()
        self.visited.add(self.pos)
        self.path_queue = []
        self.has_gold = False
        self.game_over = False
        self.message = "Explorando..."

    def get_valid_neighbors(self, pos):
        r, c = pos
        neighs = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                neighs.append((nr, nc))
        return neighs

    def infer_knowledge(self, percepts):
        """
        Atualiza o mapa mental.
        Mudança: Agora usamos 'CAUTION' em vez de bloquear tudo com 'UNSAFE'.
        """
        # Se não sinto nada, vizinhos são SAFE
        is_safe_zone = "Brisa" not in percepts and "Fedor" not in percepts

        neighbors = self.get_valid_neighbors(self.pos)

        for nr, nc in neighbors:
            current_status = self.kb[nr][nc]

            # Se já sei que é SAFE ou UNSAFE (certeza), não mudo
            if current_status in ['SAFE', 'UNSAFE']:
                continue

            if is_safe_zone:
                self.kb[nr][nc] = 'SAFE'
            else:
                # Se sinto cheiro/brisa, marco como CUIDADO (CAUTION)
                # Só marco como UNSAFE se tiver certeza absoluta (lógica avançada),
                # mas por enquanto, CAUTION permite que o agente arrisque se precisar.
                if current_status == 'UNKNOWN':
                    self.kb[nr][nc] = 'CAUTION'

    def find_best_target(self):
        """
        Estratégia de 2 Níveis:
        1. Tenta achar uma célula SAFE não visitada.
        2. Se não achar, tenta achar uma célula CAUTION não visitada (ARRISCAR!).
        """

        # 1. Busca por SAFE
        target = self.bfs_search_for_type('SAFE')
        if target:
            return target

        # 2. Busca por CAUTION (Modo Corajoso)
        self.message = "Sem caminhos seguros. Arriscando..."
        target = self.bfs_search_for_type('CAUTION')
        return target

    def bfs_search_for_type(self, target_type):
        """Busca a célula mais próxima de um tipo específico (SAFE ou CAUTION)."""
        queue = deque([self.pos])
        seen = {self.pos}

        while queue:
            curr = queue.popleft()

            # Se achei o tipo que queria e ainda não visitei
            if self.kb[curr[0]][curr[1]] == target_type and curr not in self.visited:
                return curr

            for n in self.get_valid_neighbors(curr):
                # O agente pode andar por SAFE e por CAUTION para chegar no destino.
                # Só não pode andar em UNSAFE (Paredes de medo).
                status = self.kb[n[0]][n[1]]
                if n not in seen and status != 'UNSAFE':
                    seen.add(n)
                    queue.append(n)
        return None

    def think(self, algorithm_name="A*"):
        if self.game_over: return

        # 1. Percepção
        percepts = self.world.get_percepts(self.pos)

        if "Brilho" in percepts:
            self.has_gold = True
            self.message = "OURO! Voltando..."
            self.path_queue = []

            # 2. Raciocínio
        self.infer_knowledge(percepts)

        # 3. Planejamento
        if not self.path_queue:
            target = None

            if self.has_gold:
                # Voltar para o início
                target = (3, 0)
                if self.pos == target:
                    self.message = "VITÓRIA! Ouro recuperado."
                    self.game_over = True
                    return
            else:
                # Explorar (Seguro ou Arriscado)
                target = self.find_best_target()

            if target:
                # Usa o algoritmo escolhido (BFS, DFS, A*) para gerar os passos
                if algorithm_name == "bfs":
                    path, nodes = SearchAlgorithms.bfs(self.pos, target, self.kb, self.rows, self.cols)
                elif algorithm_name == "dfs":
                    path, nodes = SearchAlgorithms.dfs(self.pos, target, self.kb, self.rows, self.cols)
                else:
                    path, nodes = SearchAlgorithms.a_star(self.pos, target, self.kb, self.rows, self.cols)

                if path:
                    self.path_queue = path
                    self.message = f"Indo para {target}. Nós: {nodes}"
                else:
                    self.message = "Travado: Sem caminho viável."
            else:
                self.message = "Mundo totalmente explorado (ou bloqueado)."
                # Opcional: Game Over se não tiver mais para onde ir
                # self.game_over = True

    def move(self):
        if self.path_queue and not self.game_over:
            next_pos = self.path_queue.pop(0)
            dr = next_pos[0] - self.pos[0]
            dc = next_pos[1] - self.pos[1]
            move_action = (dr, dc)

            new_pos, percepts, dead = self.world.step(move_action)
            self.pos = new_pos
            self.visited.add(self.pos)

            # Se a célula era CAUTION e eu não morri, agora ela é SAFE!
            if not dead:
                self.kb[self.pos[0]][self.pos[1]] = 'SAFE'

            if dead:
                self.game_over = True
                self.kb[self.pos[0]][self.pos[1]] = 'UNSAFE'  # Aprendi da pior forma
                if "Wumpus" in self.world.message:
                    self.message = "MORREU PARA O WUMPUS!"
                else:
                    self.message = "CAIU NO POÇO!"

            return move_action
        return (0, 0)
