import pandas as pd
import re

df = pd.read_csv("scraped_jobs.csv")
print(f"总数据量: {len(df)}条")

# 薪酬解析函数：从内容列提取薪酬
def parse_salary(content):
    """从内容列中提取薪酬并计算均值"""
    content = str(content)
    match = re.search(r"薪酬[:：]\s*(\d+)-(\d+)", content)
    if match:
        low, high = int(match.group(1)), int(match.group(2))
        return (low + high) / 2
    return None

df["salary_avg"] = df["内容"].apply(parse_salary)

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
    """将城市名映射为省份"""
    city = str(city)
    for c, p in province_map.items():
        if c in city:
            return p
    return "其他"

df["province"] = df["标题2"].apply(city_to_province)

def classify_job(name):
    """根据岗位名称关键词分类"""
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
print("岗位类别分布:")
print(df["job_type"].value_counts())
