import heapq
import random
from collections import deque


class SearchAlgorithms:
    """
    Algoritmos de busca puros.
    Agora aceitam o parâmetro 'safe_only' para filtrar por onde podem passar.
    """

    @staticmethod
    def reconstruct_path(came_from, start, goal):
        path = []
        current = goal
        while current != start:
            if current not in came_from:
                return []
            path.append(current)
            current = came_from[current]
        path.reverse()
        return path

    @staticmethod
    def get_neighbors(pos, rows, cols):
        r, c = pos
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        random.shuffle(directions)  # Garante variedade em empates

        result = []
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                result.append((nr, nc))
        return result

    @staticmethod
    def is_walkable(pos, knowledge_base, safe_only):
        """Define se o algoritmo tem permissão para pisar nesta célula."""
        r, c = pos
        status = knowledge_base[r][c]

        # Paredes/Obstáculos conhecidos são sempre proibidos
        if status == 'UNSAFE':
            return False

        # Se safe_only=True, só pode andar no SAFE.
        # Se safe_only=False, pode andar no SAFE e no CAUTION (arriscar).
        if safe_only:
            return status == 'SAFE'
        else:
            return True  # Aceita SAFE, CAUTION e UNKNOWN

    # ------------------------------------------------------------
    #                   B F S
    # ------------------------------------------------------------
    @staticmethod
    def bfs(start, goal, kb, rows, cols, safe_only=False):
        queue = deque([start])
        visited = {start}
        came_from = {}
        nodes_expanded = 0

        while queue:
            current = queue.popleft()
            nodes_expanded += 1

            if current == goal:
                return SearchAlgorithms.reconstruct_path(came_from, start, goal), nodes_expanded

            for neighbor in SearchAlgorithms.get_neighbors(current, rows, cols):
                if neighbor not in visited:
                    if SearchAlgorithms.is_walkable(neighbor, kb, safe_only):
                        visited.add(neighbor)
                        came_from[neighbor] = current
                        queue.append(neighbor)
        return [], nodes_expanded

    # ------------------------------------------------------------
    #                   D F S
    # ------------------------------------------------------------
    @staticmethod
    def dfs(start, goal, kb, rows, cols, safe_only=False):
        stack = [start]
        visited = {start}
        came_from = {}
        nodes_expanded = 0

        while stack:
            current = stack.pop()
            nodes_expanded += 1

            if current == goal:
                return SearchAlgorithms.reconstruct_path(came_from, start, goal), nodes_expanded

            for neighbor in SearchAlgorithms.get_neighbors(current, rows, cols):
                if neighbor not in visited:
                    if SearchAlgorithms.is_walkable(neighbor, kb, safe_only):
                        visited.add(neighbor)
                        came_from[neighbor] = current
                        stack.append(neighbor)
        return [], nodes_expanded

    # ------------------------------------------------------------
    #                   A * (A-Star)
    # ------------------------------------------------------------
    @staticmethod
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    @staticmethod
    def a_star(start, goal, kb, rows, cols, safe_only=False):
        pq = []
        # Random no custo inicial para desempatar caminhos iguais
        heapq.heappush(pq, (0 + random.random(), start))

        came_from = {}
        g_score = {start: 0}
        nodes_expanded = 0
        visited = set()

        while pq:
            _, current = heapq.heappop(pq)

            if current in visited: continue
            visited.add(current)
            nodes_expanded += 1

            if current == goal:
                return SearchAlgorithms.reconstruct_path(came_from, start, goal), nodes_expanded

            for neighbor in SearchAlgorithms.get_neighbors(current, rows, cols):
                if not SearchAlgorithms.is_walkable(neighbor, kb, safe_only):
                    continue

                # Custo dinâmico:
                # Se safe_only=True, ele nem entra aqui se for CAUTION.
                # Se safe_only=False, cobramos caro pelo risco.
                status = kb[neighbor[0]][neighbor[1]]
                move_cost = 1
                if status == 'CAUTION':
                    move_cost = 20  # Penalidade alta para evitar risco desnecessário

                tentative_g = g_score[current] + move_cost

                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f = tentative_g + SearchAlgorithms.heuristic(neighbor, goal)
                    # Adiciona ruído para evitar vício de caminho
                    heapq.heappush(pq, (f + random.uniform(0, 0.5), neighbor))

        return [], nodes_expanded