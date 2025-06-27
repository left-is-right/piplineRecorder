# Author: GouHaoliang
# Date: 2025/5/12
# Time: 9:30

import tkinter as tk
from tkinter import messagebox

from mysql_connect import MysqlConnect
import pandas as pd
from datetime import datetime
from scroll_canvas import ScrollCanvas
from file_input_window import FileInputWindow
from pos_input_window import PosInputWindow
from date_calendar_window import DateCalendarWindow
from util_fun import *
from decimal import Decimal
from pathlib2 import Path
from excel_writer import *


class DynamicButtonGenerator:

    def __init__(self, root):
        self.root = root
        self.root.title("两列按钮生成器")
        self.root.geometry("400x400")

        '''
        通用变量
        '''
        self.executor = None    # mysql执行器变量
        self.emp_dict = {}      # 员工工位姓名字典
        self.shift = ''    # 员工工位班次字典
        self.pos_emp_table = 'shift_pos_emp_info'
        self.op_table = 'operation_track_record'
        self.unit_price = 0     # 桶单价
        self.shift_start_time = None    # 班次起始时间
        self.output_path = Path.cwd()   # 结果文件输出路径
        self.is_recorder = False        # 标记当前是否是记录状态

        '''
        组件变量
        '''
        # 创建输入框架
        self.input_frame = tk.Frame()
        self.input_frame.pack(pady=5)

        # 创建统计框架
        self.stats_frame = tk.Frame()
        self.stats_frame.pack(pady=5)

        # 创建输入框验证函数（实时验证输入格式）
        vcmd = self.input_frame.register(validate_input)

        # mysql输入
        self.user_label = tk.Label(self.input_frame, text="数据库账号")
        self.user_label.grid(row=1, column=0)
        self.user_entry = tk.Entry(self.input_frame)
        self.user_entry.grid(row=1, column=1)
        self.pass_label = tk.Label(self.input_frame, text="数据库密码")
        self.pass_label.grid(row=2, column=0)
        self.pass_entry = tk.Entry(self.input_frame, show='*')
        self.pass_entry.grid(row=2, column=1)
        self.price_label = tk.Label(self.input_frame, text="设定桶单价")
        self.price_label.grid(row=3, column=0)
        self.price_entry = tk.Entry(self.input_frame, validate="key", validatecommand=(vcmd, '%P'))
        self.price_entry.grid(row=3, column=1)

        # 按键
        self.op_record_btn = tk.Button(self.root, text="操作记录", command=lambda: self.init_secondary_menu('记录'))
        self.op_record_btn.pack(pady=5)

        # 按键
        self.stats_btn = tk.Button(self.root, text="统计导出", command=lambda: self.init_secondary_menu('统计'))
        self.stats_btn.pack(pady=5)

        # 可滚动容器
        self.canvas = ScrollCanvas(self.root).create_canvas()

        # 内部框架（用于两列布局）
        self.inner_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor=tk.NW)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)  # 保留绑定

    def on_closing(self):
        if tk.messagebox.askokcancel("关闭", "确定关闭本软件？"):
            if self.executor is not None:
                end_time_temp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print('软件关闭前修改当前班次结束时间')
                self.executor.update_end_time_sql(end_time_temp)
            self.root.destroy()  # 销毁主窗口

    def init_executor(self):
        user = self.user_entry.get()
        password = self.pass_entry.get()
        try:
            self.executor = MysqlConnect(user, password)
        except Exception:
            messagebox.showwarning('提示', '数据库连接失败：请检查数据库用户名和密码')
            return False
        return True

    # 生成所有工位按键
    def generate_buttons(self, file_path):

        # 导入员工及工位数据
        res_code, msg = self.import_emp_pos(file_path)

        if res_code != 0:
            messagebox.showwarning('提示', msg)
            return

        # 创建操作表
        self.executor.create_table(self.op_table)

        # 按两列动态生成按钮
        for i in range(len(self.emp_dict)):
            row = i // 2  # 计算行号
            col = i % 2  # 计算列号（0或1）

            btn = tk.Button(
                self.inner_frame,
                text=f"工位 {i + 1}",
                command=lambda x=i + 1: self.open_pos_input_window(x),
                width=15
            )
            btn.grid(row=row, column=col, padx=5, pady=5, sticky=tk.NSEW)

        # 更新滚动区域
        self.inner_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

        # 更新当前记录状态为True
        self.is_recorder = True

    # 生成工位的扣杂率次级输入窗口
    def open_pos_input_window(self, pos_no):
        """打开次级窗口并传递回调函数"""
        PosInputWindow(self.root, pos_no, self.insert_op_fun)

    # 生成日期选择窗口
    def open_date_calendar_window(self, type_code):
        if type_code == 0:
            DateCalendarWindow(self.root, self.today_stats_fun, type_code)
        elif type_code == 1:
            DateCalendarWindow(self.root, self.his_stats_fun, type_code)
        else:
            DateCalendarWindow(self.root, self.his_detail_fun, type_code)

    # 初始化二级功能菜单
    def init_secondary_menu(self, init_type):
        """
        1、初始化数据库链接
        2、检查桶单价数据类型
        3、打开次级窗口并传递回调函数
        """
        init_res = self.init_executor()
        if init_res:
            if init_type == '记录':
                price_res = self.unit_price_check()
                if price_res:
                    # 生成所有统计按钮
                    self.create_stats_button(True)
                    FileInputWindow(self.root, self.generate_buttons)
            elif init_type == '统计':
                self.create_stats_button(False)

    # 检查桶单价
    def unit_price_check(self):
        self.unit_price = self.price_entry.get()
        try:
            # 检查是否为有效小数且小于1
            if self.unit_price and 0 <= Decimal(self.unit_price):
                self.unit_price = Decimal(self.unit_price)
                return True
            else:
                return False
        except Exception:
            messagebox.showwarning('提示', '桶单价输入错误：请检查是否为大于0的数值')
            return False

    # 生成所有统计按钮组件
    def create_stats_button(self, is_recorder):
        """打开次级窗口并传递回调函数"""
        # 销毁数据库及数据输入组件
        destroy_frame(self.input_frame)
        # 隐藏原生成按钮（关键操作）[8](@ref)
        self.op_record_btn.pack_forget()
        self.stats_btn.pack_forget()

        col_idx = 0

        if is_recorder:
            tk.Button(self.stats_frame, text='换班结算统计', command=self.shift_change_stats_fun)\
                .grid(row=0, column=col_idx, padx=5, pady=5)
            col_idx += 1
        tk.Button(self.stats_frame, text='当日统计', command=lambda: self.open_date_calendar_window(0))\
            .grid(row=0, column=col_idx, padx=5, pady=5)
        col_idx += 1
        tk.Button(self.stats_frame, text='历史统计', command=lambda: self.open_date_calendar_window(1))\
            .grid(row=0, column=col_idx, padx=5, pady=5)
        col_idx += 1
        tk.Button(self.stats_frame, text='历史详情', command=lambda: self.open_date_calendar_window(2))\
            .grid(row=0, column=col_idx, padx=5, pady=5)

    # 换班统计函数
    def shift_change_stats_fun(self):
        # 记录结束时间
        end_time_point = datetime.now()
        end_time = end_time_point.strftime("%Y-%m-%d %H:%M:%S")
        end_date = end_time_point.strftime("%Y年%m月%d日")

        # 根据时间范围筛选数据
        res = self.executor.select_shift_change_stats(self.shift_start_time, end_time, self.shift)
        # shift_change_stats_path = self.output_path / "换班统计表.xlsx"
        header = f"{end_date}{self.shift}番茄脱皮、去蒂统计表"
        output_path = f'{header}.xlsx'
        try:
            shift_change_stats_writer(res, header, output_path)
            tk.messagebox.showinfo("统计完成", f"{end_date}统计结果已输出至{output_path}")
        except Exception as e:
            tk.messagebox.showerror("详情统计失败", f"错误原因：{e}")
            return

        # 如果当前是记录状态，则为当前班次结算动作，需要准备换班动作
        if self.is_recorder:
            # 更新员工表状态
            self.executor.update_end_time_sql(end_time)

            # 销毁所有旧工位按钮
            for widget in self.inner_frame.winfo_children():
                widget.destroy()

            # 选择是否换班
            if tk.messagebox.askokcancel("是否换班", "确定是否换班"):
                # 弹出文件选择窗口，并重新生成工位按钮
                FileInputWindow(self.root, self.generate_buttons)
            else:
                self.is_recorder = False

    # 单日统计函数
    def today_stats_fun(self, stats_date_point):
        stats_date = stats_date_point.strftime("%Y-%m-%d")
        stats_date_head = stats_date_point.strftime("%Y年%m月%d日")
        res = self.executor.select_today_stats(stats_date)
        header = f"{stats_date_head}番茄脱皮、去蒂单日统计表"
        output_file_name = f'{header}.xlsx'
        try:
            his_stats_writer(res, header, output_file_name)
            tk.messagebox.showinfo("统计完成", f"{stats_date_head}统计结果已输出至{output_file_name}")
        except Exception as e:
            tk.messagebox.showerror("详情统计失败", f"错误原因：{e}")

    # 历史统计函数
    def his_stats_fun(self, start_date_point, end_date_point):
        start_date = start_date_point.strftime("%Y-%m-%d")
        end_date = end_date_point.strftime("%Y-%m-%d")
        start_date_head = start_date_point.strftime("%Y年%m月%d日")
        res = self.executor.select_his_stats(start_date, end_date)
        header = f"{start_date_head}番茄脱皮、去蒂统计表"
        output_file_name = f'{header}.xlsx'
        try:
            his_stats_writer(res, header, output_file_name)
            tk.messagebox.showinfo("统计完成", f"{end_date}统计结果已输出至{output_file_name}")
        except Exception as e:
            tk.messagebox.showerror("详情统计失败", f"错误原因：{e}")

    # 历史详情函数
    def his_detail_fun(self, start_date_point, end_date_point, pos_no):
        start_date = start_date_point.strftime("%Y-%m-%d")
        end_date = end_date_point.strftime("%Y-%m-%d")
        start_date_head = start_date_point.strftime("%Y年%m月%d日")
        res = self.executor.select_his_detail(pos_no, start_date, end_date)
        header = f"{start_date_head}{pos_no}号番茄脱皮、去蒂扣杂表"
        output_file_name = f'{header}.xlsx'
        try:
            his_detail_writer(res, header, output_file_name)
            tk.messagebox.showinfo("统计完成", f"{end_date}统计结果已输出至{output_file_name}")
        except Exception as e:
            tk.messagebox.showerror("详情统计失败", f"错误原因：{e}")

    # 操作记录
    def insert_op_fun(self, pos_no, impurity_rate):
        # 获取当前时间（精确到微秒）
        current_time = datetime.now()
        # 格式化为标准时间字符串（YYYY-MM-DD HH:MM:SS）
        op_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        self.executor.insert_op(pos_no, self.emp_dict[pos_no], self.shift,
                                impurity_rate, self.unit_price, op_time, self.op_table)

    # 员工数据导入
    def import_emp_pos(self, file_path):
        """
         修改工位及员工对应关系表
         1、每次导入操作都修改本表
         2、生成一个Map变量，key是工位，value是操作人
         3、根据导入数据，生成对应数量按钮
         :return:
         1、res_code: 错误编码
         2、msg: 错误信息
         """
        # 0、读取数据，并记录当前时间
        pos_emp_data = pd.read_excel(file_path)
        start_time_temp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pos_emp_data['start_time'] = start_time_temp
        pos_emp_data['end_time'] = '9999-12-31'

        # 1、列名替换&数据校验
        if pos_emp_data.isna().values.any():
            return -1, '数据有空值'
        try:
            pos_emp_data['pos_no'] = pos_emp_data['工位编号']
            pos_emp_data['emp_name'] = pos_emp_data['姓名']
            pos_emp_data['shift'] = pos_emp_data['班次']
            pos_emp_data = pos_emp_data[['pos_no', 'emp_name', 'shift']]
        except KeyError:
            return -2, "数据列名错误，请检查列名是否包含‘工位编号’，‘姓名’， ‘班次’"

        # 2、检查工位号是否有重复值
        duplicates = pos_emp_data['pos_no'].duplicated()
        if duplicates.any():
            # 获取具体的重复键及其出现位置
            dup_keys = pos_emp_data.loc[duplicates, 'pos_no'].unique()
            dup_positions = pos_emp_data[pos_emp_data['pos_no'].isin(dup_keys)].index.tolist()
            error_msg = (
                "'工位编号' 存在重复值，请检查文件。\n"
                f"重复值: {dup_keys.tolist()}\n"
                f"重复位置（行索引）: {dup_positions}"
            )
            return -3, error_msg

        # 3、检查班次是否为唯一值
        shift_values = pos_emp_data['shift'].unique()
        if len(shift_values) > 1:
            # 获取具体的重复键及其出现位置
            error_msg = (
                "'班次' 不唯一，请检查文件。\n"
                f"班次值: {shift_values}\n"
            )
            return -4, error_msg

        # 4、导入数据库
        try:
            self.executor.import_data(pos_emp_data, self.pos_emp_table)
        except Exception as e:
            return -5, f"员工信息导入失败，错误原因:{e}"

        # 4、生成字典，确定班次
        self.emp_dict = dict(zip(pos_emp_data['pos_no'], pos_emp_data['emp_name']))
        self.shift = shift_values[0]

        # 5、记录该班次起始时间
        self.shift_start_time = start_time_temp

        return 0, "完成导入"


if __name__ == "__main__":
    root = tk.Tk()
    app = DynamicButtonGenerator(root)
    root.mainloop()

