# _*_ coding: utf-8 _*_
import random
import requests
from bs4 import BeautifulSoup

with open('user-agent.txt') as f:
    lines = f.readlines()
    USER_AGENTS = [l.strip() for l in lines]

PROXY_IP_LIST = None
SELECT_FROM_CACHE_COUNT = 0

def get_ip_list(url, headers):
    web_data = requests.get(url, headers=headers)
    # 第一个参数是要匹配的内容
    # 第二个参数是beautifulsoup要采用的模块，即规则
    soup = BeautifulSoup(web_data.text, 'lxml')
    ips = soup.find_all('tr')    # 字符串过滤
    ip_list = []

    for i in range(1, len(ips)):
        ip_info = ips[i]
        tds = ip_info.find_all('td')
        ip_list.append(tds[1].text + ':' + tds[2].text)

    return ip_list


def get_random_ip(ip_list):
    proxy_list = []
    for ip in ip_list:
        proxy_list.append('http://' + ip)

    return {'http': random.choice(proxy_list)}


def get_random_user_agent_and_proxies():
    """
    获取代理 ip 和 user agent
    """
    global PROXY_IP_LIST, SELECT_FROM_CACHE_COUNT

    user_agent = random.choice(USER_AGENTS)

    ip_base_url = 'https://www.xicidaili.com/nn'
    headers = {
        'User-Agent': user_agent
    }

    if PROXY_IP_LIST is None:
        ip_list = get_ip_list(ip_base_url, headers)
        PROXY_IP_LIST = ip_list
    else:
        ip_list = PROXY_IP_LIST
        SELECT_FROM_CACHE_COUNT += 1

    if SELECT_FROM_CACHE_COUNT > len(PROXY_IP_LIST) / 4 * 3:
        PROXY_IP_LIST = None

    proxies = get_random_ip(ip_list)
    return user_agent, proxies


def get_random_user_agent():
    user_agent = random.choice(USER_AGENTS)
    return user_agent
