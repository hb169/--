import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
import jieba
import re
from collections import Counter
from wordcloud import WordCloud
import pandas as pd
import os

# 创建charts文件夹
os.makedirs("../charts", exist_ok=True)

df = pd.read_csv("scraped_jobs.csv")

# 添加数据领域专有词到jieba词典
custom_words = ["数据分析", "数据工程师", "数据挖掘", "大数据", "数据产品",
    "数据运营", "机器学习", "深度学习", "人工智能", "数据中台",
    "数据治理", "数据仓库", "数据开发", "数据架构", "数据分析师",
    "算法工程师", "BI工程师", "ETL", "Hadoop", "Spark",
    "Python", "SQL", "Java", "数据标注", "数据采集",
    "数据处理", "数据管理", "数据策略"]
for w in custom_words:
    jieba.add_word(w, freq=100)

# 停用词表
stopwords = set(["的","（","）","(",")","-","—","、","及","和","与","或",
    "在","了","是","有","不","也","等","中","上","下","到",
    "公司","招聘","岗位","职位","工作","相关","方向","领域",
    "高级","资深","初级","中级","要求","经验","年","月","薪",
    "负责","进行","从事","担任","任职","实习","全职","兼职"])

# 对岗位名称分词并统计词频
all_words = []
for name in df["标题"]:
    words = jieba.cut(str(name))
    for w in words:
        w = w.strip()
        if len(w) >= 2 and w not in stopwords and not re.match(r"^[\d\s]+$", w):
            all_words.append(w)

word_freq = Counter(all_words)
print(f"Top 20高频词: {word_freq.most_common(20)}")

# 生成词云图
font_path = r"C:\Windows\Fonts\simhei.ttf"
wc = WordCloud(
    font_path=font_path,
    width=1200, height=800,
    background_color="white",
    max_words=200,
    max_font_size=150,
    min_font_size=10,
    colormap="Set2",
    prefer_horizontal=0.7
)
wc.generate_from_frequencies(word_freq)

fig, ax = plt.subplots(figsize=(12, 8))
ax.imshow(wc, interpolation="bilinear")
ax.axis("off")
ax.set_title("数据相关岗位名称词云图", fontsize=16, pad=20)
plt.tight_layout()
plt.savefig("charts/chart11_wordcloud.png", dpi=150, bbox_inches="tight")
plt.show()
