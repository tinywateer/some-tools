#!/bin/env python3
# -*- coding: utf-8 -*-

import requests
import argparse
import datetime


# 你的微博 uid, 手动修改
uid = "7680559239"
# cookie 信息, 手动修改
cookies = ""


# 获取微博数据, 根据 page 获取
def get_weibo_data(page):
    url = "https://weibo.com/ajax/statuses/mymblog?uid={}&page={}&feature=0".format(
        uid, page)
    headers = {
        "cookie": cookies
    }
    response = requests.get(url, headers=headers)
    return response.json()


# 获取长微博数据, 根据 mid 获取
def get_long_weibo_data(mid):
    url = "https://weibo.com/ajax/statuses/longtext?id={}".format(mid)
    headers = {
        "cookie": cookies
    }
    response = requests.get(url, headers=headers)
    return response.json()


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

    parser.add_argument("-y", "--year", type=str, default=2021, help="过滤年份")
    args = parser.parse_args()
    year = args.year

    # 获取总页数
    result = get_weibo_data(1)
    total = result.get("data")["total"]
    page = total // 20 + 1

    output = []

    # 获取所有微博数据
    for i in range(1, page + 1):
        result = get_weibo_data(i)
        for j in result.get("data")["list"]:
            # 过滤年份
            if str(year) not in j["created_at"]:
                continue

            output.append("// " + convert_time_string(j["created_at"]))

            text = j["text_raw"]
            # 如果文本过长, 获取长微博数据
            if j["isLongText"]:
                try:
                    data = get_long_weibo_data(j["mblogid"])["data"]
                    if "longTextContent" in data:
                        text = data["longTextContent"]
                except Exception as e:
                    print(e)
                    pass
            text = align_text(text)
            output.append(text + "\n")

            # output.append("\n")

    # 写入文件
    file_name = "weibo_{}.txt".format(year)
    with open(file_name, "w") as f:
        f.write("\n".join(output))


if __name__ == '__main__':
    main()
