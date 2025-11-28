import heapq
from collections import deque


class SearchAlgorithms:
    """
    Contém as implementações puras de busca.
    Esses algoritmos operam sobre o 'mapa mental' do agente (Knowledge Base),
    não sobre o mapa real do jogo.
    """

    @staticmethod
    def reconstruct_path(came_from, start, goal):
        path = []
        current = goal
        while current != start:
            # Proteção contra caminhos quebrados
            if current not in came_from:
                return []
            path.append(current)
            current = came_from[current]
        path.reverse()
        return path

    @staticmethod
    def get_neighbors(pos, rows, cols):
        r, c = pos
        # Ordem de expansão: Cima, Baixo, Esq, Dir
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        result = []
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                result.append((nr, nc))
        return result

    # ------------------------------------------------------------
    #                   B F S (Busca em Largura)
    # ------------------------------------------------------------
    @staticmethod
    def bfs(start, goal, knowledge_base, rows, cols):
        """
        Retorna: (caminho, nós_expandidos)
        """
        queue = deque([start])
        visited = {start}
        came_from = {}
        nodes_expanded = 0

        while queue:
            current = queue.popleft()
            nodes_expanded += 1

            if current == goal:
                path = SearchAlgorithms.reconstruct_path(came_from, start, goal)
                return path, nodes_expanded

            for neighbor in SearchAlgorithms.get_neighbors(current, rows, cols):
                r, c = neighbor

                # A LÓGICA DE OURO: Só andamos se não soubermos que é perigoso.
                # Se for 'UNSAFE' (Perigo confirmado), evitamos.
                # Se for 'SAFE' ou 'UNKNOWN' (e não visitado), exploramos.
                cell_status = knowledge_base[r][c]

                if neighbor not in visited and cell_status != 'UNSAFE':
                    visited.add(neighbor)
                    came_from[neighbor] = current
                    queue.append(neighbor)

        return [], nodes_expanded

    # ------------------------------------------------------------
    #                   D F S (Busca em Profundidade)
    # ------------------------------------------------------------
    @staticmethod
    def dfs(start, goal, knowledge_base, rows, cols):
        stack = [start]
        visited = set()  # DFS precisa marcar visitado na entrada da pilha ou na saída
        came_from = {}
        nodes_expanded = 0

        # Nota: DFS em grafos precisa de cuidado com loops, por isso o visited
        visited.add(start)

        while stack:
            current = stack.pop()
            nodes_expanded += 1

            if current == goal:
                path = SearchAlgorithms.reconstruct_path(came_from, start, goal)
                return path, nodes_expanded

            # No DFS, invertemos a ordem dos vizinhos para manter consistência visual (opcional)
            neighbors = SearchAlgorithms.get_neighbors(current, rows, cols)

            for neighbor in neighbors:
                r, c = neighbor
                cell_status = knowledge_base[r][c]

                if neighbor not in visited and cell_status != 'UNSAFE':
                    visited.add(neighbor)
                    came_from[neighbor] = current
                    stack.append(neighbor)

        return [], nodes_expanded

    # ------------------------------------------------------------
    #                   A * (A-Star)
    # ------------------------------------------------------------
    @staticmethod
    def heuristic(a, b):
        # Distância Manhattan: |x1 - x2| + |y1 - y2|
        # Ideal para grids onde não se anda na diagonal
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    @staticmethod
    def a_star(start, goal, knowledge_base, rows, cols):
        """
        Usa uma fila de prioridade para expandir sempre o nó com menor f(n) = g(n) + h(n)
        """
        pq = []
        heapq.heappush(pq, (0, start))

        came_from = {}
        g_score = {start: 0}
        nodes_expanded = 0

        # Conjunto para busca rápida de quem já foi processado
        visited = set()

        while pq:
            _, current = heapq.heappop(pq)

            if current in visited:
                continue
            visited.add(current)
            nodes_expanded += 1

            if current == goal:
                path = SearchAlgorithms.reconstruct_path(came_from, start, goal)
                return path, nodes_expanded

            for neighbor in SearchAlgorithms.get_neighbors(current, rows, cols):
                r, c = neighbor
                cell_status = knowledge_base[r][c]

                if cell_status == 'UNSAFE':
                    continue

                tentative_g_score = g_score[current] + 1

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score = tentative_g_score + SearchAlgorithms.heuristic(neighbor, goal)
                    heapq.heappush(pq, (f_score, neighbor))

        return [], nodes_expanded