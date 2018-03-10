# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 16:47:59 2017

@author: Vivek
"""

import getting_ground_details as gd
import re
import pandas as pd

def get_match_data(match_format):
    return gd.map_ground_details(match_format)


def check_nulls(all_match_frame):
    print(1)
    assert (all_match_frame['date'].hasnans and all_match_frame['countries'].hasnans)
    print(2)


def create_attributes(match_format):
    try:
        # get the required match data
        all_match_frame = get_match_data(match_format)
        # print(all_match_frame['firstinn_score']==None)
        # check_nulls(all_match_frame)
        print(all_match_frame.columns)
        print(all_match_frame.info())

        # create month attribute
        month_list = []
        month_name_list = []
        month_dict = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
                      7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}
        all_match_frame['date'].apply(lambda x: month_list.append(x.month))
        for month in month_list:
            month_name_list.append(month_dict[month])
        assert all_match_frame.shape[0] == len(month_list)
        all_match_frame.loc[:, 'month'] = month_name_list
        print('month created')

        # create day of the week attribute
        # 6 - Monday....0 - Sunday
        day_list = []
        #all_match_frame['date'].apply(lambda x: day_list.append(x.dayofweek))
        all_match_frame['date'].apply(lambda x: day_list.append(x.weekday_name))
        assert all_match_frame.shape[0] == len(day_list)
        all_match_frame.loc[:, 'day'] = day_list
        print('day created')

        # create year column
        year_list = []
        all_match_frame['date'].apply(lambda x: year_list.append(x.year))
        assert all_match_frame.shape[0] == len(year_list)
        all_match_frame.loc[:, 'year'] = year_list
        print('year created')

        # create attribute to record whether rained or not
        rained_list = []
        all_match_frame['rain'].apply(lambda x: rained_list.append('rained') if 'rain' in x.casefold()
                                       else rained_list.append('not rained')
                                      )
        assert all_match_frame.shape[0] == len(rained_list)
        all_match_frame.loc[:, 'rained'] = rained_list
        print('rain created')

        # get the two teams playing the match
        team_a_list = []
        team_b_list = []
        all_match_frame['countries'].apply(lambda x: team_a_list.append(x.lower().split('v.')[0].strip().capitalize()))
        all_match_frame['countries'].apply(lambda x: team_b_list.append(x.lower().split('v.')[1].strip().capitalize()))
        assert all_match_frame.shape[0] == len(team_a_list) and all_match_frame.shape[0] == len(team_b_list)
        all_match_frame.loc[:, 'team_a'] = team_a_list
        all_match_frame.loc[:, 'team_b'] = team_b_list
        print('team_a and team_b created')

        # get the winner of the game
        winner_list = []
        all_match_frame['result'].apply(lambda x: winner_list.append(x.split('won')[0].strip()))
        assert all_match_frame.shape[0] == len(winner_list)
        all_match_frame.loc[:, 'winner'] = winner_list
        print('winner created')

        # get the losing team
        loser_list = []
        all_match_frame.apply(lambda x: loser_list.append(x['team_b'].strip())
        if x['winner'].strip().casefold() == x['team_a'].strip().casefold()
        else loser_list.append(x['team_a'].strip()),
                              axis=1)
        assert all_match_frame.shape[0] == len(loser_list)
        all_match_frame.loc[:, 'loser'] = loser_list
        print('loser created')

        # get second batting
        second_bat_list = []
        all_match_frame.apply(lambda x: second_bat_list.append(x['team_b'])
                              if x['first_batting'].strip().casefold() == x['team_a'].strip().casefold()
                              else second_bat_list.append(x['team_a'].strip()),
                              axis=1)
        assert all_match_frame.shape[0] == len(second_bat_list)
        all_match_frame.loc[:, 'second_batting'] = second_bat_list
        print('second batting created')

        # create team_a/team_b first batting
        team_bat_first = []
        all_match_frame.apply(lambda x: team_bat_first.append('team_a')
                              if x['first_batting'].strip().lower() == x['team_a'].strip().lower()
                              else team_bat_first.append('team_b'), axis = 1)
        all_match_frame.loc[:,'team_bat_first'] = team_bat_first

        # create team_a/team_b second batting
        team_bat_second = []
        all_match_frame.apply(lambda x: team_bat_second.append('team_b')
                              if x['team_bat_first'].strip().lower() == 'team_a'
                              else team_bat_second.append('team_a'), axis=1)
        all_match_frame.loc[:, 'team_bat_second'] = team_bat_second

        # get the win margin, ex:- 5 wickets, 50 runs, etc.
        win_margin_list = []
        all_match_frame['result'].apply(lambda x: win_margin_list.append(x.split('won')[1].strip()))
        assert all_match_frame.shape[0] == len(win_margin_list)
        all_match_frame.loc[:, 'win_margin'] = win_margin_list
        print('win_margin created')

        # curate the day night information as boolean values
        day_night_list = []
        all_match_frame['day_night'].apply(lambda x: day_night_list.append(True) if 'Day/Night' in x
        else day_night_list.append(False)
                                           )
        assert all_match_frame.shape[0] == len(day_night_list)
        all_match_frame.loc[:, 'day_and_night'] = day_night_list
        print('day_night created')

        # get the no. of wickets, run rate and overs delivered in the first innings
        wckts_list = []
        first_inn_ovrs_list = []
        first_inn_rr_list = []

        def get_wckts_ovrs_rr_data(row):
            row_data = row.split(';')
            wckts = row_data[0].strip()
            ovrs_rr = re.findall('\d+\.\d{1,}', row_data[1])

            wckts_list.append(10 if wckts == "All Out" else re.findall('\d+', wckts)[0])
            first_inn_ovrs_list.append(ovrs_rr[0])
            first_inn_rr_list.append(ovrs_rr[1])

        all_match_frame['wckts_ovrs_rr'].apply(get_wckts_ovrs_rr_data)
        assert (all_match_frame.shape[0] == len(wckts_list) and all_match_frame.shape[0] == len(first_inn_ovrs_list)
                and all_match_frame.shape[0] == len(first_inn_rr_list)
                )
        all_match_frame.loc[:, 'first_inn_wckts'] = wckts_list
        all_match_frame.loc[:, 'first_inn_ovrs'] = first_inn_ovrs_list
        all_match_frame.loc[:, 'first_inn_rr'] = first_inn_rr_list
        print('wckts_rr_ovrs created')

        # get the location - home/away or neutral - sub country is used to overcome England/UK problem
        location_list = []
        all_match_frame.apply(lambda x: location_list.append('home_away')
        if x['country'].casefold().strip() == x['team_a'].casefold().strip() or
           x['country'].casefold().strip() == x['team_b'].casefold().strip() or
           x['sub_country'].casefold().strip() == x['team_a'].casefold().strip() or
           x['sub_country'].casefold().strip() == x['team_b'].casefold().strip()
        else location_list.append('neutral')
                              , axis=1)
        assert all_match_frame.shape[0] == len(location_list)
        all_match_frame.loc[:, 'location'] = location_list
        print('location created')

        # get if both teams are test nations till 2016
        test_team_list = ['india', 'south africa', 'england', 'new zealand', 'australia', 'sri lanka', 'pakistan',
                          'west indies', 'bangladesh', 'zimbabwe']
        test_nat_list = []
        #all_match_frame['test_nat'] = 'nv'
        all_match_frame.apply(lambda x: test_nat_list.append(True)
                                        if (x['team_a'].strip().lower() in test_team_list and x['team_b'].strip().lower() in test_team_list)
                                        else test_nat_list.append(False),
                              axis=1
                              )
        assert all_match_frame.shape[0] == len(test_nat_list)
        all_match_frame.loc[:, 'test_nat'] = test_nat_list
        print('test_nat created')

        print(all_match_frame.info())
        # creating classifier label
        #all_match_frame['win_team'] = 'some_team'
        win_team_list = []
        all_match_frame.apply(lambda x: win_team_list.append('team_a')
                              if x['winner'].strip().lower() == x['team_a'].strip().lower()
                              else(win_team_list.append('team_b')
                                   if x['winner'].strip().lower() == x['team_b'].strip().lower()
                                   else win_team_list.append('dirty_data'))
                              , axis=1)
        print(all_match_frame.shape[0], len(win_team_list))
        assert all_match_frame.shape[0] == len(win_team_list)
        #assert len(set(win_team_list)) == 2
        all_match_frame.loc[:, 'win_team'] = win_team_list
        print('win_team created')
        print(all_match_frame.columns)

        if __name__ == '__main__':
            all_match_frame.to_csv('E:/class/Dissertation/data/clean_format/'+match_format+'/'+match_format+
                                   '_all_attribute.csv', index=False)

        if __name__ != '__main__':
            return all_match_frame
    except SystemError:
        pass
    #except AssertionError as ae:
    #    print(ae)
    #except Exception as e:
    #   print('Error raised: '+str(e))


if __name__ == '__main__':
    #create_attributes('odi')
    create_attributes('t20')
    # user_input_message = 'Please Choose a match format. \n 1 - "odi" \t 2 - "t20" \n Make a choice: '
    # while True:
    #     num = int(input(user_input_message))
    #     if num == 1:
    #         create_attributes('odi')
    #         break
    #     elif num == 2:
    #         create_attributes('t20')
    #         break
