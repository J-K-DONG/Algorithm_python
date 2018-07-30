#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/7 10:24
# @Author  : JK_DONG
# @Site    :
# @File    : codinganalysis.py
# @Software: PyCharm

import string

# 各种单词符号对应的种别码各种单词符号对应的种别码
keywords = {'begin': 1, 'if': 2, 'then': 3, 'while': 4, 'do': 5, 'end': 6,
            '+': 13, '-': 14, '*': 15, '/': 16, ':': 17, ':=': 18, '<': 20,
            '<>': 21, '<=': 22, '>': 23, '>=': 24, '=': 25, ';': 26, '(': 27,
            ')': 28, '#': 0}


signlist = {}


# 预处理函数，将源代码文件中的空格，换行等无关字符同意转换成空格字符，输出到中间代码文件中
def pretreatment(f_in, f_out):
    try:
        with open(f_in, 'r') as fp_in, open(f_out, 'w') as fp_out:       # 上下文管理器规范程序
            sign = 0
            for line in fp_in:      # 分行扫描字符串
                if not line:
                    break
                length = len(line)
                i = -1
                while i < length - 1:     # 从第一个字符串开始扫描
                    i += 1
                    if sign == 0:
                        if line[i] == ' ':
                            continue
                    if line[i] == '#':      # 每一行的结束符
                        break
                    elif line[i] == ' ':
                        if sign == 1:
                            continue
                        else:
                            sign = 1
                            fp_out.write(' ')
                    elif line[i] == '\t':
                        if sign == 1:
                            continue
                        else:
                            sign = 1
                            fp_out.write(' ')
                    elif line[i] == '\n':
                        if sign == 1:
                            continue
                        else:
                            fp_out.write(' ')
                            sign = 1
                    else:       # 其他符号或单词
                        sign = 3
                        fp_out.write(line[i])
    except FileNotFoundError:
        print(f_in, ': This FileName Not Found!')


def code_out(string):
    if string in keywords.keys():
        print('(', keywords[string], ',', string, ')')      # 输出字典中的键值对
    else:
        try:        # 捕获未在字典中定义的字符串异常
            float(string)
            code_out_const(string)      # 保存数字字符串
        except ValueError:
            code_out_var(string)        # 保存变量字符串


def code_out_var(string):
    if len(string.strip()) < 1:
        pass
    else:
        if is_signal(string) == 1:                  # 判断是不是自定义标识符
            print('(', 10, ',', string, ')')

        else:                                       # 未定义的字符串
            print('(', -1, ',', string, ')')


def code_out_const(string):
    if len(string.strip()) < 1:
        pass
    else:
        str_temp = string.strip()
        print('(', 11, ',', str_temp, ')')


def is_signal(s):
    if s[0] == '_' or s[0] in string.ascii_letters:         # 标识符以字母或下划线开头 不能以数字开头
        for i in s:
            if i in string.ascii_letters or i == '_' or i in string.digits:
                pass
            else:
                return 0
        return 1
    else:
        return 0


def recognition(filename):
    try:
        fp_read = open(filename, 'r')
        string = ""
        sign = 0
        while True:
            code_signal = fp_read.read(1)
            if not code_signal:         # 空文件则退出
                break
            if sign == 2:
                if code_signal == '=' or code_signal == '>':
                    string += code_signal
                    code_out(string)
                    sign = 0
                    string = ""
                    continue
                else:
                    code_out(string)
                    sign = 0
                    string = ""
                    string += code_signal
            else:
                if code_signal == ' ':
                    if len(string.strip()) < 1:
                        sign = 0
                        pass
                    else:
                        if sign == 1 or sign == 2:
                            string += code_signal
                        else:
                            code_out(string)
                            string = ""
                            sign = 0
                elif code_signal == '+':
                    code_out(string)
                    string = ""
                    code_out('+')
                elif code_signal == '-':
                    code_out(string)
                    string = ""
                    code_out('-')
                elif code_signal == '*':
                    code_out(string)
                    string = ""
                    code_out('*')
                elif code_signal == '/':
                    code_out(string)
                    string = ""
                    code_out('/')
                elif code_signal == ':':
                    code_out(string)
                    string = ""
                    string += code_signal
                    sign = 2
                elif code_signal == '<':
                    code_out(string)
                    string = ""
                    string += code_signal
                    sign = 2
                elif code_signal == '>':
                    code_out(string)
                    string = ""
                    string += code_signal
                    sign = 2
                elif code_signal == '=':
                    code_out(string)
                    string = ""
                    string += code_signal
                    code_out('=')
                elif code_signal == '(':
                    if sign == 1 or sign == 2:
                        string += code_signal
                    else:
                        code_out(string)
                        string = ""
                        code_out('(')
                elif code_signal == ')':
                    if sign == 1 or sign == 2:
                        string += code_signal
                    else:
                        code_out(string)
                        string = ""
                        code_out(')')
                elif code_signal == ';':
                    code_out(string)
                    string = ""
                    code_out(';')
                else:
                    string += code_signal
    except Exception as e:
        print(e)


def main():
    pretreatment('code_in', 'code_mid')
    recognition('code_mid')


if __name__ == '__main__':
    main()
