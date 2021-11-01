# coding=utf-8
import os
import re


def is_Chinese(word):
    for ch in word:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False


def is_pure_english(word):
    # 因为定义的一些变量或者方法可能带有下划线
    # 还有一些分割的时候，把两个单次分割到了一块，所以带有空格，还有一些带()，
    # 所以先把这些去掉，再进行判断
    word = word.replace("_", "").replace(" ", "").\
        replace("(", "").replace(")", "").replace("-", "").replace(".", "").\
        replace("/", "").replace("`", "").replace("、", "").\
        replace("\"", "").replace("=", "").encode('UTF-8')
    if word.isalpha():
        return True
    if word.isdigit():
        return True
    if word.isalnum():
        return True
    return False


def endswith_words_or_nums(str1):
    if str1[-1].isalpha() or str1[-1].isdigit():
        return True
    return False


def endswith_special_marks(str1):
    if str1.endswith("，") and str1[-2].isalpha():
        return True
    if str1.endswith("、") and str1[-2].isalpha():
        return True
    return False


def startswith_words_or_nums(str1):
    if str1[0].isalpha() or str1[0].isdigit():
        return True
    return False


def beautifyText(text, pattern):
    """ 美化文案，中英文，英文与数字，中文与数字直接都添加空格
        :param text: 要美化的原始文案
        :param pattern: 替换规则
    """
    res = re.compile(pattern)  # [\u4e00-\u9fa5]中文范围
    p1 = res.split(text)
    result = ""
    if len(p1) == 1:
        return p1[0]
    for index in range(len(p1)):
        str1 = p1[index]
        if "\n" == str1 or '' == str1 or '，' == str1 or '、' == str1:
            result += str1
            continue
        elif is_Chinese(str1):
            # 如果全是中文
            result += str1
        elif is_pure_english(str1):
            # 是纯英文
            if index == 0:
                # 第一行的首个是数字或者英文，直接在后面添加空格，前面不需要
                result += (str1.strip() + " ")
            else:
                # 在单词的前后加空格
                result += (" " + str1.strip() + " ")
        elif str1.endswith("\n") and str1[-2].isalpha():
            # 如果最后是英文+\n，则在前面加一个空格，例如："pod\n" --> " pod\n"
            result += (" " + str1.strip() + "\n")
        elif endswith_words_or_nums(str1):
            # 如果 str1 是以单词或者结尾，但又不是纯英文，则在最后加一个空格
            result += (str1.strip() + " ")
        elif endswith_special_marks(str1) and index != 0:
            result += (" " + str1.strip())
        elif startswith_words_or_nums(str1) and index != 0:
            if str1[-1] == "\n":
                result += (" " + str1.strip() + "\n")
            else:
                result += (" " + str1.strip())
        elif str1.startswith("`") and str1.endswith("`"):
            result += (" " + str1.strip() + " ")
        else:
            result += str1
    return result


def beatifyFile(file):
    f1 = open(file=file, mode='r+', encoding='UTF-8')
    infos = f1.readlines()
    print("该文件一共有 " + str(len(infos)) + " 行")
    f1.seek(0, 0)
    for line in infos:
        new_str = beautifyText(line, r"([\u4e00-\u9fff]+)")
        line = line.replace(line, new_str)
        f1.write(line)
    f1.close()


def test(s):
    print("原始：" + s)
    text = beautifyText(s, r"([\u4e00-\u9fff])")
    print("转换：" + text)


def DirAll(pathName):
    if os.path.exists(pathName):
        fileList = os.listdir(pathName)
        for f in fileList:
            if not f.endswith(".md"):
                continue
            f = os.path.join(pathName, f)
            if os.path.isdir(f):
                DirAll(f)
            else:
                baseName = os.path.basename(f)
                if baseName.startswith("."):
                    continue
                print(f)
                beatifyFile(f)


if __name__ == '__main__':
    rootDir = 'F:\\XieKunDownload\\golang-main\\k8s详细教程'
    DirAll(rootDir)
    # beatifyFile("F:\\XieKunDownload\\golang-main\\k8s详细教程")
    # test("查看pod状态的的命令，2、删除pod\n")
    # test("**Swarm**：Docker自己的容器编排工具")
