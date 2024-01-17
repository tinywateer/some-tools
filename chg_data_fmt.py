# -*- coding: utf-8 -*-
# 把微博数据按照每月分割

import argparse


def main(file_path):
    content = []

    months = {}
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith("// "):
                month = ".".join(line.split(".")[:-1])
                if month not in months:
                    months[month] = True
                    content.append(month)
                    content.append("\n")
                    content.append("\n")
            else:
                if len(line.strip()) == 0 and len(content[-1].strip()) == 0:
                    continue
                content.append(line)

    for i in content:
        print(i)

    new_file_path = file_path.replace(".txt", "") + "_new.txt"
    with open(new_file_path, "w", encoding="utf-8") as f:
        f.writelines(content)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # file path
    parser.add_argument("-f", "--file", type=str, default="weibo_2023.txt", help="微博文件路径")
    args = parser.parse_args()

    file_path = args.file

    main(file_path)
