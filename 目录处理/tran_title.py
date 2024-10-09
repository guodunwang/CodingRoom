import re
import sys

def convert_to_markdown(text):
    lines = text.split('\n')
    markdown_lines = []
    
    for line in lines:
        line = line.strip()
        if not line:  # 空行则跳过
            # markdown_lines.append('')
            continue
        
        # 匹配"第xx部分 xxxx"格式，设置为一级标题
        # part_match = re.match(r'^(第\s*\d+\s*部分)\s*(.*)$', line)
        part_match = re.match(r'^第([一二三四五六七八九十百千万]+|[0-9]+)\s*部分\s*(.*)$', line)
        if part_match:
            section, title = part_match.groups()
            print('# ' + section + ' ' + title)
            markdown_lines.append('# ' + section + ' ' + title)
            continue
        
        # 匹配其他章节号和标题
        match = re.match(r'^(第?\d+(?:\.\d+)*\s*章?)\s*(.*?)(?:\s*\d+)?$', line)
        if match:
            section, title = match.groups()
            
            # 计算标题级别
            level = len(section.split('.'))
            
            # 对于"第X章"格式，使用二级标题
            if '章' in section:
                level = 2
            else:
                level += 1  # 其他情况级别+1
            
            # 创建Markdown标题
            markdown_title = '#' * level + ' ' + section + ' ' + title
            markdown_lines.append(markdown_title)
        else:
            # 如果没有匹配，保持原样
            # markdown_lines.append(line)
            markdown_lines.append('#' * 4 + ' ' + line)
    
    return '\n'.join(markdown_lines)

def process_file(input_file, output_file):
    try:
        # 读取输入文件
        with open(input_file, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # 转换内容
        markdown_content = convert_to_markdown(content)
        
        # 写入输出文件
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(markdown_content)
        
        print(f"处理完成。结果已保存到 {output_file}")
    except FileNotFoundError:
        print(f"错误：找不到文件 {input_file}")
    except IOError as e:
        print(f"发生 I/O 错误: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("使用方法: python script.py 输入文件 输出文件")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        process_file(input_file, output_file)

# import re
# import sys

# def convert_to_markdown(text):
#     lines = text.split('\n')
#     markdown_lines = []
    
#     for line in lines:
#         # 匹配章节号和标题
#         line = line.strip()
#         if not line: # 空行则继续。
#             continue
#         match = re.match(r'^(第?\d+(?:\.\d+)*\s*章?)\s*(.*?)(?:\s*\d+)?$', line)
#         if match:
#             section, title = match.groups()
            
#             # 计算标题级别
#             level = len(section.split('.')) + 1
            
#             # 对于"第X章"格式，使用二级标题
#             if '章' in section:
#                 level = 2
            
#             # 创建Markdown标题
#             markdown_title = '#' * level + ' ' + section + ' ' + title
#             markdown_lines.append(markdown_title)
#         else:
#             # 如果没有匹配，保持原样
#             markdown_lines.append('#' * 3 + ' ' + line)
    
#     return '\n'.join(markdown_lines)

# def process_file(input_file, output_file):
#     try:
#         # 读取输入文件
#         with open(input_file, 'r', encoding='utf-8') as file:
#             content = file.read()
        
#         # 转换内容
#         markdown_content = convert_to_markdown(content)
        
#         # 写入输出文件
#         with open(output_file, 'w', encoding='utf-8') as file:
#             file.write(markdown_content)
        
#         print(f"处理完成。结果已保存到 {output_file}")
#     except FileNotFoundError:
#         print(f"错误：找不到文件 {input_file}")
#     except IOError as e:
#         print(f"发生 I/O 错误: {str(e)}")

# if __name__ == "__main__":
#     if len(sys.argv) != 3:
#         print("使用方法: python script.py 输入文件 输出文件")
#     else:
#         input_file = sys.argv[1]
#         output_file = sys.argv[2]
#         process_file(input_file, output_file)

# # import re

# # def convert_to_markdown(text):
# #     lines = text.split('\n')
# #     markdown_lines = []
    
# #     for line in lines:
# #         # 匹配章节号和标题
# #         match = re.match(r'^(第?\d+(?:\.\d+)*\s*章?)\s*(.*?)(?:\s*\d+)?$', line)
# #         if match:
# #             section, title = match.groups()
            
# #             # 计算标题级别
# #             level = len(section.split('.')) + 1
            
# #             # 对于"第X章"格式，使用二级标题
# #             if '章' in section:
# #                 level = 2
            
# #             # 创建Markdown标题
# #             markdown_title = '#' * level + ' ' + section + ' ' + title
# #             markdown_lines.append(markdown_title)
# #         else:
# #             # 如果没有匹配，保持原样
# #             markdown_lines.append(line)
    
# #     return '\n'.join(markdown_lines)

# # # 测试
# # text = """第1章　计算机网络和因特网1
# # 1.1　什么是因特网1
# # 1.1.1　具体构成描述1
# # 1.1.2　服务描述4
# # 1.1.3　什么是协议5
# # 1.2　网络边缘6
# # 1.2.1　接入网8
# # 1.2.2　物理媒介13
# # 1.3　网络核心15
# # 1.3.1　分组交换15
# # 1.3.2　电路交换18
# # 1.3.3　网络的网络21
# # 1.4　分组交换网中的时延、丢包和吞吐量24
# # 1.4.1　分组交换网中的时延24
# # 1.4.2　排队时延和丢包26
# # 1.4.3　端到端时延28
# # 1.4.4　计算机网络中的吞吐量29"""

# # print(convert_to_markdown(text))