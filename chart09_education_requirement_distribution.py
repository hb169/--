import pandas as pd
import matplotlib.pyplot as plt
import re
plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False
import os

# 创建charts文件夹
os.makedirs("../charts", exist_ok=True)

# 读取数据
df = pd.read_csv("scraped_jobs.csv")

# 从"内容"列提取学历
def extract_education(content):
    content = str(content)
    if "博士" in content: return "博士"
    elif "硕士" in content: return "硕士"
    elif "本科" in content: return "本科"
    elif "大专" in content: return "大专"
    elif "中专" in content or "中技" in content: return "中专/中技"
    elif "高中" in content: return "高中"
    elif "初中" in content: return "初中及以下"
    elif "不限" in content: return "不限"
    else: return "未注明"

df["edu"] = df["内容"].apply(extract_education)

# 按学历层次排序（与报告一致）
edu_order = ["初中及以下", "高中", "中专/中技", "大专", "不限", "本科", "硕士", "博士"]
edu_counts = df["edu"].value_counts()

# 只保留edu_order中存在的类别，并按edu_order排序
ordered_labels = [e for e in edu_order if e in edu_counts.index]
ordered_values = [edu_counts[e] for e in ordered_labels]

plt.figure(figsize=(10, 5))
bars = plt.bar(range(len(ordered_labels)), ordered_values, color="#548235")
plt.xticks(range(len(ordered_labels)), ordered_labels, rotation=30, ha="right")
plt.xlabel("学历要求")
plt.ylabel("岗位数量")
plt.title("数据相关岗位学历需求分布")

# 在柱顶标注数值
for bar, val in zip(bars, ordered_values):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 15,
             str(int(val)), ha="center", va="bottom", fontsize=10)

plt.tight_layout()
plt.savefig("charts/chart3_education.png", dpi=150, bbox_inches="tight")
plt.show()
