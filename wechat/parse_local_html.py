# 请求网页
import requests
import re
import os

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36'
}


def download_img(parsedFilename, img_dir, pattern, prefix):
    html = open(parsedFilename, "r", encoding="utf-8").read()
    # 解析网页
    results = re.findall(pattern, html)
    count = 0
    for result in results:
        url = result.split('\"')[1].split("?")[0]
        # suffix = "gif"
        # suffix = url.split('=')[-1]
        suffix = "jpg"
        filename = prefix + str(count) + "." + suffix
        response = requests.get(url, headers=headers)
        with open(img_dir + '/' + filename, 'wb') as f:
            # 写入获取的数据
            f.write(response.content)
        print(url)
        count = count + 1


if __name__ == '__main__':
    # 本地存放目录
    img_dir = "/Users/yannilan/workspace/swe15041/BQB/猫"
    if not os.path.exists(img_dir):
        os.mkdir(img_dir)
    # 下载图片名前缀
    prefix = "猫1_"
    # 被解析的文件
    parsedFilename = "./local.html"
    # 要爬的url正则
    pattern = '<img src=\"https:\S{1,}\"'
    #
    download_img(parsedFilename, img_dir, pattern, prefix)
