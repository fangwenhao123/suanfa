def longest_common_subsequence(X: str, Y: str):
    """求解字符串 X 和 Y 的最长公共子序列，返回其长度和具体序列"""
    m, n = len(X), len(Y)
    # 初始化 dp 数组，大小为 (m+1) x (n+1)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    # 动态规划填充 dp 表
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if X[i - 1] == Y[j - 1]:      # 若第 i 个字符相等（注意字符串索引偏移）
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:                        # 若第 i 个字符不等，则取上方或左方较大的值
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    # dp[m][n] 即为最长公共子序列长度
    lcs_length = dp[m][n]
    # 从 dp 表右下角回溯，构建最长公共子序列串
    i, j = m, n
    lcs_sequence = ""
    while i > 0 and j > 0:
        if X[i - 1] == Y[j - 1]:
            # 当前字符相同，属于 LCS
            lcs_sequence = X[i - 1] + lcs_sequence   # 将该字符加入序列前端
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            # 上方的子问题更优，向上移动
            i -= 1
        else:
            # 左方的子问题更优，向左移动
            j -= 1
    return lcs_length, lcs_sequence

# 测试函数
X = "ABADCBADAC"
Y = "CADDDCABBDAC"
length, sequence = longest_common_subsequence(X, Y)
print("字符串 X:", X)
print("字符串 Y:", Y)
print("LCS 长度:", length)
print("LCS 序列:", sequence)