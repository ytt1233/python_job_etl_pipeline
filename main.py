import pandas as pd
from sqlalchemy import create_engine
from etl.extract import extract_from_csv
from etl.transform import extract_company_info
from etl.transform import prepare_job_data
from etl.load import load_company_and_jos
from etl.load import load_errors
from etl.validata import validate_job_data


if __name__ == "__main__":

    file_path = 'data/ai_jobs.csv'
    user = "root"
    password = "12345678"
    host = "192.168.0.132"
    db = "test_db"
    # 1. 创建数据库连接
    conn_string = f'mysql+pymysql://{user}:{password}@{host}/{db}'
    engine = create_engine(conn_string)

    # 2. 提取数据
    df = extract_from_csv(file_path)
    #3 清洗+拆表
    df_company = extract_company_info(df)
    df_job = prepare_job_data(df)
    # 4. 校验异常数据
    error_df_validation, clean_job_df = validate_job_data(df_job)
    # 7、 加载公司和岗位
    load_company_and_jos(df_company, clean_job_df, engine)
    # 8. 写入异常表
    load_errors(error_df_validation, engine)

    print("数据处理完毕！")