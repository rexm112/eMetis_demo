import requests
from bs4 import BeautifulSoup
import chardet
import jieba
import re
from collections import Counter



# 获取网页主要内容（获取title和p）
TARGET_URL = "https://news.sina.com.cn/c/xl/2023-05-11/doc-imytkepa9937303.shtml"


def extract_web(url):
    # 发送GET请求，获取网页内容
    response = requests.get(url)
    encoding = chardet.detect(response.content)['encoding']
    # 使用Beautiful Soup解析HTML内容
    soup = BeautifulSoup(response.content.decode(encoding), 'html.parser')
    # 获取title标签的文本
    title = soup.title.string
    # 获取所有的p标签
    paragraphs = soup.find_all('p')
    # 获取每个p标签的文本，并将它们保存到一个列表中
    paragraph_list = []
    paragraph_texts = ""
    for p in paragraphs:
        paragraph_list.append(p.get_text())
    # 返回title和p标签的文本
    paragraph_texts = paragraph_texts.join(paragraph_list)
    return paragraph_texts

def preprocess_text(text):
    # 去除标点符号和数字
    text = re.sub('[^\u4e00-\u9fa5]+', '', text)
    # 分词
    tokens = jieba.lcut(text)
    return tokens

def extract_keywords(text, num_keywords=10):
    tokens = preprocess_text(text)
    print(tokens)
    # 统计词频并选取前num_keywords个关键词
    keywords = [keyword for keyword, count in Counter(tokens).most_common(num_keywords)]
    return keywords

def generate_summary(text, ratio=0.2):
    # 生成摘要
    summary = summarize(text, ratio=ratio, split=True)
    # 将摘要句子按照原文中的顺序排序
    summary_sentences = sorted(summary, key=lambda sentence: text.find(sentence))
    return ' '.join(summary_sentences)


content = extract_web(TARGET_URL)


keywords = extract_keywords(content)
summary = generate_summary(content)
print('Keywords:', keywords)
print('Summary:', summary)

