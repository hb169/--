import requests
import json
import re
import time
import csv
from datetime import datetime

# 定义爬虫函数：从百度百聘获取单页数据
def fetch_page(keyword, page=1):
    """从百度百聘获取指定关键词的第page页数据"""
    url = "https://yiqifu.baidu.com/g/aqc/joblist"
    params = {"q": keyword, "page": page}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    resp = requests.get(url, headers=headers, params=params, timeout=15)
    idx = resp.text.find("window.pageData")
    end_idx = resp.text.find("</script>", idx)
    pd_str = resp.text[idx+len("window.pageData = "):end_idx]
    pd_str = pd_str.rstrip().rstrip(";")
    if pd_str.endswith("|| {}"):
        pd_str = pd_str[:-5].rstrip()
    data = json.loads(pd_str)
    return data.get("list", []), data.get("total", 0)

# 岗位分类（对应标题3列）
def classify_job(name):
    name = str(name)
    if "分析" in name: return "数据分析"
    elif "工程" in name or "开发" in name: return "技术"
    elif "算法" in name or "AI" in name: return "算法/AI"
    elif "产品" in name: return "产品"
    elif "标注" in name or "采集" in name: return "数据处理"
    elif "运营" in name: return "运营/策略"
    else: return "技术"

# 批量爬取三个关键词的所有分页
keywords = ["数据", "数据分析师", "数据工程师"]
all_jobs = {}
crawl_date = datetime.now().strftime("%Y-%m-%d")

for kw in keywords:
    jobs, total = fetch_page(kw, 1)
    page_count = (total + 19) // 20
    print(f"关键词[{kw}]共{total}条, {page_count}页")
    for page in range(1, page_count + 1):
        if page > 1:
            jobs, _ = fetch_page(kw, page)
        time.sleep(0.5)
        for job in jobs:
            job_id = job.get("jobId", "")
            if job_id and job_id not in all_jobs:
                name = re.sub(r"<[^>]+>", "", job.get("jobName", ""))
                company = job.get("company", "")
                city = job.get("city", "")
                salary = job.get("salary", "")
                edu = job.get("edu", "")
                exp = job.get("exp", "")
                source = job.get("source", "")
                # 组装内容：薪酬+学历+经验+来源
                parts = []
                if salary: parts.append(f"薪酬:{salary}")
                if edu: parts.append(f"学历:{edu}")
                if exp: parts.append(f"经验:{exp}")
                if source: parts.append(f"来源:{source}")
                content = "\n".join(parts)

                all_jobs[job_id] = {
                    "标题": name,
                    "标题1": company,
                    "标题2": city,
                    "标题3": classify_job(name),
                    "标题4": exp if exp else "不限",
                    "标题5": crawl_date,
                    "内容": content,
                    "keyword": kw,
                }
    print(f"  爬取完成，累计去重后: {len(all_jobs)}条")
# 保存各关键词搜索结果总数（供6.5.py读取）
keyword_totals = {}
for kw in keywords:
    _, total = fetch_page(kw, 1)
    keyword_totals[kw] = total
    time.sleep(0.3)
with open("keyword_totals.json", "w", encoding="utf-8") as f:
    json.dump(keyword_totals, f, ensure_ascii=False, indent=2)
print(f"关键词搜索结果数已保存到keyword_totals.json: {keyword_totals}")

# 保存为CSV（列名与原始xlsx一致）
cols = ["标题","标题1","标题2","标题3","标题4","标题5","内容","keyword"]
with open("scraped_jobs.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=cols)
    writer.writeheader()
    for job in all_jobs.values():
        writer.writerow(job)
print(f"共保存{len(all_jobs)}条数据到scraped_jobs.csv")

