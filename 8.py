import pandas as pd
import matplotlib.pyplot as plt
import json
import os
plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False

# 创建charts文件夹
os.makedirs("../charts", exist_ok=True)

# 读取数据
df = pd.read_csv("scraped_jobs.csv")

keywords = ["数据", "数据分析师", "数据工程师"]
colors = ["#4472C4", "#548235", "#C0504D"]

# 优先从CSV的keyword列统计，否则从keyword_totals.json读取
if "keyword" in df.columns:
    keyword_counts = df["keyword"].value_counts()
    values = [keyword_counts.get(k, 0) for k in keywords]
else:
    with open("keyword_totals.json", "r", encoding="utf-8") as f:
        keyword_totals = json.load(f)
    values = [keyword_totals.get(k, 0) for k in keywords]

plt.figure(figsize=(8, 6))
bars = plt.bar(range(len(keywords)), values, color=colors, width=0.7)
plt.xticks(range(len(keywords)), keywords, fontsize=12)
plt.ylabel("岗位数量")
plt.title("不同关键词搜索结果岗位数量对比", fontsize=14, fontweight="bold")

# 在柱顶标注数值
for bar, val in zip(bars, values):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10,
             str(int(val)), ha="center", va="bottom", fontsize=11)

plt.tight_layout()
plt.savefig("charts/chart6_keyword_compare.png", dpi=150, bbox_inches="tight")
plt.show()
