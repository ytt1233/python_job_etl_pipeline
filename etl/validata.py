import pandas as pd

def validate_job_data(job_df):
    errors = []
    validate_edu = ["博士", "硕士", "本科", "大专", "中专/中技", "高中", "初中及以下", "学历不限"]
    for i,row in job_df.iterrows():
        issues = []
        dels = []
        #城市不能为空
        if row['city'].strip() == "":
            issues.append("城市不能为空") 
            dels.append('是')  #原数据是否删除
        #学历合法性
        if row['education_raw'].strip() not in validate_edu:
            issues.append("学历无效")
            dels.append('是')  #原数据是否删除
        #薪酬合法
        if row['salary_avg'] is None:
            issues.append("薪酬缺失")
            dels.append('否')  # 保留，仅标记异常
        elif row['salary_avg'] <= 0:
            issues.append("薪酬为负数")
            dels.append('是')  # 明显错误，剔除
        if row['salary_outlier_flag'] == 1:
            issues.append("薪酬异常")
            dels.append('否')#仅标记错误，但不删除原数据
        # 工作经验平均值是否为负
        if row.get('experience_years') is not None and row['experience_years'] < 0:
            issues.append("工作经验为负数")
            dels.append('是')
        # 更新时间合法
        try:
            pd.to_datetime(row["updated_date"])
        except:
            issues.append("更新时间非法")

        if issues:
            row_copy = row.copy()
            row_copy["error_reason"] = "，".join(issues)
            row_copy["is_deleted"] = ",".join(dels)
            errors.append(row_copy)
    error_df = pd.DataFrame(errors)
    to_drop = error_df[error_df['is_deleted'].str.contains('是')].index #有些数据既有"是"，也有"否"，则删除
    clean_df = job_df.drop(to_drop)
    return error_df, clean_df