# Author: GouHaoliang
# Date: 2025/6/20
# Time: 10:25
import tkinter as tk
from tkinter import filedialog
from pathlib2 import Path
from tkinter import messagebox


class FileInputWindow:

    def __init__(self, parent, callback):
        """次级窗口初始化
        :param parent: 父窗口
        :param pos_no: 工位编号
        :param callback: 确认后的回调函数
        """

        self.callback = callback
        self.window = tk.Toplevel(parent)
        self.window.title("选择员工工位文件路径")
        self.window.geometry("400x200")
        self.window.resizable(False, False)
        self.window.transient(parent)
        self.window.grab_set()

        # 创建界面组件
        frame = tk.Frame(self.window)
        frame.pack(pady=10)
        # 工位与姓名文件输入
        self.input_path = tk.StringVar()  # 工位名称对应关系文件路径
        self.input_path.set(str(Path.cwd()))  # 默认当前目录
        tk.Entry(frame, textvariable=self.input_path, state="readonly", width=40).pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="路径选择", command=self.select_path).pack(side=tk.LEFT)

        # 确认按钮
        self.confirm_btn = tk.Button(self.window, text="确认", command=self.on_confirm)
        self.confirm_btn.pack(pady=10)

    def on_confirm(self):
        """确认按钮回调"""
        file_path = self.input_path.get()
        if file_path:
            self.callback(file_path)
            self.window.destroy()
        else:
            messagebox.showwarning("警告", "请输入文件路径")

    # 定义更新路径函数
    def select_path(self):
        path_ = filedialog.askopenfilename()
        if path_ == "":
            self.input_path.get()
        else:
            path_ = path_.replace("/", "\\")
            self.input_path.set(path_)

