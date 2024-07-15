# coding=utf-8
# utils.py
def insert_before_line(file_path, line_number, content):
    """在指定行前插入内容并换行。

    Args:
        file_path (str): 文件路径。
        line_number (int): 要在其前插入内容的行号（从1开始计数）。
        content (str): 要插入的内容。
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    if line_number < 1 or line_number > len(lines) + 1:
        raise ValueError("Line number is out of range.")

    lines.insert(line_number - 1, content + '\n')

    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(lines)


def insert_after_line(file_path, line_number, content):
    """在指定行后插入内容并换行。

    Args:
        file_path (str): 文件路径。
        line_number (int): 要在其后插入内容的行号（从1开始计数）。
        content (str): 要插入的内容。
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    if line_number < 0 or line_number > len(lines):
        raise ValueError("Line number is out of range.")

    lines.insert(line_number, content + '\n')

    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(lines)


def replace_line(file_path, line_number, new_content):
    """替换文件中指定行的内容。

    Args:
        file_path (str): 文件路径。
        line_number (int): 要替换内容的行号（从1开始计数）。
        new_content (str): 新的行内容。
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 检查行号是否有效
    if line_number < 1 or line_number > len(lines):
        raise ValueError("Line number is out of range.")

    # 替换指定行的内容
    lines[line_number - 1] = new_content + '\n'

    # 将修改后的内容写回文件
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(lines)
