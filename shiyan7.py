import heapq
import random

# 近似算法：最长处理时间优先 (LPT) 调度
def LPT_schedule(tasks, m):
    # tasks: 任务处理时间列表
    # m: 机器数量
    # 返回每台机器分配的任务列表和每台机器的总时间

    # 将任务按处理时间降序排序（保留任务ID）
    sorted_tasks = sorted(enumerate(tasks, start=1), key=lambda x: x[1], reverse=True)
    # 初始化每台机器的当前负载和任务列表
    machine_loads = [(0, i) for i in range(m)]
    heapq.heapify(machine_loads)
    assignments = [[] for _ in range(m)]

    # 逐个分配任务：每次将最大任务给当前最空闲的机器
    for task_id, duration in sorted_tasks:
        load, i = heapq.heappop(machine_loads)       # 取出当前最小负载的机器
        assignments[i].append((task_id, duration))   # 将该任务分配给它
        new_load = load + duration
        heapq.heappush(machine_loads, (new_load, i)) # 更新该机器负载并放回堆

    # 计算每台机器的总运行时间
    machine_times = [sum(d for _, d in assignments[i]) for i in range(m)]
    return assignments, machine_times

# 生成数据集1和数据集2
random.seed(42)
m1, n1 = 3, 10
tasks1 = [random.randint(1, 20) for _ in range(n1)]
m2, n2 = 4, 15
tasks2 = [random.randint(1, 20) for _ in range(n2)]

# 调用算法并输出结果
assign1, loads1 = LPT_schedule(tasks1, m1)
print(f"数据集1任务耗时: {tasks1}, 机器数: {m1}")
for i in range(m1):
    task_list = [f"任务{tid}(耗时{d})" for tid, d in assign1[i]]
    print(f"机器{i+1}: {task_list}, 完工时间 = {loads1[i]}")

assign2, loads2 = LPT_schedule(tasks2, m2)
print(f"\n数据集2任务耗时: {tasks2}, 机器数: {m2}")
for i in range(m2):
    task_list = [f"任务{tid}(耗时{d})" for tid, d in assign2[i]]
    print(f"机器{i+1}: {task_list}, 完工时间 = {loads2[i]}")
