# 请求网页
import requests
import re
import os


def download_img(target_url, img_dir, pattern, prefix):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36'
    }

    response = requests.get(target_url, headers=headers)

    # print(response.request.headers)
    # print(response.text)
    html = response.text
    # 解析网页
    # pattern = 'data-src=\"https:\S{1,}.?wx_fmt=[jpeg|gif|png]+\"'
    results = re.findall(pattern, html)
    count = 0
    for result in results:
        url = result.split('\"')[1]
        # suffix = "gif"
        suffix = url.split('=')[-1]
        filename = prefix + str(count) + "." + suffix
        response = requests.get(url, headers=headers)
        with open(img_dir + '/' + filename, 'wb') as f:
            # 写入获取的数据
            f.write(response.content)
        print(url)
        count = count + 1


if __name__ == '__main__':
    # 要爬取的网页
    target_url = "https://mp.weixin.qq.com/s?src=11&timestamp=1645682930&ver=3639&signature=zkAHBZ0ujQt2DaUoHJz*bID9XH1pgbdeh66udkFtp7F951TQu9KaYo2njMCLN355QfAuEFa6ZlPRoUgaps*VxfVne1KNRkTc6YbsFtYkOXufh4cBN-OqdiBT3Jb4qPGx&new=1"
    # 本地存放目录
    img_dir = "/Users/yannilan/workspace/swe15041/BQB/纸团套路0224"
    # 要爬的url正则
    pattern = 'data-src=\"https:\S{1,}.?wx_fmt=[jpeg|gif|png]+'
    # pattern = 'data-src=\"https:\S{1,}\"'
    if not os.path.exists(img_dir):
        os.mkdir(img_dir)
    # 下载图片
    prefix = "纸团套路0224_2_"
    download_img(target_url, img_dir, pattern, prefix)
