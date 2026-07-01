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
}

def city_to_province(city):
    city = str(city)
    for c, p in province_map.items():
        if c in city:
            return p
    return "其他"

df["province"] = df["标题2"].apply(city_to_province)

# 省级区域分布Top15水平柱状图
prov_counts = df["province"].value_counts().head(15)
plt.figure(figsize=(12, 7))
bars = prov_counts.sort_values().plot(kind="barh", color="#4ECDC4")
plt.xlabel("岗位数量")
plt.ylabel("province")
plt.title("数据相关岗位省级区域分布Top15")

# 在柱顶标注数值
for bar in bars.patches:
    plt.text(bar.get_width() + 3, bar.get_y() + bar.get_height()/2,
             str(int(bar.get_width())), ha="left", va="center", fontsize=9)

plt.tight_layout()
plt.savefig("charts/chart7_province.png", dpi=150, bbox_inches="tight")
plt.show()
