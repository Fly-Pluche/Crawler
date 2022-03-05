import requests
import os
import requests
if __name__ == '__main__':
    url="https://www.sogou.com/"
    response=requests.get(url=url)
    print(response.text)
    with open('info.html', 'w', encoding='utf-8') as tf:
        tf.write(response.text)

    print('over')