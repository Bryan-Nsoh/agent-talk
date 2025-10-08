"""Dinic max-flow implementation tailored for vertex cuts."""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Callable, List, Optional


INF = 10**9


@dataclass(slots=True)
class Edge:
    to: int
    rev: int
    cap: int


class Dinic:
    """Lightweight Dinic max-flow."""

    def __init__(self, n: int) -> None:
        self.n = n
        self.graph: List[List[Edge]] = [[] for _ in range(n)]

    def add_edge(self, u: int, v: int, cap: int) -> None:
        forward = Edge(to=v, rev=len(self.graph[v]), cap=cap)
        backward = Edge(to=u, rev=len(self.graph[u]), cap=0)
        self.graph[u].append(forward)
        self.graph[v].append(backward)

    def max_flow(self, source: int, sink: int) -> int:
        flow = 0
        level = [-1] * self.n
        while self._bfs(source, sink, level):
            it = [0] * self.n
            while True:
                pushed = self._dfs(source, sink, INF, level, it)
                if pushed == 0:
                    break
                flow += pushed
        return flow

    def min_cut_reachable(self, source: int) -> List[bool]:
        """Return nodes reachable in the residual graph from source."""
        visited = [False] * self.n
        q: deque[int] = deque([source])
        visited[source] = True
        while q:
            u = q.popleft()
            for edge in self.graph[u]:
                if edge.cap > 0 and not visited[edge.to]:
                    visited[edge.to] = True
                    q.append(edge.to)
        return visited

    def _bfs(self, source: int, sink: int, level: List[int]) -> bool:
        for i in range(self.n):
            level[i] = -1
        q: deque[int] = deque([source])
        level[source] = 0
        while q:
            u = q.popleft()
            for edge in self.graph[u]:
                if edge.cap > 0 and level[edge.to] < 0:
                    level[edge.to] = level[u] + 1
                    q.append(edge.to)
        return level[sink] >= 0

    def _dfs(self, u: int, sink: int, f: int, level: List[int], it: List[int]) -> int:
        if u == sink:
            return f
        for i in range(it[u], len(self.graph[u])):
            it[u] = i
            edge = self.graph[u][i]
            if edge.cap <= 0 or level[u] >= level[edge.to]:
                continue
            d = self._dfs(edge.to, sink, min(f, edge.cap), level, it)
            if d > 0:
                edge.cap -= d
                rev_edge = self.graph[edge.to][edge.rev]
                rev_edge.cap += d
                return d
        return 0
