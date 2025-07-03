import re 
import pandas as pd
def clean_data(df):
    #去除空值
    df.dropna()
    #去除城市前后空格
    df['城市'] = df['城市'].str.strip()
    return df

def extract_company_info(df):
    """
    从原始DataFrame中提取公司维度信息（去重、字段重命名）
    """
    company_df = df[["公司名称", "公司类型", "公司规模", "公司行业"]].drop_duplicates().copy()
    company_df = company_df.rename(columns={
        "公司名称": "company_name",
        "公司类型": "company_type",
        "公司规模": "company_size",
        "公司行业": "company_industry"
    })
    return company_df


def prepare_job_data(df):
    """
    处理岗位信息数据，标准化字段，保留company_name用于映射公司ID
    """
    job_df = df[[
        "城市", "岗位", "薪酬", "技能", "工作经验", "学历", "职位类型", "人数",
        "公司名称", "地址", "职位更新日期"
    ]].copy()
    job_df = job_df.rename(columns={
        "城市": "city",
        "岗位": "position",
        "薪酬": "salary_raw",
        "技能": "skills",
        "工作经验": "experience_raw",
        "学历": "education_raw",
        "职位类型": "job_type",
        "人数": "headcount",
        "公司名称": "company_name",  # 暂保留，后续load时映射 company_id
        "地址": "company_address",
        "职位更新日期": "updated_date"
    })
    # 处理薪酬数据,生成新的列salary_avg并清洗
    job_df["salary_avg"] = job_df["salary_raw"].apply(parse_salary_range)
    job_df = mark_salary_outliers(job_df)
    # 处理学历数据
    job_df["education_clean"] = job_df["education_raw"].apply(standardize_education)
    # 处理经验数据
    job_df["experience_years"] = job_df["experience_raw"].apply(parse_experience)
    return job_df

def parse_salary_range(salary_str):
    """
    对 DataFrame 的“薪酬”列进行清洗处理，提取为 salary_avg（月薪均值）
    解析薪酬字符串，如 '1.2-2万'、'200-300元/天' 等，返回月薪平均值（元）
    """
    if not isinstance(salary_str, str):
        return None

    salary_str = salary_str.lower().strip()
    if any(term in salary_str for term in ['面议', '暂无']):
        return None

    match = re.match(r'(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)\s*(万|k|元)?(?:\s*/?\s*(天))?', salary_str)
    if match:
        low = float(match.group(1))
        high = float(match.group(2))
        unit = match.group(3)
        flag = match.group(4)

        avg = (low + high) / 2

        if flag == '天':
            return int(avg * 21.75)  # 按月估算
        else:
            if unit == 'k':
                return int(avg * 1000)
            elif unit == '万':
                return int(avg * 10000)
            else:
                return int(avg)

    return None

def mark_salary_outliers(df, threshold=50000):
    """
    标记 salary_avg 超过指定阈值的为异常
    """
    df["salary_outlier_flag"] = df["salary_avg"] > threshold
    return df

def standardize_education(edu_str):
    """
    将学历字段标准化为有限类别：博士、硕士、本科、大专、中专/中技、高中、初中及以下
    无效或模糊值返回 None
    """
    if not isinstance(edu_str, str):
        return None

    edu_str = edu_str.strip().lower()

    if "博士" in edu_str:
        return "博士"
    elif "硕士" in edu_str:
        return "硕士"
    elif "本科" in edu_str:
        return "本科"
    elif "大专" in edu_str or "专科" in edu_str:
        return "大专"
    elif "中专" in edu_str or "中技" in edu_str:
        return "中专/中技"
    elif "高中" in edu_str:
        return "高中"
    elif "初中" in edu_str or "小学" in edu_str:
        return "初中及以下"
    elif "不限" in edu_str or "无要求" in edu_str:
        return "学历不限"
    else:
        return None
def parse_experience(exp_str):
    """
    将工作经验字段标准化为区间平均值：
    "无"返回0，“不限"返回None
    """
    if not isinstance(exp_str, str):
        return None

    exp_str = exp_str.strip().lower()
    if '不限' in exp_str :
        return None
    if "无" in exp_str:
        return 0
    match = re.match(r'(\d+)-(\d+)年', exp_str)
    if match:
        low = int(match.group(1))
        high = int(match.group(2))
        return (low + high) / 2
    return None


# def job_data_clean(salary_str):
#     """
#     清洗薪酬数据

#     """
#     if not isinstance(salary_str, str):
#         return None
    
#     salary_str = salary_str.lower().strip()
#     # 1、处理无效数据
#     if any(term in salary_str for term in ['面议','暂无']):
#         return None
#     # 2、处理有效数据
#     # match = re.match(r'(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)\s*(万|k)?(/天)',salary_str)
#     match = re.match(r'(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)\s*(万|k|元)?(?:\s*/?\s*(天))?',salary_str)
#     if match:
#         low = float(match.group(1))
#         high = float(match.group(2))
#         unit = match.group(3)
#         flag = match.group(4)

#         avg = (low + high) / 2
#         if flag == '天':
#             return int(avg * 21.75)#平均每月工作天数
#         else:
#             if unit == 'k':
#                 return int(avg * 1000)
#             elif unit == '万':
#                 return int(avg * 10000)
#             else:
#                 return int(avg)
#             return None # 无效数据
            
#     # 3、处理空值(经过eda_salary.py对salary_avg列画直方图和箱线图分析后，发现薪酬缺失占比：3.24% 暂不处理)
    
#     # 4、处理异常值(异常值判断标准是：上限 = Q3 + 1.5 * IQR ≈ 20K + 1.5 * (20K - 8K) = 38K,根据经验clip设置为50000)
#     # 动态计算薪酬上限（基于箱线图）
#     q1 = df["salary_avg"].quantile(0.25)    
#     q3 = df["salary_avg"].quantile(0.75)
#     iqr = q3 - q1
#     upper_limit = q3 + 1.5 * iqr

#     # 限制极端高薪值
#     df["salary_avg"] = df["salary_avg"].clip(upper=upper_limit)


  