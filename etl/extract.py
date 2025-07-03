import pandas as pd

def extract_from_csv(file_path):
    df = pd.read_csv(file_path,encoding='gbk')  
    return df 


    
