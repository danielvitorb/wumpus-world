# environment.py
# Environment for a grid-based game where an agent moves autonomously.
# The user will NOT use the keyboard; instead, an agent will choose actions.

class Environment:
    def __init__(self, grid, start_pos, goal_pos):
        self.grid = grid
        self.start_pos = start_pos
        self.goal_pos = goal_pos
        self.agent_pos = start_pos
        self.rows = len(grid)
        self.cols = len(grid[0])

    def reset(self):
        self.agent_pos = self.start_pos
        return self.agent_pos

    def is_valid(self, pos):
        r, c = pos
        if 0 <= r < self.rows and 0 <= c < self.cols:
            return self.grid[r][c] != 1  # 1 = wall
        return False

    def step(self, action):
        # Actions: 0=UP, 1=DOWN, 2=LEFT, 3=RIGHT
        r, c = self.agent_pos
        if action == 0:
            new_pos = (r - 1, c)
        elif action == 1:
            new_pos = (r + 1, c)
        elif action == 2:
            new_pos = (r, c - 1)
        elif action == 3:
            new_pos = (r, c + 1)
        else:
            new_pos = self.agent_pos

        if self.is_valid(new_pos):
            self.agent_pos = new_pos

        done = self.agent_pos == self.goal_pos
        return self.agent_pos, done

    def get_state(self):
        return self.agent_pos
