import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False
import os

os.makedirs("../charts", exist_ok=True)

df = pd.read_csv("scraped_jobs.csv")

exp_counts = df["标题4"].value_counts()

color_map = {
    "3-5年": "#4472C4",
    "不限": "#ED7D31",
    "1-3年": "#A5A5A5",
    "5-10年": "#FFC000",
    "10年以上": "#5B9BD5",
}
colors = [color_map.get(label, "#7F7F7F") for label in exp_counts.index]

fig, ax = plt.subplots(figsize=(8, 8))
wedges, texts, autotexts = ax.pie(
    exp_counts.values,
    labels=exp_counts.index,
    autopct="%1.1f%%",
    startangle=90,
    colors=colors,
    wedgeprops=dict(width=0.5, edgecolor="white")
)
ax.set_title("数据相关岗位工作经验要求分布", fontsize=14, fontweight="bold")

plt.tight_layout()
plt.savefig("charts/chart6_experience.png", dpi=150, bbox_inches="tight")
plt.show()


# 工作经验要求分布柱状图
exp_sorted = exp_counts.sort_values(ascending=False)
plt.figure(figsize=(10, 6))
bars = plt.bar(range(len(exp_sorted)), exp_sorted.values, color="#B5B35C")
plt.xticks(range(len(exp_sorted)), exp_sorted.index, rotation=30, ha="right")
plt.xlabel("经验要求")
plt.ylabel("岗位数量")
plt.title("数据相关岗位工作经验要求分布")
for bar, val in zip(bars, exp_sorted.values):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10,
             str(int(val)), ha="center", va="bottom", fontsize=10)
plt.tight_layout()
plt.savefig("charts/chart6_experience_bar.png", dpi=150, bbox_inches="tight")
plt.show()
