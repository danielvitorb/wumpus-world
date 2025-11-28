# agent.py
"""
Agent: componente que liga as buscas ao World e executa ações no ambiente.

Como usar (exemplo rápido):
    from world import World
    from searches.bfs import search as bfs_search
    from agent.agent import Agent

    w = World()
    ag = Agent(world=w, search_fn=bfs_search)

    # planeja usando as posições padrão (inicio do world -> ouro do world)
    ag.plan_path()

    # obter a sequência de ações (0=UP,1=DOWN,2=LEFT,3=RIGHT)
    actions = ag.actions_queue.copy()

    # executar passo a passo (ideal para animação)
    while ag.actions_queue and not ag.finished:
        status = ag.execute_next_action()
        # status é um dicionário com info sobre o movimento atual
"""

from typing import Callable, List, Tuple, Optional
import time

Position = Tuple[int, int]
Action = int  # 0=UP,1=DOWN,2=LEFT,3=RIGHT


class Agent:
    def __init__(self, world, search_fn: Callable):
        """
        world: instância de World (contendo grid, posições, move_agent(...))
        search_fn: função de busca importada da pasta searches, com assinatura:
                   search_fn(world, start_pos, goal_pos) -> List[Position]
                   (retorna caminho como lista de (r,c))
        """
        self.world = world
        self.search_fn = search_fn

        # caminho em termos de posições (lista de (r,c)); pode conter a posição inicial
        self.planned_path: List[Position] = []

        # fila de ações numéricas (0..3) derivada do planned_path
        self.actions_queue: List[Action] = []

        # flags de estado
        self.finished: bool = False  # true quando terminou (achou ouro ou morreu ou esgotou ações)
        self.last_status: Optional[dict] = None  # último retorno de execute_next_action

    # -----------------------------
    # UTILITÁRIOS
    # -----------------------------
    @staticmethod
    def _pos_to_action(from_pos: Position, to_pos: Position) -> Optional[Action]:
        """
        Converte dois positions adjacentes em uma action inteira:
        - (r-1,c) => UP (0)
        - (r+1,c) => DOWN (1)
        - (r,c-1) => LEFT (2)
        - (r,c+1) => RIGHT (3)

        Retorna None se posições não são adjacentes válidas.
        """
        fr, fc = from_pos
        tr, tc = to_pos
        dr = tr - fr
        dc = tc - fc

        if dr == -1 and dc == 0:
            return 0  # UP
        if dr == 1 and dc == 0:
            return 1  # DOWN
        if dr == 0 and dc == -1:
            return 2  # LEFT
        if dr == 0 and dc == 1:
            return 3  # RIGHT
        return None

    @staticmethod
    def _normalize_path(start: Position, path: List[Position]) -> List[Position]:
        """
        Garante que a lista de posições comece com 'start'.
        Alguns algoritmos retornam caminho incluindo start; outros não.
        Nós normalizamos para que path[0] == start.
        """
        if not path:
            return []
        if path[0] == start:
            return list(path)
        return [start] + list(path)

    # -----------------------------
    # PLANEJAMENTO
    # -----------------------------
    def plan_path(self, start: Optional[Position] = None, goal: Optional[Position] = None) -> List[Position]:
        """
        Executa a função de busca (search_fn) no world e popula:
        - self.planned_path (lista de posições)
        - self.actions_queue (lista de ações correspondentes)

        Se start/goal não forem informados, usa:
        - start = world.agent_pos
        - goal = world.gold_pos (ou o local identificado pelo world)

        Retorna a lista de posições planejadas.
        """
        if start is None:
            start = self.world.agent_pos

        if goal is None:
            # tentativa de detectar gold_pos a partir do World
            # aceitamos ambos world.gold_pos ou um método is_goal()
            goal = getattr(self.world, "gold_pos", None)
            if goal is None:
                # ver se world tem método is_goal e procurar
                # (procura a primeira célula com gold=True)
                for r in range(self.world.rows):
                    for c in range(self.world.cols):
                        if self.world.grid[r][c].gold:
                            goal = (r, c)
                            break
                    if goal is not None:
                        break

        if goal is None:
            raise ValueError("Goal (gold position) não encontrado no world e não foi passado.")

        # chama a função de busca: espera-se que retorne uma lista de posições
        raw_path = self.search_fn(self.world, start, goal)

        # normaliza para incluir start como primeiro elemento
        path = self._normalize_path(start, raw_path)

        # armazena caminho
        self.planned_path = path

        # converte em ações
        self.actions_queue = self._path_to_actions(path)

        # reset estado
        self.finished = False
        self.last_status = None

        return self.planned_path

    def _path_to_actions(self, path: List[Position]) -> List[Action]:
        """
        Converte um caminho de posições em uma lista de ações.
        Se o path tiver N posições, teremos N-1 ações (movimentos entre posições consecutivas).
        Posições não-adjacentes produzem uma exceção.
        """
        actions: List[Action] = []
        if not path or len(path) == 1:
            return actions

        for i in range(len(path) - 1):
            a = self._pos_to_action(path[i], path[i + 1])
            if a is None:
                raise ValueError(f"Posições não adjacentes encontradas no path: {path[i]} -> {path[i+1]}")
            actions.append(a)
        return actions

    # -----------------------------
    # EXECUÇÃO (um passo / todos)
    # -----------------------------
    def execute_next_action(self) -> dict:
        """
        Executa a próxima ação na fila (se existir), chamando world.move_agent(action).
        Retorna um dicionário com informações do resultado:
            {
                "action": int,
                "new_pos": (r,c),
                "status": "OK" | "GOLD_FOUND" | "DEAD_PIT" | "DEAD_WUMPUS" | ...,
                "died": bool
            }
        Atualiza self.last_status, e marca self.finished quando for o caso.
        """
        if self.finished:
            return {"action": None, "new_pos": self.world.agent_pos, "status": "FINISHED", "died": False}

        if not self.actions_queue:
            # sem ações → terminou (nenhum caminho ou já executado)
            self.finished = True
            return {"action": None, "new_pos": self.world.agent_pos, "status": "NO_ACTIONS", "died": False}

        action = self.actions_queue.pop(0)
        new_pos, status_str, died = self.world.move_agent(action)

        # monta info
        info = {
            "action": action,
            "new_pos": new_pos,
            "status": status_str,
            "died": died
        }
        self.last_status = info

        # se morreu ou achou ouro, finalize
        if died or status_str == "GOLD_FOUND":
            self.finished = True

        return info

    def execute_all(self, delay: float = 0.12):
        """
        Executa todas as ações da fila, esperando `delay` segundos entre as ações.
        Útil para rodar em modo não interativo (sem animação quadro-a-quadro).
        Atenção: esse método bloqueia a thread atual até terminar.
        """
        results = []
        while not self.finished and self.actions_queue:
            info = self.execute_next_action()
            results.append(info)
            # pequeno delay para visualizar (ou para evitar instantanéidade)
            time.sleep(delay)
        return results

    # -----------------------------
    # AUXILIARES / RESET
    # -----------------------------
    def reset_plan(self):
        """Limpa o plano e fila de ações (não altera posição do agente)."""
        self.planned_path = []
        self.actions_queue = []
        self.finished = False
        self.last_status = None

    def set_search_fn(self, search_fn: Callable):
        """Troca a função de busca em tempo de execução."""
        self.search_fn = search_fn

    # -----------------------------
    # DEBUG / REPRESENTAÇÃO
    # -----------------------------
    def __repr__(self):
        return f"<Agent pos={self.world.agent_pos} actions_left={len(self.actions_queue)} finished={self.finished}>"
