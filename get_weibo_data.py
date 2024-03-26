# -*- coding: utf-8 -*-
#
# 调用 weibo API 获取微博数据
#

import argparse
import datetime
import requests


# 获取微博数据, 根据 page 获取
def get_weibo_data(page, uid, cookie):
    if uid is None:
        raise Exception("uid is None")
    url = "https://weibo.com/ajax/statuses/mymblog?uid={}&page={}&feature=0".format(
        uid, page)
    headers = {
        "Content-Type": "application/json;charset=UTF-8",
        "Cookie": cookie,
    }
    response = requests.get(url, headers=headers)
    return response.json()


# 获取长微博数据, 根据 mid 获取
def get_long_weibo_data(mid, cookie):
    url = "https://weibo.com/ajax/statuses/longtext?id={}".format(mid)
    headers = {
        "Content-Type": "application/json;charset=UTF-8",
        "Cookie": cookie,
    }
    response = requests.get(url, headers=headers)
    return response.json()


# 格式化文本
def align_text(text):
    # 将文本按行分割成一个列表
    lines = text.split('\n')
    # 过滤掉空行
    non_empty_lines = [line for line in lines if line.strip()]
    # 将非空行重新组合成一个字符串
    result = '\n'.join(non_empty_lines)
    return result


def convert_time_string(time_string):
    # 将时间字符串解析为 datetime 对象
    time_obj = datetime.datetime.strptime(
        time_string, "%a %b %d %H:%M:%S %z %Y")

    # 将 datetime 对象的日期部分格式化为指定格式的字符串
    return time_obj.strftime("%Y.%m.%d")


def main():
    parser = argparse.ArgumentParser()

    # year
    parser.add_argument("-y", "--year", type=str, default=2024, help="年份")
    # uid: default is mine
    parser.add_argument("-u", "--uid", type=str,
                        default=7680559239, help="微博 uid")
    # cookie: default is empty
    parser.add_argument("-c", "--cookie", type=str,
                        default="", help="微博 cookie")
    args = parser.parse_args()
    year = args.year
    uid = args.uid
    cookie = args.cookie

    # 输出列表
    output = []

    # 获取总页数
    data = get_weibo_data(1, uid, cookie)
    total = data.get("data")["total"]
    page = total // 20 + 1

    # 获取所有微博数据
    for i in range(1, page + 1):
        data = get_weibo_data(i, uid, cookie)
        for j in data.get("data")["list"]:
            # 过滤年份
            if j["created_at"].find(str(year)) == -1:
                # 如果年份不匹配, 跳出循环, 不再获取数据
                break

            # 获取微博创建时间
            created_at = convert_time_string(j["created_at"])
            output.append("// " + created_at)

            # 获取微博文本
            text = j["text_raw"]
            # 如果文本过长, 获取长微博数据
            if "isLongText" not in j:
                print("isLongText not found: ", text)
            if "isLongText" in j and j["isLongText"]:
                long_data = get_long_weibo_data(j["mblogid"], cookie)
                text = long_data.get("data").get("longTextContent")

            # 格式化文本
            text = align_text(text)

            # 添加到输出列表
            output.append(text + "\n")

    # 写入文件
    file_name = "weibo_{}.txt".format(year)
    with open(file_name, "w") as f:
        f.write("\n".join(output))


if __name__ == '__main__':
    main()
