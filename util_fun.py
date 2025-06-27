# Author: GouHaoliang
# Date: 2025/6/20
# Time: 10:27
import re


def validate_input(new_value):
    """验证输入格式（允许数字和小数点）[1,3](@ref)
    :param new_value: 输入框的新值
    :return: 是否允许输入
    """
    # 允许空输入（用于删除操作）
    if new_value == "":
        return True

    # 验证数字和小数点格式
    pattern = r'^[0-9]*\.?[0-9]*$'
    return bool(re.fullmatch(pattern, new_value))


# 布局销毁
def destroy_frame(frame):
    """完全销毁Frame及其所有子组件"""
    # 递归销毁所有子组件
    for widget in frame.winfo_children():
        widget.destroy()

    # 销毁Frame自身
    frame.destroy()

