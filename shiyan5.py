# 0-1 背包问题的回溯算法实现
def knapsack_backtrack(n, W, weights, values):
    # 当前最大价值和最优解
    max_value = 0
    best_solution = [0] * n

    # 回溯法函数，idx是当前考虑的物品，current_weight是当前背包的重量，current_value是当前背包的总价值
    def backtrack(idx, current_weight, current_value, solution):
        nonlocal max_value, best_solution

        # 如果所有物品都已考虑完，更新最大值
        if idx == n:
            if current_value > max_value:
                max_value = current_value
                best_solution = solution.copy()
            return

        # 当前物品不放入背包
        backtrack(idx + 1, current_weight, current_value, solution)

        # 当前物品放入背包（如果放入不超过背包容量）
        if current_weight + weights[idx] <= W:
            solution[idx] = 1
            backtrack(idx + 1, current_weight + weights[idx], current_value + values[idx], solution)
            solution[idx] = 0  # 回溯

    # 初始的回溯调用
    backtrack(0, 0, 0, [0] * n)

    return max_value, best_solution


# 示例数据
# n = 4  # 物品数量
# W = 5  # 背包容量
# weights = [2, 3, 4, 5]  # 物品重量
# values = [3, 4, 5, 6]  # 物品价值

n = 3  # 物品数量
W = 6  # 背包容量
weights = [1, 2, 3]  # 物品重量
values = [10, 20, 30]  # 物品价值

max_value, solution = knapsack_backtrack(n, W, weights, values)
print(f"最大总价值: {max_value}")
print(f"物品选择情况: {solution}")
