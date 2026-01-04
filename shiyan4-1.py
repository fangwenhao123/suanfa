def shortest_path_branch_and_bound(graph, source):
    # graph以邻接表表示: {节点: {邻居: 边长, ...}, ...}
    import heapq
    # 初始化距离字典，所有距离设为正无穷，源点距离设为0
    dist = {node: float('inf') for node in graph}
    dist[source] = 0
    # 小根堆（优先队列），存储元组(当前路径长度, 节点)
    pq = [(0, source)]
    while pq:
        d, u = heapq.heappop(pq)      # 取出路径长度最小的活结点
        if d > dist[u]:
            continue  # 如果当前堆中记录的距离大于已知最短距离，则跳过（已被更新剪枝）
        # 扩展结点u的所有邻居v
        for v, w in graph[u].items():
            new_dist = d + w  # 经由u到达v的路径长度
            if new_dist < dist[v]:
                # 找到更短路径，更新v的最短距离并将v作为新的活结点压入堆
                dist[v] = new_dist
                heapq.heappush(pq, (new_dist, v))
    return dist

# 测试
# 定义图的邻接表，例如:
# graph = {
#     0: {1: 10, 2: 3},
#     1: {2: 1, 3: 2},
#     2: {1: 4, 3: 8, 4: 2},
#     3: {4: 7},
#     4: {3: 9}
# }
graph = {
    0: {1: 2, 2: 5},
    1: {2: 1},
    2: {3: 2},
    3: {}
}
source = 0
distances = shortest_path_branch_and_bound(graph, source)
print(distances)