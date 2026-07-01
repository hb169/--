import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re
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

def classify_job(name):
    name = str(name).lower()
    if "分析" in name: return "数据分析类"
    elif "工程" in name or "开发" in name: return "数据工程/开发类"
    elif "产品" in name: return "数据产品类"
    elif "算法" in name or "ai" in name: return "算法/AI类"
    elif "标注" in name or "采集" in name: return "数据处理/标注类"
    elif "运营" in name or "策略" in name: return "数据运营/策略类"
    elif "管理" in name: return "数据管理类"
    else: return "其他数据相关"

df["job_type"] = df["标题"].apply(classify_job)

type_salary = df.groupby("job_type")["salary_avg"].mean()

categories = ["其他数据相关", "数据工程/开发类", "数据产品类", "数据处理/标注类",
              "数据运营/策略类", "算法/AI类", "数据分析类"]
values = [type_salary.get(c, 0) for c in categories]

N = len(categories)
angles = [n / float(N) * 2 * np.pi for n in range(N)]
angles += angles[:1]
values += values[:1]

fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))
ax.plot(angles, values, color="#9B59B6", linewidth=2)
ax.fill(angles, values, color="#9B59B6", alpha=0.25)
ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories, fontsize=12)

for angle, val, cat in zip(angles[:-1], values[:-1], categories):
    ax.text(angle, val + 1000, f"{int(val)}", ha="center", va="center", fontsize=10, color="#9B59B6")

ax.set_title("不同岗位类型平均薪酬对比", fontsize=14, fontweight="bold", pad=20)

plt.tight_layout()
plt.savefig("charts/chart5_salary_by_type.png", dpi=150, bbox_inches="tight")
plt.show()

# 各类别数据岗位平均月薪对比水平柱状图
type_salary_sorted = type_salary.sort_values(ascending=True)
fig, ax = plt.subplots(figsize=(12, 6))
bars = ax.barh(range(len(type_salary_sorted)), type_salary_sorted.values, color="#9B8EC4", height=0.6)
ax.set_yticks(range(len(type_salary_sorted)))
ax.set_yticklabels(type_salary_sorted.index, fontsize=11)
ax.set_xlabel("平均月薪（元）")
ax.set_title("各类别数据岗位平均月薪对比")
for bar, val in zip(bars, type_salary_sorted.values):
    ax.text(bar.get_width() + 200, bar.get_y() + bar.get_height()/2,
            f"{int(val)}元", ha="left", va="center", fontsize=10)
plt.tight_layout()
plt.savefig("charts/chart5_salary_by_type_bar.png", dpi=150, bbox_inches="tight")
plt.show()
