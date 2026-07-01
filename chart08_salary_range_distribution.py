import pandas as pd
import matplotlib.pyplot as plt
import re
import numpy as np
plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False
import os

os.makedirs("../charts", exist_ok=True)

df = pd.read_csv("scraped_jobs.csv")

def parse_salary(content):
    content = str(content)
    match = re.search(r"薪酬[:：]\s*(\d+)-(\d+)", content)
    if match:
        low, high = int(match.group(1)), int(match.group(2))
        return (low + high) / 2
    return None

df["salary_avg"] = df["内容"].apply(parse_salary)

salary_bins = [0, 3000, 5000, 8000, 10000, 15000, 20000, 30000, 50000, 100000]
salary_labels = ["3K以下","3K-5K","5K-8K","8K-10K","10K-15K","15K-20K","20K-30K","30K-50K","50K以上"]
df["salary_bin"] = pd.cut(df["salary_avg"], bins=salary_bins, labels=salary_labels)
salary_dist = df["salary_bin"].value_counts().sort_index()

x = range(len(salary_labels))
y = [salary_dist.get(l, 0) for l in salary_labels]

fig, ax = plt.subplots(figsize=(12, 5))
ax.fill_between(x, y, alpha=0.3, color="#C0504D")
ax.plot(x, y, color="#C0504D", marker="o", markersize=6)

for i, v in enumerate(y):
    ax.text(i, v + 10, str(v), ha="center", va="bottom", fontsize=10)

ax.set_xticks(x)
ax.set_xticklabels(salary_labels, rotation=45, ha="right")
ax.set_xlabel("薪酬区间")
ax.set_ylabel("岗位数量")
ax.set_title("数据相关岗位薪酬区间分布")

plt.tight_layout()
plt.savefig("charts/chart4_salary_distribution.png", dpi=150, bbox_inches="tight")
plt.show()
