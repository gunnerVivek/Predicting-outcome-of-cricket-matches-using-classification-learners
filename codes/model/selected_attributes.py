import pandas as pd


def get_selected_attributes(match_format):

    with open('model/data/' + match_format + '_dynamic_attrib.csv', mode='r') as file:
            match_data = pd.read_csv(file)

    selected_attributes = ['win_team', 'location', 'day_and_night', 'wc_match', 'rained', 'team_a_win_per',
                           'team_b_win_per', 'team_a_form', 'team_b_form', 'bat_first_perf', 'bat_second_perf',
                           'team_bat_first', 'team_bat_second','format']

    match_data = match_data[selected_attributes]
    
    return match_data


if __name__ == '__main__':
    get_selected_attributes('combined')
