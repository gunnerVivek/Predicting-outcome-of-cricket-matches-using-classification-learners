import pandas as pd
# udf module
import odi_format
import t20_format

odi_master = odi_format.clean_format_data()
t20_master = t20_format.clean_format_data()

#odi_grounds_list = odi_master['ground'].unique()
t20_grounds_list = t20_master['ground'].unique()

write_file_path = 'data/'
odi_grounds_file = write_file_path+'grounds_odi.csv'
t20_grounds_file = write_file_path+'grounds_t20.csv'

if __name__ == '__main__':
    pd.Series(odi_grounds_list).to_csv(odi_grounds_file, header=['ground'],index=False)
    pd.Series(t20_grounds_list).to_csv(t20_grounds_file, header=['ground'],index=False)



    
    