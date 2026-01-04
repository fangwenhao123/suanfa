import networkx as nx
import math
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False  # 解决负号 '-' 显示为方块的问题

# 1. 定义 8 个二维坐标（也可以随机生成）
points = {
    0: (0, 0),
    1: (1, 5),
    2: (5, 2),
    3: (3, 1),
    4: (4, 4),
    5: (6, 0),
    6: (7, 3),
    7: (2, 6),
}

# 构造完全图，节点为 0..7，边权为欧几里得距离
G = nx.Graph()
for i, coord in points.items():
    G.add_node(i)  # 添加节点
for i in points:
    for j in points:
        if i < j:
            xi, yi = points[i]
            xj, yj = points[j]
            dist = math.hypot(xi - xj, yi - yj)  # 计算欧几里得距离
            G.add_edge(i, j, weight=dist)

# 计算最小生成树（MST）
mst = nx.minimum_spanning_tree(G)
mst_edges = list(mst.edges())
mst_weight = sum(mst[u][v]['weight'] for u, v in mst_edges)
print("MST 边集合:", mst_edges)
print("MST 总权重:", mst_weight)

# 找出 MST 中度为奇数的顶点
odd_nodes = [v for v, d in mst.degree() if d % 2 == 1]
print("MST 中奇数度顶点:", odd_nodes)

# 暴力枚举奇数顶点的完美匹配
def min_weight_matching_on_nodes(G, nodes):
    nodes = list(nodes)
    best_weight = float('inf')
    best_matching = None

    # 递归生成所有配对方案
    def generate_matchings(current):
        if not current:
            yield []
            return
        first = current[0]
        for i in range(1, len(current)):
            second = current[i]
            rest = current[1:i] + current[i+1:]
            for matching in generate_matchings(rest):
                yield [(first, second)] + matching

    for matching in generate_matchings(nodes):
        w = sum(G[u][v]['weight'] for u, v in matching)
        if w < best_weight:
            best_weight = w
            best_matching = matching
    return best_matching

matching = min_weight_matching_on_nodes(G, odd_nodes)
print("匹配边:", matching)
print("匹配总权重:", sum(G[u][v]['weight'] for u, v in matching))

# 构造包含 MST 边和匹配边的多重图
multi = nx.MultiGraph()
multi.add_nodes_from(G.nodes())
for u, v, data in mst.edges(data=True):
    multi.add_edge(u, v, weight=data['weight'])
for u, v in matching:
    multi.add_edge(u, v, weight=G[u][v]['weight'])

# 检查是否欧拉图
print("是否为欧拉图:", nx.is_eulerian(multi))

# 查找欧拉回路（可选指定起点）
start = odd_nodes[0] if odd_nodes else 0
euler_edges = list(nx.eulerian_circuit(multi, source=start))
print("欧拉回路边序列:", euler_edges)

# 提取欧拉回路的顶点序列
euler_path = []
for i, (u, v) in enumerate(euler_edges):
    if i == 0:
        euler_path.append(u)
    euler_path.append(v)
print("欧拉回路顶点序列:", euler_path)

# 从欧拉回路中提取哈密尔顿回路（去除重复顶点）
visited = set()
hamilton_path = []
for node in euler_path:
    if node not in visited:
        visited.add(node)
        hamilton_path.append(node)
# 回到起点
hamilton_path.append(hamilton_path[0])
print("哈密尔顿回路（TSP路径）:", hamilton_path)

# 计算最终路径总长度
total_dist = 0
for i in range(len(hamilton_path) - 1):
    u, v = hamilton_path[i], hamilton_path[i+1]
    total_dist += G[u][v]['weight']
print("TSP路径总长度:", total_dist)

pos = points  # 节点位置用坐标 dict

# （1）绘制 MST：绿色实线表示
plt.figure(figsize=(6,6))
nx.draw_networkx_nodes(G, pos, node_size=300)
nx.draw_networkx_labels(G, pos)
nx.draw_networkx_edges(G, pos, edgelist=list(mst.edges()), edge_color='green', width=2)
mst_labels = {(u, v): f"{mst[u][v]['weight']:.2f}" for u, v in mst.edges()}
nx.draw_networkx_edge_labels(G, pos, edge_labels=mst_labels, font_color='green')
plt.title("MST (绿色为最小生成树边)")

# （2）绘制 MST + 匹配边：匹配边红色虚线
plt.figure(figsize=(6,6))
nx.draw_networkx_nodes(G, pos, node_size=300)
nx.draw_networkx_labels(G, pos)
# MST 边（绿色）
nx.draw_networkx_edges(G, pos, edgelist=list(mst.edges()), edge_color='green', width=2)
# 匹配边（红色虚线）
nx.draw_networkx_edges(G, pos, edgelist=matching, edge_color='red', style='dashed', width=2)
nx.draw_networkx_edge_labels(G, pos, edge_labels=mst_labels, font_color='green')
match_labels = {(u, v): f"{G[u][v]['weight']:.2f}" for u, v in matching}
nx.draw_networkx_edge_labels(G, pos, edge_labels=match_labels, font_color='red')
plt.title("MST + 最小权完美匹配 (红色虚线为匹配边)")

# （3）绘制欧拉回路：蓝色线表示欧拉回路经过的边
plt.figure(figsize=(6,6))
nx.draw_networkx_nodes(G, pos, node_size=300)
nx.draw_networkx_labels(G, pos)
# 使用较淡的灰色展示 MST 和匹配边
nx.draw_networkx_edges(G, pos, edgelist=list(mst.edges()), edge_color='gray', style='dotted', width=1)
nx.draw_networkx_edges(G, pos, edgelist=matching, edge_color='gray', style='dotted', width=1)
# 蓝色实线绘制欧拉回路边
nx.draw_networkx_edges(G, pos, edgelist=euler_edges, edge_color='blue', width=2)
euler_labels = {(u, v): f"{G[u][v]['weight']:.2f}" for u, v in euler_edges}
nx.draw_networkx_edge_labels(G, pos, edge_labels=euler_labels, font_color='blue')
plt.title("欧拉回路 (蓝色为欧拉路径边)")

# （4）绘制最终 TSP 路径：紫色表示最终哈密尔顿回路
plt.figure(figsize=(6,6))
nx.draw_networkx_nodes(G, pos, node_size=300)
nx.draw_networkx_labels(G, pos)
nx.draw_networkx_edges(G, pos, edgelist=list(zip(hamilton_path, hamilton_path[1:])),
                       edge_color='purple', width=2)
final_labels = { (hamilton_path[i], hamilton_path[i+1]): f"{G[hamilton_path[i]][hamilton_path[i+1]]['weight']:.2f}"
                 for i in range(len(hamilton_path)-1) }
nx.draw_networkx_edge_labels(G, pos, edge_labels=final_labels, font_color='purple')
plt.title("最终 TSP 路径 (紫色为哈密尔顿回路边)")
plt.show()
