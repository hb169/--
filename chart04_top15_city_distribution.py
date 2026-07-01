import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False
import os
os.makedirs("../charts", exist_ok=True)

# 读取数据
df = pd.read_csv("scraped_jobs.csv")

city_counts = df["标题2"].value_counts().head(15)
plt.figure(figsize=(12, 7))
bars = city_counts.sort_values().plot(kind="barh", color="#5B9BD5")
plt.xlabel("岗位数量")
plt.title("数据相关岗位城市分布Top15")
# 在柱顶标注数值
for bar in bars.patches:
    plt.text(bar.get_width() + 3, bar.get_y() + bar.get_height()/2,
             str(int(bar.get_width())), ha="left", va="center", fontsize=9)
plt.tight_layout()
plt.savefig("charts/chart2_city_distribution.png", dpi=150, bbox_inches="tight")
plt.show()
