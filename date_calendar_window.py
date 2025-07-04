# Author: GouHaoliang
# Date: 2025/6/25
# Time: 17:17
from tkcalendar import Calendar
import tkinter as tk
from datetime import datetime


class DateCalendarWindow:

    def __init__(self, parent, callback, type_code):
        """次级窗口初始化
        :param parent: 父窗口
        :param callback: 确认后的回调函数
        :param type_code: 调用类型（0：单日  1：历史统计  2：历史详情
        """
        self.callback = callback
        self.window = tk.Toplevel(parent)
        self.window.title(f"选择日期范围")
        self.window.transient(parent)
        self.window.grab_set()
        self.type_code = type_code

        if type_code == 0:
            # 单日统计
            self.cal_stats = Calendar(self.window, selectmode='day', locale='zh_CN')
            self.cal_stats.pack()
        else:
            # 起始日期日历
            self.cal_start = Calendar(self.window, selectmode='day', locale='zh_CN')
            self.cal_start.pack(side='left', padx=10)
            # 结束日期日历
            self.cal_end = Calendar(self.window, selectmode='day', locale='zh_CN')
            self.cal_end.pack(side='right', padx=10)

            if type_code == 2:
                vcmd = self.window.register(self.validate_int_input)
                tk.Label(self.window, text="输入工位号").pack(pady=10)
                self.pos_no_entry = tk.Entry(self.window, validate="key", validatecommand=(vcmd, '%P'))
                self.pos_no_entry.pack(pady=10)

        tk.Button(self.window, text="确定", command=self.confirm).pack(pady=10)

    # 选取日期范围窗口
    def confirm(self):
        if self.type_code == 0:
            stats_date = datetime.strptime(self.cal_stats.get_date(), '%Y/%m/%d')
            self.callback(stats_date)
        else:
            start_date = datetime.strptime(self.cal_start.get_date(), '%Y/%m/%d')
            end_date = datetime.strptime(self.cal_end.get_date(), '%Y/%m/%d')

            if self.type_code == 2:
                pos_no = int(self.pos_no_entry.get())
                self.callback(start_date, end_date, pos_no)
            else:
                self.callback(start_date, end_date)
        self.window.destroy()

    def validate_int_input(self, new_value):
        # 如果输入为空字符串，允许输入
        if new_value == "":
            return True

        # 验证输入是否为整数且在范围内
        try:
            value = int(new_value)
            return 1 <= value
        except ValueError:
            return False

