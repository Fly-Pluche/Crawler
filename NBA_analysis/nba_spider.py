# _*_ coding: utf-8 _*_
import random
import time
import requests
import json

base_url = 'https://china.nba.cn/stats2/league/playerstats.json?conference=All&country=All&individual=All&locale=zh_CN&pageIndex=0&position=All&qualified=false&season={}&seasonType=4&split=All+Team&statType=points&team=All&total=perGame'

fout = open('nab_player.json', 'w', encoding='utf8')
all_players = []
for season in range(2000, 2022):
    print('抓取 {} 赛季的球员数据...'.format(season))
    url = base_url.format(season)

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3756.400 QQBrowser/10.5.4039.400',      # 告诉浏览器可以接收什么水平的文件
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'max-age=0',
        'cookie': 'cna=5ac59bf8eea548dcb6dca70e36193717; i18next=zh_CN; locale=zh_CN; countryCode=CN; AMCVS_248F210755B762187F000101%40AdobeOrg=1; AMCV_248F210755B762187F000101%40AdobeOrg=-1712354808%7CMCIDTS%7C19116%7CMCMID%7C83724821919951562613917957561124131488%7CMCAAMLH-1652197327%7C11%7CMCAAMB-1652197327%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1651599727s%7CNONE%7CMCSYNCSOP%7C411-19123%7CMCAID%7CNONE%7CvVersion%7C4.3.0; s_cc=true; privacyV2=true; s_gpv=cn%3Astats%3Aplayers%3Amain; s_sq=nbachinaprod%3D%2526pid%253Dcn%25253Astats%25253Aplayers%25253Amain%2526pidt%253D1%2526oid%253Djavascript%25253Avoid%2525280%252529%2526ot%253DA; tp=3766; s_ppv=cn%253Astats%253Aplayers%253Amain%2C16%2C12%2C609',
        'referer': 'https://china.nba.cn/statistics/',
        'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
        'accept': '*/*'
    }    # 模拟浏览器头部信息，向服务器发送消息
    resp = requests.get(url, headers=headers).json()      #作为请求的请求头
    players = resp['payload']['players']
    for player in players:
        player['season'] = season

    all_players.extend(players)

    if len(all_players) % 10 == 0:
        fout.writelines([json.dumps(player, ensure_ascii=False) + '\n' for player in all_players])
        fout.flush()      #刷新内存到文件
        all_players.clear()    #清空数据
    time.sleep(1 + random.random())

if all_players:
    fout.writelines([json.dumps(player, ensure_ascii=False) + '\n' for player in all_players])
    fout.flush()
    all_players.clear()
