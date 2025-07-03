from sqlalchemy import create_engine
from sqlalchemy import text

def load_to_mysql(df, table_name, user, password, host, db):
    conn_string = f'mysql+pymysql://{user}:{password}@{host}/{db}'
    engine = create_engine(conn_string)
    df.to_sql(table_name, engine, if_exists='replace', index=False)


def load_company_and_jos(df_company, df_job, engine):
    with engine.connect() as conn:
        #插入公司数据
        df_company.to_sql('company_info', con=engine, if_exists='append', index=False)
        #获取公司ID
        result = conn.execute(text('SELECT id, company_name FROM company_info'))
        id_mapping = {row[1]: row[0] for row in result}
        #将公司ID映射到职位数据中
        df_job['company_id'] = df_job['company_name'].map(id_mapping)
        df_job = df_job.drop(columns=['company_name'])

        #插入职位数据
        df_job.to_sql('job_postings', con=engine, if_exists='replace', index=False)

def load_errors(df_error, engine):
    if not df_error.empty:
        df_error.to_sql("error_jobs", con=engine, if_exists="replace", index=False)
        print(f"已写入异常记录 {len(df_error)} 条 到 error_jobs 表")
    else:
        print("未发现异常数据")
