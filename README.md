
# 💼 job-etl-pipeline

> 🚀 A practical ETL project for recruitment data cleaning and transformation using Python and MySQL  
> 🚀 一个基于 Python + MySQL 的招聘数据清洗与转换项目，具备实际 ETL 经验积累价值

---

## 📌 项目简介 | Project Overview

该项目模拟企业级数据工程实践流程，从数据采集到清洗、转换与入库，实现了完整的招聘岗位数据处理管道。数据源为智联招聘采集的原始招聘信息，最终目标是生成结构化、高质量的数据，供后续分析与建模使用。

This project simulates a practical enterprise-level ETL pipeline. It starts from job postings collected via web scraping, and processes the data through cleaning, transformation, and loading into a MySQL database. It serves as a foundation for downstream analytics or machine learning tasks.

---

## 🧱 技术栈 | Tech Stack

- **语言 Language**：Python 3.10+
- **数据库 Database**：MySQL 8
- **数据处理 Data Handling**：pandas, re
- **数据库接口 Database API**：SQLAlchemy, PyMySQL
- **可选工具 Optional Tools**：Selenium（数据采集），Matplotlib（数据探索）

---

## 🗂️ 项目结构 | Project Structure

```

job\_etl\_pipeline/
├── data/                    # 原始招聘数据（CSV格式）
├── results/                 # 清洗结果和异常数据（可选导出）
├── analysis/                # EDA 脚本，例如薪酬分布分析
├── etl/                     # ETL 核心逻辑模块
│   ├── extract.py           # 数据加载
│   ├── transform.py         # 数据转换（清洗/标准化/特征工程）
│   ├── validate.py          # 数据校验逻辑
│   └── load.py              # 数据加载至 MySQL
├── main.py                  # 项目主流程入口
├── config.py                # 数据库及文件配置项
├── README.md                # 项目说明文档（当前文件）
└── report.md                # 项目总结报告
└── requirements.txt         # 依赖包列表

```

---

## 🎯 核心功能 | Key Features

- [√] 多源数据整合（公司+岗位信息）
- [√] 薪酬字段智能解析（支持月薪/日薪/区间/单位转换）
- [√] 工作经验字段解析（区间平均值/无经验/不限）
- [√] 异常值检测与标记（如工资异常、高校学历空值）
- [√] 数据入库至 MySQL，并支持异常数据单独输出
- [√] 可扩展性强，支持进一步接入数据质量报告、调度平台

---

## 📊 示例图表 | Sample Analysis

<div align="center">
  <img src="https://raw.githubusercontent.com/yourname/job-etl-pipeline/main/assets/salary_boxplot.png" width="60%" />
  <br/>
  <em>📦 薪酬分布箱线图（基于处理后的数据）</em>
</div>

---

## 📚 项目适用场景 | Use Cases

- 用于简历中的 ETL 项目经验展示
- 作为数据工程面试的作品集支撑
- 提升对数据清洗、转换及入库流程的实践能力
- 为 AI 招聘建模或分析打下数据基础

---

## 💡 作者推荐建议

若你计划未来进入以下方向：

- ✅ 数据分析师 / 数据工程师
- ✅ 数据治理 / 数据质量管理

该项目可以作为扎实的数据准备项目起点。

---

## 📮 联系方式 | Contact

如需交流该项目，欢迎通过 GitHub Issue 联系或发送邮件至：41142633@qq.com

```


