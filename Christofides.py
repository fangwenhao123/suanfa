import networkx as nx
import matplotlib.pyplot as plt
import random


# 生成一个随机的完全图
def generate_complete_graph(num_nodes):
    G = nx.complete_graph(num_nodes)
    for (u, v) in G.edges():
        G[u][v]['weight'] = random.randint(1, 20)
    return G


# 绘制图
def draw_graph(G, pos, title, edge_labels=True, path_edges=None, node_color='green'):
    plt.figure(figsize=(8, 6))
    nx.draw(
        G, pos, with_labels=True, node_color=node_color, node_size=800, font_weight='bold', font_color='white'
    )
    edge_weights = nx.get_edge_attributes(G, 'weight')
    if edge_labels:
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_weights)
    if path_edges:
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2)
    plt.title(title)
    plt.show()


# 克里斯托菲德斯算法
def christofides_algorithm(G):
    # 1. 生成最小生成树(MST)
    mst = nx.minimum_spanning_tree(G)
    pos = nx.spring_layout(G)
    draw_graph(mst, pos, '最小生成树 (MST)')

    # 2. 找到度数为奇数的节点集
    odd_degree_nodes = [v for v, d in mst.degree() if d % 2 == 1]

    # 3. 在奇数度节点子图中找到最小权匹配
    odd_graph = G.subgraph(odd_degree_nodes)
    matching = nx.algorithms.matching.max_weight_matching(odd_graph, maxcardinality=True)
    matching_edges = list(matching)

    # 构造新图，将匹配边加入MST
    mst_with_matching = nx.MultiGraph(mst)
    mst_with_matching.add_edges_from(matching_edges)
    draw_graph(
        mst_with_matching, pos, 'MST + 完美匹配 (奇数度节点)', path_edges=matching_edges, node_color='blue'
    )

    # 4. 找到欧拉回路
    euler_circuit = list(nx.eulerian_circuit(mst_with_matching))
    euler_path_edges = [(u, v) for u, v in euler_circuit]
    draw_graph(
        mst_with_matching, pos, '欧拉回路', path_edges=euler_path_edges, node_color='green'
    )

    # 5. 将欧拉回路转化为哈密顿回路
    visited = set()
    hamiltonian_path = []
    for u, v in euler_circuit:
        if u not in visited:
            visited.add(u)
            hamiltonian_path.append(u)
    hamiltonian_path.append(hamiltonian_path[0])  # 回到起点

    # 绘制最终的哈密顿回路
    hamiltonian_edges = [(hamiltonian_path[i], hamiltonian_path[i + 1]) for i in range(len(hamiltonian_path) - 1)]
    draw_graph(
        G, pos, '最终哈密顿回路', path_edges=hamiltonian_edges, node_color='green'
    )
    return hamiltonian_path


# 主函数
if __name__ == "__main__":
    num_nodes = 6  # 节点数量
    G = generate_complete_graph(num_nodes)
    pos = nx.spring_layout(G)

    # 绘制完全图
    draw_graph(G, pos, '初始完全图', edge_labels=True)

    # 运行克里斯托菲德斯算法
    hamiltonian_path = christofides_algorithm(G)
    print("最优哈密顿回路:", hamiltonian_path)