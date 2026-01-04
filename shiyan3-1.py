def max_programs_detail(n, L, file_len):
    # 记录程序及其编号
    programs = list(enumerate(file_len, start=1))  # [(编号, 长度), ...]

    # 按长度从小到大排序
    programs.sort(key=lambda x: x[1])

    total_len = 0
    selected = []  # 存储选中的程序编号与长度

    # 贪心选择
    for pid, length in programs:
        if total_len + length <= L:
            total_len += length
            selected.append((pid, length))
        else:
            break

    return selected, total_len, len(selected)

# 示例测试
n = 7
L = 100
file_len = [22, 15, 39, 55, 33, 79, 10]

selected, total_len, count = max_programs_detail(n, L, file_len)

print(f"最多可以存放的程序数量：{count}")
print(f"总占用长度：{total_len}")
print("选择的程序如下：")
for pid, length in selected:
    print(f"程序 {pid}，长度 {length}")
