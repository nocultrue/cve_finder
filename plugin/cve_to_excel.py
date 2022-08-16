# -*- coding:utf-8 -*-
# @FileName  :cve_to_excel.py
# @Time      :2022/8/8 13:45
# @Author    :noculture

import time,xlwt
from colorama import init, Fore
from cve_finder import cveItem
# 爬取到的漏洞信息转换为excel
def cve_to_excel(cve_items,name,cve_list):
        print(Fore.GREEN+'开始保存数据:')

        # 创建一个样式对象，初始化样式 style
        cve_style = xlwt.XFStyle()
        # 设置字体格式
        font=xlwt.Font()
        font.name = 'Calibri'  # 设置字体
        font.height = 248 # 字体大小
        cve_style.font=font
        #设置字体位置
        alignment = xlwt.Alignment()
        alignment.vert = 0x00  #vert设置水平距离0x00左端对齐
        alignment.horz = 0x01  #
        alignment.wrap = 1 #自动换行
        cve_style.alignment=alignment

        now = time.strftime('%Y-%m-%d-%H-%M', time.localtime())
        filename = name+'-'+now+'.xls'
        book = xlwt.Workbook(encoding='utf-8', style_compression=0)
        sheet = book.add_sheet('cve官网查询结果')

        #设置第一列（1）列宽
        col=sheet.col(0)
        col.width=8888
        # 设置第二列（2）列宽
        col = sheet.col(1)
        col.width = 15000
        # 设置第三列（3）列宽
        col = sheet.col(2)
        col.width = 15000
        # 设置第四列（4）列宽
        col = sheet.col(3)
        col.width = 12000
        # 设置第五列（5）列宽
        col = sheet.col(4)
        col.width = 15000
        # 设置第五列（5）列宽
        col = sheet.col(5)
        col.width = 15000

        #提示信息
        info_style = xlwt.easyxf('pattern: pattern solid, fore_colour ice_blue')
        font = xlwt.Font()
        font.name = 'Calibri'  # 设置字体
        font.height = 270  # 字体大小
        info_style.font = font
        info_style.alignment = alignment
        sheet.write(1,5,"1.翻译结果仅仅参考！谨慎阅读\n2.若cve报不存在，尝试sxf、qax等漏洞情报处手工查询",info_style)
        # 添加标题
        item = cveItem()
        item.cve_id = 'cve_ID'
        item.cve_description = 'cve漏洞详细'
        item.cve_translate = '有道翻译cve漏洞详情'
        item.cve_affect = '产品及影响版本'
        item.cve_link = "cve漏洞地址"
        cve_items.append(item)

        #排序
        i=0
        j=1
        n = len(cve_list)
        for i in range(n):
                # j控制item_list
                for j in range(n + 1):
                        if (cve_list[i] == cve_items[j].cve_id):
                                # list.append(item_list[j])
                                temp = cve_items[j]
                                cve_items[j] = cve_items[i + 1]
                                cve_items[i + 1] = temp
                        j = j + 1
                i = i + 1



        # 写入文件
        i = 0
        while i < len(cve_items):
            item = cve_items[i]

            sheet.write(i, 0, item.cve_id,cve_style)
            sheet.write(i, 1, item.cve_description,cve_style)
            sheet.write(i, 2, item.cve_translate, cve_style)
            sheet.write(i, 3, item.cve_affect,cve_style)
            sheet.write(i, 4, item.cve_link, cve_style)

            i = i + 1
        try:
                book.save("./result/"+filename)
                print(Fore.GREEN+"保存结果："+"./result/"+filename)
        except:
                print(Fore.RED+"保存失败")


if __name__ == '__main__':
        cve_to_excel()