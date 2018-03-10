import pandas as pd
from IPython.core.magic_arguments import magic_arguments

import warnings
import os

read_file_path = 'data/'

grounds_file = read_file_path+'grounds_'

#print('-------------------Running getting_ground_details-----------------------------')


def get_all_matches(match_format):
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore")
        if match_format.strip().lower() == 'odi'.strip():
            import odi_format
            all_matches = odi_format.clean_format_data()
        elif match_format.strip().lower() == 't20'.strip():
            import t20_format
            all_matches = t20_format.clean_format_data()

        
    return all_matches


def get_ground_details(match_format):
    with open(grounds_file+match_format+'.csv', mode='r') as file:
        ground_details = pd.read_csv(file, index_col=False)
        return ground_details


def map_ground_details(match_format):

    all_matches = get_all_matches(match_format)
    ground_details = get_ground_details(match_format)
    
    all_matches.loc[:, 'row_no'] = pd.Series(range(0,all_matches.shape[0])).values
    all_matches.set_index('row_no', inplace=True)
    all_matches_grounds = all_matches.loc[:, 'ground'];
    all_matches_grounds = all_matches_grounds.apply(lambda x: x.strip().lower())
    
    ground_details_grounds = ground_details['ground'];
    ground_details_grounds = ground_details_grounds.apply(lambda x: x.strip().lower())
    ground_details_country = ground_details['country']
    ground_details_sub_country = ground_details['sub_country']
    ground_details_city = ground_details.loc[:, 'city']
    
    ground_dict = dict(zip(ground_details_grounds, 
                           zip(ground_details_country, 
                               ground_details_sub_country, 
                               ground_details_city
                           )
                       )
    )

    am_country = []
    am_sub_country = []
    am_city = []
    
    for i in range(all_matches.shape[0]):
    
        match_ground = all_matches_grounds[i].strip()
        
        details = ground_dict[match_ground]
        
        am_country.append(details[0])
        am_sub_country.append(details[1])
        am_city.append(details[2])
            
    all_matches.loc[:, 'country'] = am_country
    all_matches.loc[:, 'sub_country'] = am_sub_country
    all_matches.loc[:, 'city'] = am_city
    
    if __name__ == '__main__':
        all_matches.to_csv('data/clean_format/'+match_format+'/'+match_format+'_all.csv', index=False)
    
    if __name__!= '__main__':
        return all_matches

                      
           
if __name__ == '__main__':
    map_ground_details('combined')

