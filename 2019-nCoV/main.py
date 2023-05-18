# 导入模块
import time
import pandas as pd
from lxml import etree
# 读取html文件信息（在真实代码中是爬取的网页信息）

# url = 'http://m.bj.bendibao.com/news/gelizhengce/fengxianmingdan.php'
# # headers = {
# #     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1326.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63010200)'}
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36 Edg/98.0.1108.43"
# }

# res = requests.get(url, headers=headers)
# res.encoding = 'utf-8'
# html = etree.HTML(res.text)

f = open("./1.html",'r',encoding="utf-8")
content = f.read()
f.close()
# 解析HTML文档，返回根节点对象
html = etree.HTML(content)

info_total=[]

def get_info(info_index):
    content = html.xpath(f'/html/body/div[1]/div[2]/div[5]/div[{info_index}]//ul/li//text()')
    global info_total
    info_list = []
    for cont in content:
        if '\n' in cont:
            continue
        info_total.append(cont)
        info_list.append(cont)
    return len(info_list)

if __name__ == '__main__':

    label_list = []
    info_dict = ['高风险','中风险','低风险','今日调高','今日调中','今日调低']

    for i in range(1,7):
        num = get_info(i)
        for j in range(num):
            label_list.append(info_dict[i-1])

    save_dict = {
        '地区':info_total,
        '风险等级':label_list
    }
    pd = pd.DataFrame(save_dict)
    day_time = time.localtime(time.time())
    name = f'save/{day_time[1]}月{day_time[2]}日全国疫情等级查询.xlsx'
    # pd.to_csv(name,encoding='utf-8')
    pd.to_excel(name,encoding='gbk')


