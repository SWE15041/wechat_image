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
    target_url = "https://mp.weixin.qq.com/s?src=11&timestamp=1641348173&ver=3539&signature=OdFTLT-dcR3tkPsPJeSfwIJ5Pqv8w8Ru-EcBL*NahL8m4enbzZlmDXRSwZX-mtlFaKB61VIRbZ*LMgPB0zdhuLvzQv5gQ3wPnms-pUrWwJ4*9D4a822Sd*6qFlr8zQA9&new=1"
    # 本地存放目录
    img_dir = "/Users/yannilan/workspace/swe15041/BQB/吴京中国"
    # 要爬的url正则
    # pattern = 'data-src=\"https:\S{1,}.?wx_fmt=[jpeg|gif|png]+\"'
    pattern = 'data-src=\"https:\S{1,}\"'
    if not os.path.exists(img_dir):
        os.mkdir(img_dir)
    # 下载图片
    prefix = "吴京中国_"
    download_img(target_url, img_dir, pattern, prefix)
