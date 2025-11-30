from collections import deque
from agent.algorithms import SearchAlgorithms


class Agent:
    def __init__(self, world):
        self.world = world
        self.rows = world.rows
        self.cols = world.cols
        self.pos = (3, 0)

        # KB: 'UNKNOWN', 'SAFE', 'CAUTION', 'UNSAFE'
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
        """Atualiza a base de conhecimento."""
        is_safe_zone = "Brisa" not in percepts and "Fedor" not in percepts

        neighbors = self.get_valid_neighbors(self.pos)
        for nr, nc in neighbors:
            current = self.kb[nr][nc]

            # O que é certo, não muda
            if current in ['SAFE', 'UNSAFE']:
                continue

            if is_safe_zone:
                self.kb[nr][nc] = 'SAFE'
            else:
                if current == 'UNKNOWN':
                    self.kb[nr][nc] = 'CAUTION'

    def find_target(self):
        """
        Define o objetivo.
        Retorna: (target_pos, must_be_safe)
        - must_be_safe=True: Só aceita caminho limpo.
        - must_be_safe=False: Aceita risco.
        """

        # 1. Se tem Ouro -> Voltar para o início (PRIORIDADE MÁXIMA)
        if self.has_gold:
            return (3, 0), True  # Tenta voltar só pelo seguro primeiro

        # 2. Se não tem Ouro -> Procurar célula SAFE não visitada
        target = self.bfs_find_nearest('SAFE')
        if target:
            return target, True  # Caminho seguro até a fronteira segura

        # 3. Se acabou o SAFE -> Arriscar em CAUTION
        target = self.bfs_find_nearest('CAUTION')
        if target:
            self.message = "Sem opções seguras. Arriscando..."
            return target, False  # Permite risco

        return None, True

    def bfs_find_nearest(self, type_target):
        """Busca BFS simples apenas para achar a coordenada do objetivo mais próximo."""
        queue = deque([self.pos])
        seen = {self.pos}
        while queue:
            curr = queue.popleft()
            if self.kb[curr[0]][curr[1]] == type_target and curr not in self.visited:
                return curr
            for n in self.get_valid_neighbors(curr):
                if n not in seen and self.kb[n[0]][n[1]] != 'UNSAFE':
                    seen.add(n)
                    queue.append(n)
        return None

    def think(self, algorithm_name="A*"):
        if self.game_over: return

        # 1. Perceber
        percepts = self.world.get_percepts(self.pos)
        if "Brilho" in percepts:
            self.has_gold = True
            self.message = "OURO! Voltando para casa..."
            self.path_queue = []

            # 2. Raciocinar
        self.infer_knowledge(percepts)

        # 3. Reação a Perigo (Interrupção de Caminho)
        # Se eu estava seguindo um plano e senti perigo, paro para reavaliar.
        if (("Brisa" in percepts or "Fedor" in percepts) and self.path_queue):
            # Mas só paro se o próximo passo for desconhecido/perigoso.
            # Se o próximo passo é SAFE (ex: voltando pra trás), continuo.
            next_step = self.path_queue[0]
            if self.kb[next_step[0]][next_step[1]] != 'SAFE':
                self.path_queue = []
                self.message = "Perigo detectado! Reavaliando..."

        # 4. Planejar (Se precisar)
        if not self.path_queue:
            target, safe_only = self.find_target()

            # Se tenho ouro e não achei caminho seguro, tento caminho arriscado
            if self.has_gold and not target:
                target = (3, 0)
                safe_only = False

            if target:
                # Chama o algoritmo genérico
                args = (self.pos, target, self.kb, self.rows, self.cols, safe_only)

                if algorithm_name == "bfs":
                    path, nodes = SearchAlgorithms.bfs(*args)
                elif algorithm_name == "dfs":
                    path, nodes = SearchAlgorithms.dfs(*args)
                else:
                    path, nodes = SearchAlgorithms.a_star(*args)

                # Se falhou em achar caminho seguro, e é permitido arriscar, tenta de novo sem filtro
                if not path and safe_only:
                    self.message = "Caminho seguro bloqueado. Tentando risco..."
                    # Tenta de novo com safe_only=False
                    args = (self.pos, target, self.kb, self.rows, self.cols, False)
                    if algorithm_name == "bfs":
                        path, nodes = SearchAlgorithms.bfs(*args)
                    elif algorithm_name == "dfs":
                        path, nodes = SearchAlgorithms.dfs(*args)
                    else:
                        path, nodes = SearchAlgorithms.a_star(*args)

                if path:
                    self.path_queue = path
                    modo = "SEGURO" if safe_only else "ARRISCADO"
                    self.message = f"Indo p/ {target} ({modo}). Nós: {nodes}"
                else:
                    self.message = "TRAVADO! Sem caminho possível."
            else:
                if self.has_gold and self.pos == (3, 0):
                    self.message = "VITÓRIA! Ouro entregue."
                    self.game_over = True
                else:
                    self.message = "Exploração Finalizada."

    def move(self):
        if self.path_queue and not self.game_over:
            next_pos = self.path_queue.pop(0)
            dr = next_pos[0] - self.pos[0]
            dc = next_pos[1] - self.pos[1]
            move_action = (dr, dc)

            new_pos, percepts, dead = self.world.step(move_action)

            self.pos = new_pos
            self.visited.add(self.pos)

            if not dead:
                self.kb[self.pos[0]][self.pos[1]] = 'SAFE'
            else:
                self.game_over = True
                self.kb[self.pos[0]][self.pos[1]] = 'UNSAFE'
                self.message = "MORREU NO CAMINHO!"

            return move_action
        return (0, 0)
