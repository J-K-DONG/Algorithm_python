#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/8 0:05
# @Author  : JK_DONG
# @Site    : 
# @File    : analysis_2.py
# @Software: PyCharm

keywords = ['', 'begin', 'end']
symbols = ['+', '-', '*', '/', ';', ':=', '(', ')'] # 13


def scanner(string_temp):
    str = string_temp
    str += ' '
    cur_str = ''
    cur_idx = 0
    syn_list = []
    toke_list = []
    while cur_idx != -1:
        if cur_idx == len(str):
            str = input()
            cur_idx = 0
            str += ''

        cur_str = ''
        syn = -1

        while(str[cur_idx] == ' ' or str[cur_idx] == '\n'):
            cur_idx += 1
            if cur_idx == len(str):
                break

        if(cur_idx == len(str)):
            continue

        if(str[cur_idx].isalpha()):
            while(str[cur_idx].isalnum()):
                cur_str += str[cur_idx]
                cur_idx += 1

            for idx in range(len(keywords)):
                if cur_str == keywords[idx]:
                    syn = idx
                    break
            if(syn == -1):
                syn = 10

            syn_list.append(syn)
            toke_list.append(cur_str)

        elif(str[cur_idx].isdigit()):
            while(str[cur_idx].isdigit()):
                cur_str += str[cur_idx]
                cur_idx += 1
            syn = 11
            syn_list.append(syn)
            toke_list.append(cur_str)

        else:
            if cur_idx + 1 < len(str):
                cur_str = str[cur_idx] + str[cur_idx + 1]
                for idx in range(len(symbols)):
                    if cur_str == symbols[idx]:
                        syn = 13 + idx
                        cur_idx += 2
                        break

            if syn == -1:
                cur_str = str[cur_idx]
                for idx in range(len(symbols)):
                    if cur_str == symbols[idx]:
                        syn = 13 + idx
                        cur_idx += 1
                        break

            if syn == -1:
                if str[cur_idx] == '#':
                    syn = 0
                    cur_str = '#'
                    cur_idx = -1
                else:
                    print("Error")
                    exit(0)
            syn_list.append(syn)
            toke_list.append(cur_str)

    return syn_list, toke_list

def check_word_string(word_string):
    left_idx = 0
    all_right = True
    word_string.append(17)
    cur_idx = 0

    while cur_idx < len(word_string):
        if word_string[cur_idx] == 19:
            if cur_idx != left_idx:
                return False

            left_counter = 1
            right_counter = 0
            temp_idx = cur_idx + 1
            while left_counter != right_counter:
                if temp_idx == len(word_string):
                    return False
                if word_string[temp_idx] == '19':
                    left_counter += 1
                elif word_string[temp_idx] == '20':
                    right_counter += 1
                temp_idx += 1
            all_right = check_word_string(word_string[left_idx+1:temp_idx-1])
            if all_right == False:
                break
            cur_idx = left_idx = temp_idx
            continue

        elif word_string[cur_idx] == 17:
            all_right = check_word(word_string[left_idx:cur_idx])
            if all_right == False:
                break
            left_idx = cur_idx + 1
        cur_idx = cur_idx + 1
    return all_right


def check_word(word):
    if len(word) < 3 or word[0] != 10 or word[1] != 18:
        return False
    return check_expression(word[2:])


def check_expression(expression):
    left_idx = 0
    all_right = True
    expression.append(13)
    if len(expression) < 1:
        return False

    for cur_idx in range(len(expression)):
        if expression[cur_idx] == 13 or expression[cur_idx] == 14:
            all_right = check_term(expression[left_idx:cur_idx])
            if all_right == False:
                break
            left_idx = cur_idx + 1
    return all_right


def check_term(term):
    left_idx = 0
    all_right = True
    term.append(15)
    if len(term) < 1:
        return False

    for cur_idx in range(len(term)):
        if term[cur_idx] == 15 or term[cur_idx] == 16:
            all_right = check_factor(term[left_idx:cur_idx])
            if all_right == False:
                break
            left_idx = cur_idx + 1
    return all_right


def check_factor(factor):
    if len(factor) != 1:
        return False
    if factor[0] == 10 or factor[0] == 11:
        return True
    else:
        return False


def main():
    str = input("Enter your input: ")
    all_right = True
    syn_list, toke_list = scanner(str)

    if (syn_list[0] != 1) or (syn_list[-1] != 0) or (syn_list[-2] != 2):
        all_right = False

    if all_right:
        all_right = check_word_string(syn_list[1:-2])

    if all_right:
        print('success!')
    else:
        print('error')


if __name__ == '__main__':
    main()