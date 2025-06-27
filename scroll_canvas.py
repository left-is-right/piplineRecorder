# Author: GouHaoliang
# Date: 2025/6/20
# Time: 10:23
import tkinter as tk


class ScrollCanvas:

    def __init__(self, root):
        # 可滚动容器
        self.canvas = tk.Canvas(root)
        self.scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL, command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 绑定鼠标滚轮事件
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        # 根据滚轮方向滚动（Windows/Linux: event.delta, macOS: -event.delta）
        scroll_direction = -1 if event.delta > 0 else 1
        self.canvas.yview_scroll(scroll_direction, "units")
        self.scrollbar.set(*self.canvas.yview())  # 强制同步位置 [3](@ref)

    def create_canvas(self):
        return self.canvas
