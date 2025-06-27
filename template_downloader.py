# Author: GouHaoliang
# Date: 2025/6/6
# Time: 9:24

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import base64
import os
import json
from PIL import Image, ImageTk

# =====================================================
# 应用资源（所有模板文件都嵌入在此处）
# =====================================================

# 程序图标（Base64编码）
APP_ICON = """
iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAACXBIWXMAAAsTAAALEwEAmpwYAAAB
gmlDQ1BzUkdCIElFQzYxOTY2LTIuMQAAKJF1kb9Lw1AUxr9qpaJaSaRYCAiCMaEQ2CIFS5H0EUr
CoaAghJ1IdR0MheKto0exb+BFi0DqK4uH2ALuIoKO8KLoKj4C7g+ZfJpQ8LwejoV3ODjHZcBQ0L
qK4ujVLIZV1Zn1dK3I8fnzc3p7QxwBeKXy8rgE9FbA6S5B/RGmRZ4b1qE8q3h3g+8w6L28z/t+8
vM5vBZ9JxSQiYhGLiqhQyKJzTGNjVbE9yKubGQ2I3w09bDk9Ivwzcl8C4KftdHtOcR/EA3w8fCw
sD5I+C7vCzI0Qb4gFkqgL5NCLJZoYxJ6mWH+ExKxwD/h2B76R1RwOIkL8YQJgQaN1cxNxJECowzA
oUOoOAg0N2K8z6LeAv5EAJQyCYQALsC6cL9Vp8u4AIAzLcGgR2b5L+/1fTqWArwOA8GAWGRgwEC
wXfC8DkG6HwCDwDQNQNkYwGcRkABgAYN4AAAgAAABOAGkAYwByAG8AcwBvAGYAdAB8AFcAaQBuAG
QAbwB3AHMAIABQAGgAbwB0AG8AIABWAGkAZQB3AGUAcgAAAGJwbW5pY2F0aW9uAEUAeABjAGwAI
ABXAG8AcgBrAGIAbwBvAGsAfABEAG8AYwB1AG0AZQBuAHQAfABFAHgAYwBlAGwAIABXAG8AcgBr
AGIAbwBvAGsAAAAAAAABAAH//wACAAAAAAAAAAAAAAAAAAAAAAAABgABAAAAAQAAAAEAAAAAAA
AAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
"""

# 模板1: 年度报告模板 (Word文档)
ANNUAL_REPORT = "UEsDBBQAAAAIAMYdKVFqWjJQZAAAAGQAAAAIAAAAbWFpbi50eHQAZWZmZWN0aXZlIGFubnVhbCByZXBvcnQgdGVtcGxhdGUgZm9yIGVudGVycHJpc2VzLgpDb3B5cmlnaHQgKGMpIDIwMjMgQ29tcGFueSBJbmMuIE5vIHJpZ2h0cyByZXNlcnZlZC5QSwECFAAUAAAACADGHSlRaloyUGQAAABkAAAACAAAAAAAAAAAAAAAAAAAAAAAbWFpbi50eHRQSwUGAAAAAAAAAAEAAQAyAAAAKwAAAAAAAAAAAAD//xQAAAAUAAAA/v8DAAAAAA"

# 模板2: 财务报表模板 (Excel表格)
FINANCIAL_STATEMENT = "UEsDBBQAAAAIAMYdKVFqWjJQZAAAAGQAAAAIAAAAbWFpbi50eHQgZmluYW5jaWFsIHN0YXRlbWVudCB0ZW1wbGF0ZSBmb3Igc21hbGwgYnVzaW5lc3Nlcy4KQ29weXJpZ2h0IChjKSAyMDIzIENvbXBhbnkgSW5jLiBObyByaWdodHMgcmVzZXJ2ZWQuUEsBAhQAFAAAAAgAxh0pUWpaMlBkAAAAZAAAAAgAAAAAAAAAAAAAAAAAAAAAAG1haW4udHh0UEsFBgAAAAAAAAABAAEAMgAAADMAAAAAAAAAAAAAAP//FAAAABQAAAA="

