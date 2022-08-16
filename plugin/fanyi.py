# -*- coding:utf-8 -*-
# @FileName  :fanyi.py
# @Time      :2022/8/8 13:45
# @Author    :noculture

from urllib import request, parse
import json

class fanyi():
    # 有道翻译：中文→英文
    def fy(i):
        req_url = 'http://fanyi.youdao.com/translate'  # 创建连接接口
        # 创建要提交的数据
        Form_Date = {}
        Form_Date['i'] = i
        Form_Date['doctype'] = 'json'
        Form_Date['form'] = 'AUTO'
        Form_Date['to'] = 'AUTO'
        Form_Date['smartresult'] = 'dict'
        Form_Date['client'] = 'fanyideskweb'
        Form_Date['salt'] = '16595997355726'
        Form_Date['sign'] = '528cd727bb6d82d5751324dddbe03da3'
        Form_Date['version'] = '2.1'
        Form_Date['keyform'] = 'fanyi.web'
        Form_Date['action'] = 'FY_BY_REALTIME'
        Form_Date['typoResult'] = 'false'

        data = parse.urlencode(Form_Date).encode('utf-8')  # 数据转换
        response = request.urlopen(req_url, data)  # 提交数据并解析
        html = response.read().decode('utf-8')  # 服务器返回结果读取
        response.close()
        translate_results = json.loads(html)  # 以json格式载入
        try:
            i = 0
            sum = ''
            while True:
                # json格式调取
                sum = sum + translate_results['translateResult'][0][i]['tgt']
                i = i + 1

        except:
            return sum  # 返回结果

if __name__ == '__main__':
    q = "A Command Injection vulnerability exists in the getTopologyHistory service of the Apache Storm 2.x prior to 2.2.1 and Apache Storm 1.x prior to 1.2.4. A specially crafted thrift request to the Nimbus server allows Remote Code Execution (RCE) prior to authentication "
    print(fanyi().fy(q))
