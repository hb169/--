import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False
import os

# 创建charts文件夹
os.makedirs("../charts", exist_ok=True)

# 读取数据
df = pd.read_csv("scraped_jobs.csv")

# 城市→省份映射
province_map = {
    "北京": "北京", "上海": "上海", "广州": "广东", "深圳": "广东",
    "杭州": "浙江", "成都": "四川", "武汉": "湖北", "南京": "江苏",
    "苏州": "江苏", "西安": "陕西", "长沙": "湖南", "郑州": "河南",
    "重庆": "重庆", "天津": "天津", "青岛": "山东", "济南": "山东",
    "合肥": "安徽", "福州": "福建", "厦门": "福建", "大连": "辽宁",
    "沈阳": "辽宁", "哈尔滨": "黑龙江", "长春": "吉林", "昆明": "云南",
    "南宁": "广西", "贵阳": "贵州", "太原": "山西", "石家庄": "河北",
    "南昌": "江西", "兰州": "甘肃", "海口": "海南", "呼和浩特": "内蒙古",
    "乌鲁木齐": "新疆", "拉萨": "西藏", "西宁": "青海", "银川": "宁夏",
    # 省份名直接匹配
    "广东": "广东", "浙江": "浙江", "江苏": "江苏", "四川": "四川",
    "湖北": "湖北", "陕西": "陕西", "湖南": "湖南", "河南": "河南",
    "山东": "山东", "安徽": "安徽", "福建": "福建", "辽宁": "辽宁",
    "黑龙江": "黑龙江", "吉林": "吉林", "云南": "云南", "广西": "广西",
    "贵州": "贵州", "山西": "山西", "河北": "河北", "江西": "江西",
    "甘肃": "甘肃", "海南": "海南", "内蒙古": "内蒙古", "新疆": "新疆",
    "西藏": "西藏", "青海": "青海", "宁夏": "宁夏",
}

def city_to_province(city):
    city = str(city)
    for c, p in province_map.items():
        if c in city:
            return p
    return "其他"

df["province"] = df["标题2"].apply(city_to_province)

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

# 主要省份岗位类别堆叠柱状图（取Top8省份）
top_provs = df["province"].value_counts().head(8).index
cross = pd.crosstab(df[df["province"].isin(top_provs)]["province"],
                    df[df["province"].isin(top_provs)]["job_type"])

fig, ax = plt.subplots(figsize=(12, 6))
cross.plot(kind="bar", stacked=True, colormap="Set2", ax=ax)
ax.set_xlabel("省份")
ax.set_ylabel("岗位数量")
ax.set_title("主要省份数据岗位类别分布")
ax.tick_params(axis='x', rotation=45)
ax.legend(title="岗位类别", bbox_to_anchor=(1.02, 1), loc="upper left")
fig.tight_layout()
fig.savefig("charts/chart9_province_jobtype.png", dpi=150, bbox_inches="tight")
plt.show()
