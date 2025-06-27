# Author: GouHaoliang
# Date: 2025/6/16
# Time: 11:11

import pandas as pd

# 创建示例DataFrame
data = {'产品': ['苹果', '香蕉', '苹果'], '销量': [100, 200, 150]}
df = pd.DataFrame(data)

pos_dict = dict(zip(data['产品'], data['销量']))

print(pos_dict['苹果'])
print(pos_dict)

import tkinter as tk
from tkcalendar import Calendar
from datetime import datetime


def show_calendar():
    top = tk.Toplevel()
    cal = Calendar(top, selectmode='day', date_pattern='y-mm-dd')
    cal.pack()
    btn = tk.Button(top, text="确认", command=lambda: print(cal.get_date()))
    btn.pack()


def select_range():
    top = tk.Toplevel()
    # 开始日期日历
    cal_start = Calendar(top, selectmode='day')
    cal_start.pack(side='left', padx=10)
    # 结束日期日历
    cal_end = Calendar(top, selectmode='day')
    cal_end.pack(side='right', padx=10)

    def confirm():
        start = cal_start.get_date()
        end = cal_end.get_date()
        print(f"范围: {start} 至 {end}")
        start_date = datetime.strptime(start, '%m/%d/%y')
        end_date = datetime.strptime(end, '%m/%d/%y')
        print(f"范围: {start_date} 至 {end_date}")
        top.destroy()

    tk.Label(top, text="输入工位号").pack(pady=10)
    pos_no_entry = tk.Entry(top)
    pos_no_entry.pack(pady=10)
    tk.Button(top, text="确定", command=confirm).pack(pady=10)


# root = tk.Tk()
# tk.Button(root, text="选择日期范围", command=select_range).pack()
# tk.Button(root, text="选择日期", command=show_calendar).pack()
# root.mainloop()


# from pathlib import Path
#
# # 获取当前工作目录的Path对象
# current_dir = Path.cwd()
#
# # 添加文件名（如"example.txt"）
# file_path = current_dir / "example.txt"
# print(file_path)

# 创建示例 DataFrame
data = {'A': [1, 2, 3, 4, 5], 'B': [5, 5, 5, 5, 5]}
df = pd.DataFrame(data)
# A A1 A2 A3
# 1 n  n  n
# 2 1  n  n
# 3 2  1  n
print(df)
df_new = df.reset_index()
print(df)
# print(df.shift(1))
# print(df.shift(2))
# print(df.shift(3))
#
# print(df[2:])

# 找出 A 列中不同的值
# a_values = df['A'].unique()
# b_values = df['B'].unique()
# print("A 列中不同的值:", a_values)
# print("A 列中不同的值:", b_values)
# print("A 列中不同的值:", type(b_values[0]))
# print("A 列中不同的值:", type(b_values))
#
# print(df.A)
#
# print(df.iloc[1])
#
# for col_idx, col_name in enumerate(df.columns, start=2):  # 从第3列开始
#     if col_name in ['A']:
#         print('sum')
#     elif col_name in ['B']:
#         print('avg')
#     else:
#         print('ori')

