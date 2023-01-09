# -*- coding:utf-8 -*-
# @FileName  :cve_finder.py
# @Time      :2022/8/8 13:45
# @Author    :noculture

import sys
import threading

import  requests
import  time
import json
from colorama import init, Fore
from plugin import fanyi, header_random,cve_to_excel,banner


class cveItem(object):
    cve_id = None #cve编号
    cve_description = None #cve漏洞详情
    cve_translate =None #翻译漏洞详情
    cve_link = None #cve链接
    cve_affect=None  #获取供应商、产品和版本

class search_cve():

    #构造方法
    def __init__(self,cvet_txt_path,filename):
        self.url ="https://www.cve.org/api/?action=getCveById&cveId="
        self.text=cvet_txt_path
        self.filename=filename
        self.cve_items=[]
        self.cve_list=[]
        init(autoreset=True)

    #将文本中的cve编号进行提取
    def  Text_to_list(self):
        try:
            with open(self.text,'r',encoding='utf-8') as f:
                totalines=f.readlines()

                for line in totalines:
                    if line == '\n':
                        pass
                    else:
                        temp1=line.strip('\n')
                        self.cve_list.append(temp1)
            if len(self.cve_list)>0:
                return True
            else:
                print(Fore.BLUE+self.text+'文本中没有cve编号')
                return False
        except:
            print(Fore.RED+"error！请确认cve_txt路径是否正确")
            return False

    #多线程处理数据
    def chuli(self,j):
        jsons=self.crwaler_cve(j)
        self.chuli_data(jsons, self.cve_list[j])


    def duoxian(self):


        if self.Text_to_list() == True:
            print(Fore.GREEN + "开始爬取数据：")
            thread=[]
            try:
                for i in range(len(self.cve_list)):
                    t=threading.Thread(target=self.chuli,args=(i,))
                    t.start()
                    thread.append(t)
                for j in range(len(self.cve_list)):
                    time.sleep(0.1)
                    thread[j].join()
                    if j == len(self.cve_list):
                        process = "\r[%2s/%3s]\n" % (j+1,len(self.cve_list))
                    else:
                        process = "\r[%2s/%3s]" % (j+1,len(self.cve_list))
                    print(process, end='', flush=True)
                print('\n')
                #print(self.cve_items[0].cve_id)
                cve_to_excel.cve_to_excel(self.cve_items,self.filename,self.cve_list)
                print(Fore.GREEN + '查询完成！')


            except Exception as e:
                print(e)
        else:
            print()

    #根据cve编号爬取信息
    def crwaler_cve(self,j):

            try:
                        header = {
                            "User-Agent": header_random.random_header()
                        }
                        try:
                            response=requests.get(url=self.url+self.cve_list[j],headers=header,verify=True,timeout=6)
                            response.close()
                            return response.json()

                        except requests.exceptions.RequestException:
                            try:
                                response = requests.get(url=self.url + self.cve_list[j], headers=header, verify=True, timeout=6)
                                response.close()
                                return response.json()

                            except requests.exceptions.RequestException:
                                html2='''{"description":{"description_data":[{"value":"连接超时，请尝试手工查询"}]}}'''
                                jsons = json.loads(html2)
                                return jsons

            except Exception as e:
                print(e)

    def chuli_data(self,jsons,cve_id):
        #解决list.append覆盖问题
        item = cveItem()
        #写入cve编号
        #print(''.join(cve_id))
        item.cve_id = ''.join(cve_id)

        #获取cve描述
        try:
            item.cve_description =jsons['containers']['cna']['descriptions'][0].get('value')
        except Exception as e:
            try:
                item.cve_description = jsons.get("message")
            except:
                item.cve_description = "CVE-YYYY-NNNN,YYYY  must be a year starting from 1999. NNNN is must be 4 digits or greater"
            #print(e)

        #翻译
        try:
            item.cve_translate= fanyi.fanyi.fy(item.cve_description)
        except:
            item.cve_translate='请手工翻译'

        #获取产品和影响版本
        try:
            #处理json数据
            name=jsons['containers']['cna']['affected'][0]['versions']
            #定义产品名称
            product_name = []
            product_name.append(jsons['containers']['cna']['affected'][0].get('product'))
            #受影响版本
            affect_version=[]
            cve_affect=''
            #通过产品名称出发点，寻找受影响版本
            # for l in range(len(name)):
                # for i in name:
                    # if len(name) >= 1:
                        # product_name.append(i.get('product_name'))
                        # for j in i['version']['version_data']:
                            # if 'version_affected' in j:
                                # affect_version[l].append(j.get('version_affected') + j.get('version_value'))
                            # else:
                                # affect_version[l].append(j.get('version_value'))
            for	i in name:
               if len(name) >= 1:
                        if 'affected' in i:
                            affect_version.append(i.get('version') + i.get('status'))
                        else:
                            affect_version.append(i.get('version'))
            cve_affect = cve_affect + "产品名称：{}\n影响产品版本：\n{}\n".format(product_name[0], ('\n'.join(affect_version)))

								
            # for k in range(len(name)):
                # cve_affect = cve_affect + "产品名称：{}\n影响产品版本：\n{}\n".format(product_name[k], ('\n'.join(affect_version[k])))

            item.cve_affect=cve_affect
        except Exception as e:
             print(e)
             item.cve_affect = '空'
        # 链接：
        try:
            item.cve_link = "https://www.cve.org/CVERecord?id="+item.cve_id
        except:
            item.cve_link ="空"
        self.cve_items.append(item)


if __name__ == '__main__':
    if len(sys.argv)==3:
        time_start=time.time()
        run=search_cve(sys.argv[1], sys.argv[2])
        # run = search_cve('E:\cola\cve_finder\finder\cve.txt', '工行排查')
        banner.banner()
        run.duoxian()
        time_end=time.time()

        print(Fore.YELLOW+"%2s:%.1fs" % ("本次查询花费时间",time_end-time_start))

    else:
        banner.banner()


