import tkinter as tk
from tkinter import messagebox
import random
import threading
import time


class WarmTipsApp:
    def __init__(self):
        self.tips = [
            "多喝水哦~", "保持微笑呀", "每天都要元气满满",
            "记得吃水果", "保持好心情", "好好爱自己",
            "梦想成真", "期待下一次见面", "金榜题名",
            "顺顺利利", "早点休息", "愿所有烦恼都消失",
            "别熬夜", "今天过得开心嘛", "天冷了，多穿衣服",
            "今天要开心哦", "今天要努力哦", "今天要加油哦"
        ]

        self.bg_colors = [
            "#FFB6C1",  # lightpink
            "#87CEEB",  # skyblue
            "#90EE90",  # lightgreen
            "#E6E6FA",  # lavender
            "#FFFFE0",  # lightyellow
            "#DDA0DD",  # plum
            "#FF7F50",  # coral
            "#FFE4C4",  # bisque
            "#7FFFD4",  # aquamarine
            "#FFE4E1",  # mistyrose
            "#F0FFF0",  # honeydew
            "#FFF0F5"  # lavenderblush
        ]

    def create_tip_window(self):
        # 创建新窗口
        window = tk.Toplevel()
        window.title("温馨提示")
        window.geometry("300x150")

        # 设置随机位置
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = random.randint(0, screen_width - 300)
        y = random.randint(0, screen_height - 150)
        window.geometry(f"300x150+{x}+{y}")

        # 随机选择背景色和提示语
        bg_color = random.choice(self.bg_colors)
        tip = random.choice(self.tips)

        # 创建标签
        label = tk.Label(
            window,
            text=tip,
            font=("Microsoft YaHei", 16, "bold"),
            bg=bg_color,
            fg="#333333",
            wraplength=280,
            justify="center"
        )
        label.pack(expand=True, fill="both")

        # 设置窗口始终在最前面
        window.attributes('-topmost', True)

    def start_tips(self, num_windows=20):
        """启动提示窗口"""

        def create_windows():
            for i in range(num_windows):
                # 在GUI线程中创建窗口
                window.after(0, self.create_tip_window)
                time.sleep(0.2)  # 每个窗口间隔200毫秒

        # 创建主窗口（隐藏）
        global window
        window = tk.Tk()
        window.withdraw()  # 隐藏主窗口

        # 在新线程中创建提示窗口
        thread = threading.Thread(target=create_windows)
        thread.daemon = True
        thread.start()

        # 显示完成提示
        window.after((num_windows + 1) * 200, lambda: messagebox.showinfo("完成", f"已显示 {num_windows} 个温馨提示！"))
        window.after((num_windows + 2) * 200, window.quit)

        window.mainloop()


if __name__ == "__main__":
    app = WarmTipsApp()
    app.start_tips(40)