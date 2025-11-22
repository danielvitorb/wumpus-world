# agent/search.py
from collections import deque
import heapq


def reconstruct_path(came_from, start, goal):
    """Reconstrói o caminho a partir do dicionário came_from."""
    path = []
    current = goal
    while current != start:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path


# ------------------------------------------------------------
#                   B R E A D T H   F I R S T   S E A R C H
# ------------------------------------------------------------
def bfs(start, goal, grid):
    """
    BFS padrão em grid.
    start: (r, c)
    goal: (r, c)
    grid: matriz contendo strings ou None
    """
    rows, cols = len(grid), len(grid[0])

    def is_valid(pos):
        r, c = pos
        if not (0 <= r < rows and 0 <= c < cols):
            return False
        if grid[r][c] in ("pit", "wumpus"):
            return False
        return True

    queue = deque([start])
    visited = {start}
    came_from = {}

    while queue:
        current = queue.popleft()

        if current == goal:
            return reconstruct_path(came_from, start, goal)

        r, c = current
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nxt = (r + dr, c + dc)
            if nxt not in visited and is_valid(nxt):
                visited.add(nxt)
                came_from[nxt] = current
                queue.append(nxt)

    return None  # sem solução


# ------------------------------------------------------------
#                   D E P T H   F I R S T   S E A R C H
# ------------------------------------------------------------
def dfs(start, goal, grid):
    """
    DFS recursivo.
    """
    rows, cols = len(grid), len(grid[0])

    def is_valid(pos):
        r, c = pos
        if not (0 <= r < rows and 0 <= c < cols):
            return False
        if grid[r][c] in ("pit", "wumpus"):
            return False
        return True

    stack = [start]
    visited = {start}
    came_from = {}

    while stack:
        current = stack.pop()

        if current == goal:
            return reconstruct_path(came_from, start, goal)

        r, c = current
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nxt = (r + dr, c + dc)
            if nxt not in visited and is_valid(nxt):
                visited.add(nxt)
                came_from[nxt] = current
                stack.append(nxt)

    return None


# ------------------------------------------------------------
#                   A   S T A R   S E A R C H
# ------------------------------------------------------------
def a_star(start, goal, grid):
    """A* com heurística Manhattan."""
    rows, cols = len(grid), len(grid[0])

    def is_valid(pos):
        r, c = pos
        if not (0 <= r < rows and 0 <= c < cols):
            return False
        if grid[r][c] in ("pit", "wumpus"):
            return False
        return True

    def heuristic(a, b):
        return abs(a[0]-b[0]) + abs(a[1]-b[1])

    pq = []
    heapq.heappush(pq, (0, start))
    came_from = {}
    g_score = {start: 0}
    visited = set()

    while pq:
        _, current = heapq.heappop(pq)

        if current == goal:
            return reconstruct_path(came_from, start, goal)

        if current in visited:
            continue
        visited.add(current)

        r, c = current
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nxt = (r + dr, c + dc)
            if not is_valid(nxt):
                continue

            tentative = g_score[current] + 1

            if nxt not in g_score or tentative < g_score[nxt]:
                came_from[nxt] = current
                g_score[nxt] = tentative
                f_score = tentative + heuristic(nxt, goal)
                heapq.heappush(pq, (f_score, nxt))

    return None
