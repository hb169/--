import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False
import os
os.makedirs("../charts", exist_ok=True)

# 读取数据
df = pd.read_csv("scraped_jobs.csv")

# 岗位分类函数
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

type_counts = df["job_type"].value_counts()
plt.figure(figsize=(8, 6))
plt.pie(type_counts.values, labels=type_counts.index, autopct="%1.1f%%",
        startangle=90, colors=plt.cm.Set3.colors[:len(type_counts)])
plt.title("数据相关岗位类别分布")
plt.tight_layout()
plt.savefig("charts/chart1_job_type_pie.png", dpi=150, bbox_inches="tight")
plt.show()
