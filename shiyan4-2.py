import heapq

# 定义结点结构，用于存储在搜索过程中的状态
class Node:
    def __init__(self, level, value, weight, bound, taken):
        self.level = level        # 当前决策到第几个物品（level=index）
        self.value = value        # 当前总价值
        self.weight = weight      # 当前总重量
        self.bound = bound        # 当前结点的价值上界
        self.taken = taken        # 已选物品索引列表（记录选择了哪些物品）
    def __lt__(self, other):
        # 定义优先队列中结点比较: 按bound大小降序（bound大的优先）
        return self.bound > other.bound

def knapsack_branch_and_bound(weights, values, capacity):
    n = len(weights)
    # 按单位价值（value/weight）降序排序物品，以提高上界的精准性
    items = list(range(n))
    items.sort(key=lambda i: values[i]/weights[i], reverse=True)
    sorted_weights = [weights[i] for i in items]
    sorted_values = [values[i] for i in items]
    # 计算上界的函数（以当前结点的level为起点）
    def calc_bound(level, current_weight, current_value):
        if current_weight >= capacity:
            return 0  # 超过容量，不可行，上界记为0
        bound_value = current_value
        total_w = current_weight
        j = level
        # 贪心加入后续物品的价值
        while j < n and total_w + sorted_weights[j] <= capacity:
            total_w += sorted_weights[j]
            bound_value += sorted_values[j]
            j += 1
        # 如果还有剩余容量且未考虑完物品，则加下一物品的部分价值
        if j < n:
            bound_value += (capacity - total_w) * (sorted_values[j] / sorted_weights[j])
        return bound_value

    # 初始状态：在决策层次0，当前无物品，总重量0，总价值0
    best_value = 0
    best_items = []  # 存储最优解时选中的物品原始索引
    # 建立初始根结点并计算其上界
    root_bound = calc_bound(0, 0, 0)
    root = Node(level=0, value=0, weight=0, bound=root_bound, taken=[])
    # 优先队列初始化
    heap = []
    heapq.heappush(heap, root)

    # 分支限界搜索
    while heap:
        node = heapq.heappop(heap)  # 取出上界最高的结点
        if node.bound <= best_value:
            # 即使当前结点（活结点）上界不优于已知最优，也无需继续扩展
            continue
        level = node.level
        # 若未到达最后一个物品，继续分支扩展下一个物品决策
        if level < n:
            # **分支1**：选择当前物品
            new_weight = node.weight + sorted_weights[level]
            new_value = node.value + sorted_values[level]
            if new_weight <= capacity:
                taken_list = node.taken + [items[level]]  # 记录选了该物品（用原始索引）
                if new_value > best_value:
                    # 更新当前最优解
                    best_value = new_value
                    best_items = taken_list
                # 计算该分支结点的上界并加入队列
                bound_val = calc_bound(level + 1, new_weight, new_value)
                if bound_val > best_value:
                    heapq.heappush(heap, Node(level+1, new_value, new_weight, bound_val, taken_list))
            # **分支2**：不选择当前物品
            bound_val = calc_bound(level + 1, node.weight, node.value)
            if bound_val > best_value:
                heapq.heappush(heap, Node(level+1, node.value, node.weight, bound_val, node.taken))
    return best_value, best_items

# 测试
# weights = [2, 3, 4, 5]
# values = [3, 4, 5, 6]

weights = [1, 2, 3, 4, 5]
values = [1, 3, 4, 8, 10]

capacity = 8
max_val, items_selected = knapsack_branch_and_bound(weights, values, capacity)
print("最佳总价值:", max_val, "选择物品索引:", items_selected)