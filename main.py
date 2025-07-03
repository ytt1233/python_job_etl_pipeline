import pandas as pd
from sqlalchemy import create_engine
from config import DB_CONFIG, DATA_PATH
from etl.extract import extract_from_csv
from etl.transform import extract_company_info
from etl.transform import prepare_job_data
from etl.load import load_company_and_jos
from etl.load import load_errors
from etl.validata import validate_job_data


if __name__ == "__main__":
    # 1、获取配置信息
    file_path = DATA_PATH['ai_job_csv']
    user = DB_CONFIG["user"]
    password = DB_CONFIG["password"]
    host = DB_CONFIG["host"]
    db = DB_CONFIG["database"]
    # 2. 创建数据库连接
    conn_string = f'mysql+pymysql://{user}:{password}@{host}/{db}'
    engine = create_engine(conn_string)

    # 3. 提取数据
    df = extract_from_csv(file_path)
    #4 清洗+拆表
    df_company = extract_company_info(df)
    df_job = prepare_job_data(df)
    # 5. 校验数据
    error_df_validation, clean_job_df = validate_job_data(df_job)
    # 6、 加载公司和岗位
    load_company_and_jos(df_company, clean_job_df, engine)
    # 7. 写入异常表
    load_errors(error_df_validation, engine)

    print("数据处理完毕！")