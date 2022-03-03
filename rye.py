import requests
from bs4 import BeautifulSoup
import xlwt

# 请求headers 模拟谷歌浏览器访问
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
}

'''
import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/75.0.3770.100 Safari/537.36",
}

res = requests.get('http://www.eeo.com.cn/yaowen/',headers = headers)
response = bytes(res.text,res.encoding).decode('utf-8','ignore')
print(response)
'''


# 定义一个函数用于抓取网页内容，并处理
def get_data():
    response = requests.get('http://www.hs-bianma.com/hs_chapter_01.htm', headers=headers)
    # bs = BeautifulSoup(response.text, 'lxml')
    # res = requests.get('http://www.eeo.com.cn/yaowen/', headers=headers)
    bs = bytes(response.text, requests.encoding).decode('utf-8', 'ignore')
    return bs

    # 标题处理
    title = bs.find_all('th')  # 寻找所有的内容
    data_list_title = []  # 定义一个空列表
    for data in title:
        data_list_title.append(data.text.strip())  # 获取标签的内容去掉两边空格并添加到列表里

    # 内容处理
    content = bs.find_all('td')
    data_list_content = []  # 定义一个空列表
    for data in content:
        data_list_content.append(data.text.strip())  # 获取标签的内容去掉两边空格并添加到列表里
    # 语句featList = [example[i] for example in dataSet]作用为： 将dataSet中的数据按行依次放入example中，然后取得example中的example[i]元素，放入列表featList中
    new_list = [data_list_content[i:i + 16] for i in range(0, len(data_list_content), 16)]

    # 存入excel表格
    book = xlwt.Workbook()
    sheet1 = book.add_sheet('sheet1', cell_overwrite_ok=True)

    # 标题存入
    heads = data_list_title[:]  # 将data_list_title第一位到最后一位赋值给heads
    ii = 0
    for head in heads:
        sheet1.write(0, ii, head)
        ii += 1

    # 内容录入
    i = 1
    for list in new_list:
        j = 0
        for data in list:
            sheet1.write(i, j, data)
            j += 1
        i += 1
    # 文件保存
    book.save('./data.xls')


print("全部完成")


if __name__ == '__main__':
    get_data()