# 模板3: 项目计划模板 (Word文档)
PROJECT_PLAN = "UEsDBBQAAAAIAMYdKVFqWjJQZAAAAGQAAAAIAAAAbWFpbi50eHQgcHJvamVjdCBwbGFubmluZyBhbmQgZXhlY3V0aW9uIHRlbXBsYXRlLgpDb3B5cmlnaHQgKGMpIDIwMjMgQ29tcGFueSBJbmMuIE5vIHJpZ2h0cyByZXNlcnZlZC5QSwECFAAUAAAACADGHSlRaloyUGQAAABkAAAACAAAAAAAAAAAAAAAAAAAAAAAbWFpbi50eHRQSwUGAAAAAAAAAAEAAQAyAAAAOwAAAAAAAAAAAAD//xQAAAAUAAAA"

# 模板4: 数据分析模板 (Excel表格)
DATA_ANALYSIS = "UEsDBBQAAAAIAMYdKVFqWjJQZAAAAGQAAAAIAAAAbWFpbi50eHQgZGF0YSBhbmFseXNpcyBhbmQgdmlzdWFsaXphdGlvbiB0ZW1wbGF0ZS4KQ29weXJpZ2h0IChjKSAyMDIzIENvbXBhbnkgSW5jLiBObyByaWdodHMgcmVzZXJ2ZWQuUEsBAhQAFAAAAAgAxh0pUWpaMlBkAAAAZAAAAAgAAAAAAAAAAAAAAAAAAAAAAG1haW4udHh0UEsFBgAAAAAAAAABAAEAMgAAADoAAAAAAAAAAAAAAP//FAAAABQAAAA="

# 模板5: 员工合同模板 (PDF文档)
EMPLOYMENT_CONTRACT = "UEsDBBQAAAAIAMYdKVFqWjJQZAAAAGQAAAAIAAAAbWFpbi50eHQgc3RhbmRhcmQgZW1wbG95bWVudCBjb250cmFjdCB0ZW1wbGF0ZS4KQ29weXJpZ2h0IChjKSAyMDIzIENvbXBhbnkgSW5jLiBObyByaWdodHMgcmVzZXJ2ZWQuUEsBAhQAFAAAAAgAxh0pUWpaMlBkAAAAZAAAAAgAAAAAAAAAAAAAAAAAAAAAAG1haW4udHh0UEsFBgAAAAAAAAABAAEAMgAAADcAAAAAAAAAAAAAAP//FAAAABQAAAA="

# 模板6: 会议纪要模板 (Word文档)
MEETING_MINUTES = "UFsDBBQAAAAIAMYdKVFqWjJQZAAAAGQAAAAIAAAAbWFpbi50eHQgcHJvZmVzc2lvbmFsIG1lZXRpbmcgbWludXRlcyB0ZW1wbGF0ZS4KQ29weXJpZ2h0IChjKSAyMDIzIENvbXBhbnkgSW5jLiBObyByaWdodHMgcmVzZXJ2ZWQuUEsBAhQAFAAAAAgAxh0pUWpaMlBkAAAAZAAAAAgAAAAAAAAAAAAAAAAAAAAAAG1haW4udHh0UEsFBgAAAAAAAAABAAEAMgAAADYAAAAAAAAAAAAAAP//FAAAABQAAAA="

# 模板7: 工作流程模板 (Visio图表)
WORKFLOW_TEMPLATE = "UFsDBBQAAAAIAMYdKVFqWjJQZAAAAGQAAAAIAAAAbWFpbi50eHQgYnVzaW5lc3MgcHJvY2VzcyBhbmQgd29ya2Zsb3cgdGVtcGxhdGUuCkNvcHlyaWdodCAoYykgMjAyMyBDb21wYW55IEluYy4gTm8gcmlnaHRzIHJlc2VydmVkLlBLAQIUBQAACAAIAB0eKVFqWjJQZAAAAGQAAAAIAAAAAAAAAAAAAAAAAAAAAABtYWluLnR4dFBLBQYAAAAAAAABAAEAMgAAADIAAAAAAAAAAAAA//8UAAAAFAAAAA=="

# 模板8: 营销计划模板 (PDF文档)
MARKETING_PLAN = "UFsDBBQAAAAIAMYdKVFqWjJQZAAAAGQAAAAIAAAAbWFpbi50eHQgY29tcHJlaGVuc2l2ZSBtYXJrZXRpbmcgcGxhbiB0ZW1wbGF0ZS4KQ29weXJpZ2h0IChjKSAyMDIzIENvbXBhbnkgSW5jLiBObyByaWdodHMgcmVzZXJ2ZWQuUEsBAhQAFAAAAAgAxh0pUWpaMlBkAAAAZAAAAAgAAAAAAAAAAAAAAAAAAAAAAG1haW4udHh0UEsFBgAAAAAAAAABAAEAMgAAADkAAAAAAAAAAAAAAP//FAAAABQAAAA="


class TemplateDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("离线文件模板下载器")
        self.root.geometry("800x500")
        # 作用: 控制应用程序窗口是否可以改变大小
        # 第一个参数: 控制水平方向(宽度)是否可以调整
        # 第二个参数: 控制垂直方向(高度)是否可以调整
        self.root.resizable(True, True)
        # self.root.iconphoto(False, tk.PhotoImage(data=base64.b64decode(APP_ICON)))
        self.root.configure(bg="#f0f5ff")

        # 设置应用样式
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TFrame', background='#f0f5ff')
        self.style.configure('TLabel', background='#f0f5ff', font=('微软雅黑', 10))
        self.style.configure('TButton', font=('微软雅黑', 10), background='#4a7bff', foreground='white')
        self.style.map('TButton', background=[('active', '#3a6bff'), ('pressed', '#2a5bff')])
        self.style.configure('Treeview', font=('微软雅黑', 9), rowheight=25)
        self.style.configure('Treeview.Heading', font=('微软雅黑', 10, 'bold'))
        self.style.configure('Header.TLabel', font=('微软雅黑', 16, 'bold'), foreground='#1a3b9a')

        self.create_widgets()
        self.load_templates()

    def create_widgets(self):
        # 顶部标题区域
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill='x', padx=10, pady=10)

        title_label = ttk.Label(header_frame, text="📁 离线文件模板下载", style='Header.TLabel')
        title_label.pack(side='left', padx=(10, 0))

        # 搜索区域
        search_frame = ttk.Frame(self.root)
        search_frame.pack(fill='x', padx=20, pady=(5, 10))

        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30, font=('微软雅黑', 10))
        search_entry.pack(side='left', fill='x', expand=True, padx=(0, 5))
        search_entry.bind('<KeyRelease>', self.filter_templates)

        search_btn = ttk.Button(search_frame, text="搜索", command=self.filter_templates, width=8)
        search_btn.pack(side='left')

        # 模板列表区域
        list_frame = ttk.Frame(self.root)
        list_frame.pack(fill='both', expand=True, padx=20, pady=(0, 10))

        columns = ("name", "type", "size", "desc")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", selectmode="browse")

        # 设置列宽
        self.tree.column("name", width=180, anchor='w')
        self.tree.column("type", width=100, anchor='w')
        self.tree.column("size", width=80, anchor='center')
        self.tree.column("desc", width=300, anchor='w')

        # 设置列标题
        self.tree.heading("name", text="模板名称", anchor='w')
        self.tree.heading("type", text="类型", anchor='w')
        self.tree.heading("size", text="大小", anchor='center')
        self.tree.heading("desc", text="描述", anchor='w')

        self.tree.pack(fill='both', expand=True, side='left')

        # 滚动条
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=scrollbar.set)

        # 详细信息区域
        detail_frame = ttk.Frame(self.root)
        detail_frame.pack(fill='x', padx=20, pady=(5, 10))

        detail_label = ttk.Label(detail_frame, text="详细信息:", font=('微软雅黑', 10, 'bold'))
        detail_label.pack(anchor='w', pady=(0, 5))

        self.detail_text = tk.Text(detail_frame, height=5, wrap='word', font=('微软雅黑', 9),
                                   bg='white', relief='flat', padx=5, pady=5)
        self.detail_text.pack(fill='x')
        self.detail_text.config(state='disabled')

        # 底部按钮区域
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(fill='x', padx=20, pady=10)

        download_btn = ttk.Button(btn_frame, text="下载模板", command=self.download_template, width=15)
        download_btn.pack(side='right', padx=(10, 0))

        preview_btn = ttk.Button(btn_frame, text="预览模板", command=self.preview_template, width=15)
        preview_btn.pack(side='right')

        # 绑定事件
        self.tree.bind('<<TreeviewSelect>>', self.show_template_details)

    def load_templates(self):
        """加载所有可用的模板"""
        templates = [
            {"name": "年度报告模板", "type": "Word文档", "size": "45KB",
             "desc": "标准化的公司年度报告文档格式", "ext": "docx", "data": ANNUAL_REPORT},

            {"name": "财务报表模板", "type": "Excel表格", "size": "68KB",
             "desc": "标准会计格式的财务报表模板", "ext": "xlsx", "data": FINANCIAL_STATEMENT},

            {"name": "项目计划模板", "type": "Word文档", "size": "32KB",
             "desc": "详细的项目规划和管理计划模板", "ext": "docx", "data": PROJECT_PLAN},

            {"name": "数据分析模板", "type": "Excel表格", "size": "78KB",
             "desc": "包含常用公式和图表的数据分析表格", "ext": "xlsx", "data": DATA_ANALYSIS},

            {"name": "员工合同模板", "type": "PDF文件", "size": "56KB",
             "desc": "标准劳动雇佣合同范本", "ext": "pdf", "data": EMPLOYMENT_CONTRACT},

            {"name": "会议纪要模板", "type": "Word文档", "size": "28KB",
             "desc": "结构化会议记录格式模板", "ext": "docx", "data": MEETING_MINUTES},

            {"name": "工作流程模板", "type": "Visio图表", "size": "42KB",
             "desc": "业务和工作流程可视化模板", "ext": "vsdx", "data": WORKFLOW_TEMPLATE},

            {"name": "营销计划模板", "type": "PDF文件", "size": "62KB",
             "desc": "市场营销活动规划模板", "ext": "pdf", "data": MARKETING_PLAN}
        ]

        for template in templates:
            self.tree.insert("", "end",
                             values=(template["name"], template["type"],
                                     template["size"], template["desc"]),
                             tags=(json.dumps(template),))

    def show_template_details(self, event):
        """显示选中的模板详细信息"""
        selected = self.tree.focus()
        if not selected:
            return

        tag_data = self.tree.item(selected, "tags")[0]
        template = json.loads(tag_data)

        self.detail_text.config(state='normal')
        self.detail_text.delete(1.0, tk.END)

        details = f"模板名称: {template['name']}\n"
        details += f"文件类型: {template['type']} (.{template['ext']})\n"
        details += f"文件大小: {template['size']}\n\n"
        details += f"详细描述:\n{template['desc']}\n\n"
        details += "注：所有模板均为范例格式，实际使用时请根据具体需求调整内容"

        self.detail_text.insert(tk.END, details)
        self.detail_text.config(state='disabled')

    def filter_templates(self, event=None):
        """根据搜索条件过滤模板"""
        query = self.search_var.get().lower()

        # 先删除所有项目
        for child in self.tree.get_children():
            self.tree.delete(child)

        # 重新加载所有模板，但只显示匹配的项目
        if not query:
            self.load_templates()
            return

        for template in self.tree.tag_has(""):
            data = json.loads(self.tree.item(template, "tags")[0])

            # 在名称和描述中搜索
            if (query in data["name"].lower() or
                    query in data["desc"].lower() or
                    query in data["type"].lower()):
                values = self.tree.item(template)["values"]
                self.tree.insert("", "end", values=values, tags=(json.dumps(data),))

    def preview_template(self):
        """预览模板（示例功能）"""
        selected = self.tree.focus()
        if not selected:
            messagebox.showinfo("提示", "请先选择一个模板进行预览")
            return

        tag_data = self.tree.item(selected, "tags")[0]
        template = json.loads(tag_data)

        messagebox.showinfo("模板预览",
                            f"正在预览: {template['name']}\n\n"
                            f"由于离线环境限制，我们无法展示实际内容预览。\n"
                            f'您可以通过"下载模板"功能保存到本地后查看完整内容。')

    def download_template(self):
        """下载选中的模板到本地"""
        selected = self.tree.focus()
        if not selected:
            messagebox.showinfo("提示", "请先选择一个模板进行下载")
            return

        tag_data = self.tree.item(selected, "tags")[0]
        template = json.loads(tag_data)

        # 获取保存路径
        default_filename = f"{template['name'].replace(' ', '_')}_模板.{template['ext']}"
        file_path = filedialog.asksaveasfilename(
            initialfile=default_filename,
            defaultextension=f".{template['ext']}",
            filetypes=[(f"{template['type']}文件", f"*.{template['ext']}"), ("所有文件", "*.*")]
        )

        if not file_path:  # 用户取消操作
            return

        try:
            # 解码并保存文件
            file_data = base64.b64decode(template["data"])
            with open(file_path, "wb") as f:
                f.write(file_data)

            messagebox.showinfo("下载成功",
                                f"模板 '{template['name']}' 已成功保存到:\n{file_path}\n\n"
                                "请使用相关软件打开此文件")
        except Exception as e:
            messagebox.showerror("下载错误", f"保存模板时出错:\n{str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = TemplateDownloader(root)
    root.mainloop()