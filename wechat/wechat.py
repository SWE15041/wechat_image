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
    target_url = "https://mp.weixin.qq.com/s?__biz=MzUxNjkyNjU4OA==&mid=2247487183&idx=1&sn=d2f82fbe498920e5d372aeb285cbd70e&chksm=f99eb3dccee93aca538ad49aebf9b888db035e730123f48a91f652ac880899d4ae8ed33e74ee&token=669374865&lang=zh_CN#rd"
    # 本地存放目录
    img_dir = "/Users/yanni/workspace/lyn/BQB/植物0221"
    # 要爬的url正则
    pattern = 'data-src=\"https:\S{1,}.?wx_fmt=[jpeg|gif|png]+'
    # pattern = 'data-src=\"https:\S{1,}\"'
    if not os.path.exists(img_dir):
        os.mkdir(img_dir)
    # 下载图片
    prefix = "植物_1_"
    download_img(target_url, img_dir, pattern, prefix)
