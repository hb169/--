import pandas as pd
import os

os.makedirs("../outputs", exist_ok=True)

# 源数据：基础数据表
orig = pd.read_excel("2026春季《数据挖掘》考试规定动作 + 基础数据.xlsx")

# 提取数据：爬取的数据（去掉keyword列，和源数据格式一致）
df = pd.read_csv("scraped_jobs.csv")
df_extracted = df[["标题", "标题1", "标题2", "标题3", "标题4", "标题5", "内容"]]

# 写入xlsx
with pd.ExcelWriter("../outputs/完整数据.xlsx", engine="openpyxl") as writer:
    orig.to_excel(writer, sheet_name="源数据", index=False)
    df_extracted.to_excel(writer, sheet_name="提取数据", index=False)

print("xlsx文件生成完成")
