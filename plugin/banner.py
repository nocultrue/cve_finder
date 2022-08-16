# -*- coding:utf-8 -*-
# @FileName  :banner.py
# @Time      :2022/8/8 14:09
# @Author    :noculture
from colorama import init, Fore

def banner():
    init(autoreset=True)
    for i in range(2):
        print(Fore.CYAN + ' ' * 20 + '=============================================================')
    print(Fore.CYAN + ' '* 30 + "简介：通过cve编号进行查询漏洞描述信息 v1.0")
    print(Fore.CYAN + ' '* 30 + "查询网站：https://www.cve.org/")
    print(Fore.CYAN+ ' '* 30+"Usage : python3 cve_finder.py c:\cve.txt 输出文件名前缀")
    print(Fore.CYAN + ' ' * 30 + "输出 :  ./result/文件名-时间")
    for i in range(2):
        print(Fore.CYAN + ' ' * 20 + '=============================================================')