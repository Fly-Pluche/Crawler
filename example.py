import json
import requests

if __name__ == '__main__':
    import time

    time_tuple = time.localtime(time.time())
    print("当前时间为{}年{}月{}日{}点{}分{}秒".format(time_tuple[0], time_tuple[1], time_tuple[2], time_tuple[3], time_tuple[4],
                                           time_tuple[5]))
    # url = "https://fanyi.baidu.com/sug"
    #
    # headers = {
    #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36 Edg/98.0.1108.43"
    # }
    #
    # data = {
    #     'kw': 'word'
    # }
    #
    # proxy = {
    #     "https": "http://127.0.0.1:4780"
    # }
    #
    # response = requests.post(url=url, data=data, headers=headers, proxies=proxy)
    # dic = response.json()
    #
    # tf = open('2019-nCoV/word.json', 'w', encoding='utf-8')
    # json.dump(dic, fp=tf, ensure_ascii=False)
    # # tf.write(response.text)
    # print('over')
