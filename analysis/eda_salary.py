# eda_salary.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
import sys
import os
from pathlib import Path


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))#添加根目录到sys.path中
from etl.transform import parse_salary_range

plt.rcParams['font.sans-serif'] = ['SimHei']  # 正确显示中文
plt.rcParams['axes.unicode_minus'] = False    # 正确显示负号

# === 第一步：读取数据 ===
df = pd.read_csv("f:/mycode/job_etl_pipeline/data/ai_jobs.csv", encoding="gbk")

print("数据加载完成，总行数:", len(df))
# print(df[["岗位", "城市", "薪酬"]].head())

# === 第二步：清洗薪酬，构建 salary_avg ===
df["salary_avg"] = df["薪酬"].apply(parse_salary_range)
df.to_csv("salary_clean.csv", index=False,encoding="utf-8")
print(df[["岗位", "城市", "薪酬", "salary_avg"]].head())

# === 第三步：缺失情况分析 ===
missing_ratio = df["salary_avg"].isna().mean()
print(f"薪酬缺失占比：{missing_ratio:.2%}")

# === 第四步：绘制分布图 ===
plt.figure(figsize=(10, 6))
sns.histplot(df["salary_avg"].dropna(), bins=50, kde=True)
plt.title("薪酬分布直方图")
plt.xlabel("月薪（元）")
plt.ylabel("职位数量")
plt.grid(True)
plt.tight_layout()
plt.show()

# === 第五步：绘制箱型图看异常值 ===
plt.figure(figsize=(10, 2))
sns.boxplot(x=df["salary_avg"].dropna())
plt.title("薪酬箱型图")
plt.tight_layout()
plt.show()

# === 第六步：统计分布指标 ===
print("\n📊 salary_avg 描述性统计：")
print(df["salary_avg"].describe())

# === 第七步：按岗位查看中位数/均值 ===
print("\n📌 按岗位分组统计（前10）:")
print(df.groupby("岗位")["salary_avg"].agg(["count", "mean", "median"]).sort_values("count", ascending=False).head(10))

# === 第八步：按城市查看中位数 ===
print("\n🌍 按城市分组的薪酬中位数（Top 10）:")
print(df.groupby("城市")["salary_avg"].median().sort_values(ascending=False).head(10))
