# Author: GouHaoliang
# Date: 2025/6/20
# Time: 10:26

import tkinter as tk
from tkinter import messagebox
from util_fun import *


class PosInputWindow:
    def __init__(self, parent, pos_no, callback):
        """次级窗口初始化
        :param parent: 父窗口
        :param pos_no: 工位编号
        :param callback: 确认后的回调函数
        """
        self.callback = callback
        self.window = tk.Toplevel(parent)
        self.window.title(f"输入工位【{pos_no}】的扣杂率")
        self.window.geometry("300x150")
        self.window.resizable(False, False)
        self.window.transient(parent)
        self.window.grab_set()
        self.pos_no = pos_no

        print('创建子窗口')
        # 创建输入框验证函数（实时验证输入格式）
        vcmd = self.window.register(validate_input)

        # 创建界面组件
        tk.Label(self.window, text="请输入小于1的小数：").pack(pady=10)

        # 使用StringVar跟踪输入变化
        self.input_var = tk.StringVar()
        self.entry = tk.Entry(
            self.window,
            validate="key",
            validatecommand=(vcmd, '%P'),
            textvariable=self.input_var
        )
        self.entry.pack(pady=5, ipadx=10, ipady=5)

        # 输入后直接按Enter键确认（扩展功能）
        self.entry.bind("<Return>", lambda e: self.on_confirm())
        # 让输入框自动获得焦点[1,4](@ref)
        self.entry.focus_set()
        # 关键点2：确保窗口获得焦点（针对部分系统的兼容处理）[5,9](@ref)
        self.window.grab_set()

        # 创建禁用状态的确认按钮
        self.confirm_btn = tk.Button(
            self.window,
            text="确认",
            state="disabled",
            command=self.on_confirm,
            width=10
        )
        self.confirm_btn.pack(pady=10)

        # 绑定输入变化事件
        self.input_var.trace_add("write", self.update_button_state)

    def update_button_state(self, *args):
        """根据输入有效性更新按钮状态[9,11](@ref)"""
        input_val = self.input_var.get()
        try:
            # 检查是否为有效小数且小于1
            if input_val and 0 <= float(input_val) < 1:
                self.confirm_btn.config(state="normal")
            else:
                self.confirm_btn.config(state="disabled")
        except ValueError:
            self.confirm_btn.config(state="disabled")

    def on_confirm(self):
        """确认按钮点击处理"""
        input_val = self.input_var.get()
        try:
            # 确保值有效后传递给回调函数
            impurity_rate = float(input_val)
            if 0 <= impurity_rate < 1:
                self.callback(self.pos_no, impurity_rate)
                self.window.destroy()
        except ValueError:
            messagebox.showerror("错误", "请输入有效的小数！")
