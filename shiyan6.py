from collections import deque, defaultdict

class Graph:
    def __init__(self, n):
        self.n = n  # 节点数
        self.adj = [[] for _ in range(n)]          # 邻接表
        self.capacity = [[0]*n for _ in range(n)]  # 容量矩阵
    def add_edge(self, u, v, cap):
        # 添加 u->v 的边，容量累加（处理多重边）
        self.adj[u].append(v)
        self.adj[v].append(u)   # 添加反向边到邻接表，以便于残量更新
        self.capacity[u][v] += cap
    def bfs(self, s, t, parent):
        """
        在残量网络中用 BFS 寻找 s 到 t 的路径，返回是否找到增广路径，
        并通过 parent 数组记录路径结构。
        """
        visited = [False] * self.n
        queue = deque([s])
        visited[s] = True
        parent[s] = -1
        while queue:
            u = queue.popleft()
            for v in self.adj[u]:
                # 如果未访问且剩余容量 > 0 则可以前进
                if not visited[v] and self.capacity[u][v] > 0:
                    visited[v] = True
                    parent[v] = u
                    queue.append(v)
                    if v == t:  # 找到终点立即返回
                        return True
        return False
    def ford_fulkerson(self, source, sink):
        """
        Ford-Fulkerson 主过程（Edmonds-Karp 实现）：
        反复寻找增广路径并更新流，直到无增广路径为止。
        返回计算得到的最大流值。
        """
        parent = [-1] * self.n
        max_flow = 0
        # BFS 查找增广路径
        while self.bfs(source, sink, parent):
            # 找到路径后，找该路径上的最小容量（瓶颈容量）
            path_flow = float('Inf')
            v = sink
            while v != source:
                u = parent[v]
                path_flow = min(path_flow, self.capacity[u][v])
                v = u
            # 更新残量网络：正向边减去流量，反向边增加流量
            v = sink
            while v != source:
                u = parent[v]
                # 减去正向边容量
                self.capacity[u][v] -= path_flow
                # 增加反向边容量（即反向流量）
                self.capacity[v][u] += path_flow
                v = u
            max_flow += path_flow
        return max_flow

# 示例：构建图并计算最大流
if __name__ == "__main__":
    g = Graph(4)  # 6个节点：0~5
    # 添加边：格式 (u, v, 容量)
    # edges = [
    #     (0, 1, 16), (0, 2, 13),
    #     (1, 3, 12), (2, 1, 4),  (2, 4, 14),
    #     (3, 2, 9),  (3, 5, 20), (4, 3, 7), (4, 5, 4)
    # ]
    edges = [
        (0, 1, 10), (0, 2, 5),
        (1, 2, 15), (1, 3, 10),  (2, 3, 10),
    ]
    for u, v, cap in edges:
        g.add_edge(u, v, cap)
    source, sink = 0, 3
    maxflow = g.ford_fulkerson(source, sink)
    print(f"最大流值 = {maxflow}")
