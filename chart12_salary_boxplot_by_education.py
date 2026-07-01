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

# 从"内容"列提取薪酬
def parse_salary(content):
    content = str(content)
    match = re.search(r"薪酬[:：]\s*(\d+)-(\d+)", content)
    if match:
        low, high = int(match.group(1)), int(match.group(2))
        return (low + high) / 2
    return None

df["salary_avg"] = df["内容"].apply(parse_salary)

# 从"内容"列提取学历
def extract_education(content):
    content = str(content)
    if "本科" in content: return "本科"
    elif "硕士" in content: return "硕士"
    elif "大专" in content: return "大专"
    elif "博士" in content: return "博士"
    elif "不限" in content: return "不限"
    else: return "其他"

df["edu"] = df["内容"].apply(extract_education)

# 不同学历要求对应的薪酬分布箱线图
edu_order = ["大专","本科","硕士","博士","不限"]
df_edu = df[df["edu"].isin(edu_order)]

plt.figure(figsize=(8, 6))
data_box = [df_edu[df_edu["edu"]==e]["salary_avg"].dropna().values for e in edu_order]
bp = plt.boxplot(data_box, patch_artist=True)
colors = ["#F4A0A0","#A8D5A2","#B4B8D4","#FFD966","#D4B8D4"]
for patch, color in zip(bp["boxes"], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.6)
plt.xticks(range(1, len(edu_order)+1), edu_order)
plt.ylabel("月薪（元）")
plt.title("不同学历要求对应的薪酬分布")
plt.tight_layout()
plt.savefig("charts/chart10_edu_salary.png", dpi=150, bbox_inches="tight")
plt.show()
