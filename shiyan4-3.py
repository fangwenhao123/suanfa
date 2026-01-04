from collections import deque

def n_queens_branch_and_bound(N):
    # 使用队列实现广度优先搜索
    queue = deque()
    queue.append([])  # 初始状态：空布局
    while queue:
        partial = queue.popleft()       # 取出一个部分布局状态
        row = len(partial)             # 当前需要放置皇后的行索引
        if row == N:
            return partial  # 找到一个完整的解决方案（列表长度为N）
        # 在该行尝试放置皇后
        for col in range(N):
            # 检查col列放置是否与partial冲突
            conflict = False
            for r, c in enumerate(partial):
                if c == col or abs(col - c) == (row - r):
                    conflict = True
                    break
            if conflict:
                continue  # 冲突则剪枝跳过
            # 无冲突，则加入新状态
            new_state = partial + [col]
            queue.append(new_state)
    return None  # 若无解，返回None

# 测试
print(n_queens_branch_and_bound(8))

print("11111")