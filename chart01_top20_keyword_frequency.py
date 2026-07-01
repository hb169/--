import pandas as pd
import matplotlib.pyplot as plt
import jieba
import re
from collections import Counter
import os

plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False
os.makedirs("../charts", exist_ok=True)

df = pd.read_csv("scraped_jobs.csv")

# 添加自定义词典
custom_words = ["数据分析", "数据工程师", "数据挖掘", "大数据", "数据产品",
    "数据运营", "机器学习", "深度学习", "人工智能", "数据中台",
    "数据治理", "数据仓库", "数据开发", "数据架构", "数据分析师",
    "算法工程师", "BI工程师", "ETL", "Hadoop", "Spark",
    "Python", "SQL", "Java", "数据标注", "数据采集",
    "数据处理", "数据管理", "数据策略"]
for w in custom_words:
    jieba.add_word(w, freq=100)

stopwords = set(["的","（","）","(",")","-","—","、","及","和","与","或",
    "在","了","是","有","不","也","等","中","上","下","到",
    "公司","招聘","岗位","职位","工作","相关","方向","领域",
    "高级","资深","初级","中级","要求","经验","年","月","薪",
    "负责","进行","从事","担任","任职","实习","全职","兼职"])

all_words = []
for name in df["标题"]:
    words = jieba.cut(str(name))
    for w in words:
        w = w.strip()
        if len(w) >= 2 and w not in stopwords and not re.match(r"^[\d\s]+$", w):
            all_words.append(w)

word_freq = Counter(all_words)

# 获取Top20高频词，反转顺序使最高频的在最上方
top20_words = word_freq.most_common(20)
top20_words.reverse()
labels = [w[0] for w in top20_words]
values = [w[1] for w in top20_words]

fig, ax = plt.subplots(figsize=(12, 8))
bars = ax.barh(range(len(labels)), values, color="#4472C4", height=0.6)
ax.set_yticks(range(len(labels)))
ax.set_yticklabels(labels, fontsize=10)
ax.set_xlabel("出现次数", fontsize=10)
ax.set_title("岗位名称Top20词频分布", fontsize=13, fontweight="bold")

# 在柱右侧标注数值
for bar, val in zip(bars, values):
    ax.text(bar.get_width() + 10, bar.get_y() + bar.get_height()/2,
            str(val), ha="left", va="center", fontsize=9)

plt.tight_layout()
plt.savefig("charts/chart12_top20_freq.png", dpi=150, bbox_inches="tight")
plt.show()
