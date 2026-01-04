def average_waiting_time_detail(n, s, service_times):
    # 记录任务编号
    tasks = list(enumerate(service_times, start=1))  # [(编号, 服务时间), ...]

    # 按服务时间排序（贪心处理较短任务优先）
    tasks.sort(key=lambda x: x[1])

    # 初始化服务台信息
    station_time = [0] * s  # 每个服务台的累计服务时间
    station_tasks = [[] for _ in range(s)]  # 每个服务台的任务队列
    wait_times = [0] * n  # 每个任务的等待时间（按排序后的顺序）

    # 分配任务
    for idx, (task_id, t_time) in enumerate(tasks):
        # 找到当前最空闲（累计时间最短）的服务台
        station = min(range(s), key=lambda i: station_time[i])

        # 记录等待时间
        wait_times[idx] = station_time[station]

        # 将任务加入该服务台队列
        station_tasks[station].append((task_id, t_time))

        # 更新服务台的累计服务时间
        station_time[station] += t_time

    # 计算平均等待时间
    avg_wait = sum(wait_times) // n

    return avg_wait, station_tasks

# 示例测试
n = 10
s = 4
service_times = [7, 9, 13, 2, 4, 5, 11, 8, 1, 6]

avg_wait, station_tasks = average_waiting_time_detail(n, s, service_times)

print(f"平均等待时间：{avg_wait}")
print("\n每个服务台的任务队列如下：")
for i, queue in enumerate(station_tasks):
    print(f"服务台 {i+1}: ", end="")
    for task_id, t in queue:
        print(f"[任务 {task_id}, 服务时间 {t}] ", end="")
    print()
