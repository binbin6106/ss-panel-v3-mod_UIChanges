import json
from ShowapiRequest import ShowapiRequest
import time
import requests


def getoilprice():
    showapi_appid = '96301'
    showapi_sign = 'af5c7c34b82c43b4902eaf2aa70297e3'
    # prov:
    url = 'http://route.showapi.com/138-46'
    content = {}
    r = ShowapiRequest(url, showapi_appid, showapi_sign)
    r.addBodyPara("prov", "山东")
    # r.addFilePara("img", r"C:\Users\showa\Desktop\使用过的\4.png") #文件上传时设置
    res = r.post()
    # print(res.text) # 返回信息
    restr = json.loads(res.text)
    ri = time.strftime("%d", time.localtime())
    p92 = restr['showapi_res_body']['list'][0]['p92']
    p95 = restr['showapi_res_body']['list'][0]['p95']
    p98 = restr['showapi_res_body']['list'][0]['p98']
    p0 = restr['showapi_res_body']['list'][0]['p0']
    text = "#### 山东" + ri + "日油价\n- 92号汽油：" + p92 + "元\n- 95号汽油：" + p95 + "元\n- 98号汽油：" + p98 + \
           "元\n- 0号柴油：" + p0 + "元\n##### 本工具作者:binbin6106,运行于家里的基于ESXI的Fedora系统上"
    content = {'text': text, 'p92': p92}
    return content


def serverpush(text):
    url = 'https://sc.ftqq.com/SCU37292T4696a7b5cb4db8bc991944c1f13b7d485c0bb92524731.send'
    urlchenyang = 'https://sc.ftqq.com/SCU52362T441a5e86203df6e131a41315d35986cc5cebc8dc8a13f.send'

    textmod = {'text': '油价发生了变化', 'desp': text}
    requests.post(url, params=textmod)
    time.sleep(1)
    requests.post(urlchenyang, params=textmod)
    # print(req.text)


def priceischange(p92):
    with open("lastprice.txt", "r") as f:
        lastp92 = f.read()
    if lastp92 != p92:
        with open("lastprice.txt", "w") as f1:
            f1.write(p92)
        return True
    else:
        print("no update")
        return False


def main():

    content = getoilprice()
    if priceischange(content['p92']):
        serverpush(content['text'])


if __name__ == '__main__':
    main()
