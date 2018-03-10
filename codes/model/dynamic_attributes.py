import pandas as pd

import eda.getting_data as getting_data


def get_data(match_format):
    return getting_data.get_match_data(match_format.strip().lower())


def create_win_per(match_data):

    for i, row in match_data.iterrows():
        # get data till date - 0:5 - gives 0,1,2,3,4
        match_df = match_data.iloc[0:i+1, :]
        #print(match_df.info())
        #break
        team_a = row['team_a'].lower()
        team_b = row['team_b'].lower()

        team_a_mask = []
        match_df.apply(lambda x: team_a_mask.append(True)
                       if x['team_a'].lower() == team_a or x['team_b'].lower() == team_a
                       else team_a_mask.append(False), axis=1)
        team_a_df = match_df[team_a_mask]

        team_b_mask = []
        match_df.apply(lambda x: team_b_mask.append(True)
                       if x['team_a'].lower() == team_b or x['team_b'].lower() == team_b
                       else team_b_mask.append(False), axis=1)
        team_b_df = match_df[team_b_mask]

        no_of_games_team_a = team_a_df.shape[0]
        no_of_games_team_b = team_b_df.shape[0]

        team_a_win = []
        team_a_df.apply(lambda x: team_a_win.append(1)
                        if x['winner'].lower() == row['team_a'].lower()
                        else '', axis=1)

        team_b_win = []
        team_b_df.apply(lambda x: team_b_win.append(1)
                        if x['winner'].lower() == row['team_b'].lower()
                        else '', axis=1)

        try:
            if len(team_a_win) > 0:
                team_a_win_per = round(len(team_a_win) / no_of_games_team_a * 100, 2)
            else:
                team_a_win_per = 50 # random chance
        except ZeroDivisionError:
            team_a_win_per = 50 # random chance

        try:
            if len(team_b_win) > 0:
                team_b_win_per = round(len(team_b_win) / no_of_games_team_b * 100, 2)
            else:
                team_b_win_per = 50 # random chance
        except ZeroDivisionError:
            team_a_win_per = 50 # random chance

        match_data.loc[i, 'team_a_win_per'] = team_a_win_per
        match_data.loc[i, 'team_b_win_per'] = team_b_win_per

    return match_data


def create_form(match_data):
    # Zimbabwe played ony 3 matches in one year
    lookup = 3

    for i, row in match_data.iterrows():
        match_df = match_data.iloc[0:i + 1, :]

        team_a = row['team_a'].lower()
        team_b = row['team_b'].lower()

        team_a_mask = []
        match_df.apply(lambda x: team_a_mask.append(True)
                       if x['team_a'].lower() == team_a or x['team_b'].lower() == team_a
                       else team_a_mask.append(False), axis=1)
        team_a_df = match_df[team_a_mask]

        team_b_mask = []
        match_df.apply(lambda x: team_b_mask.append(True)
                       if x['team_a'].lower() == team_b or x['team_b'].lower() == team_b
                       else team_b_mask.append(False), axis=1)
        team_b_df = match_df[team_b_mask]

        if team_a_df.shape[0] >= lookup:
            team_a_form_df = team_a_df.iloc[-3:, :]
            team_a_win = []
            team_a_form_df.apply(lambda x: team_a_win.append(1)
                                 if x['winner'].lower() == team_a
                                 else '', axis=1)
            team_a_form = round(len(team_a_win)/lookup * 100, 2)
        else:
            # team_a_form = row['team_a_win_per'] - because an attribute with the same already exists
            # not random i.e. 50 cause some calculations may be greater than 0 for the other team
            # let ML figure out
            team_a_form = 0

        if team_b_df.shape[0] >= lookup:
            team_b_form_df = team_b_df.iloc[-3:, :]
            team_b_win = []
            team_b_form_df.apply(lambda x: team_b_win.append(1)
                                 if x['winner'].lower() == team_b
                                 else '', axis=1)
            team_b_form = round(len(team_b_win)/lookup * 100, 2)

        else:
            team_b_form = 0

        match_data.loc[i, 'team_a_form'] = team_a_form
        match_data.loc[i, 'team_b_form'] = team_b_form

    return match_data


def create_loc_form(match_data):
    for i, row in match_data.iterrows():
        match_df = match_data.iloc[0:i + 1, :]

        team_a = row['team_a'].lower()
        team_b = row['team_b'].lower()

        # calculate for home/away matches
        if row['location'].strip().lower() == 'home_away':
            team_a_mask = []
            match_df.apply(lambda x: team_a_mask.append(True)
                           if x['team_a'].lower() == team_a
                           else team_a_mask.append(False), axis=1)
            team_a_df = match_df[team_a_mask]

            team_b_mask = []
            match_df.apply(lambda x: team_b_mask.append(True)
                           if x['team_b'].lower() == team_b
                           else team_b_mask.append(False), axis=1)
            team_b_df = match_df[team_b_mask]

            no_of_games_team_a = team_a_df.shape[0]
            no_of_games_team_b = team_b_df.shape[0]

            team_a_win = []
            team_a_df.apply(lambda x: team_a_win.append(1)
                            if x['winner'].lower() == team_a
                            else '', axis=1)

            team_b_win = []
            team_b_df.apply(lambda x: team_b_win.append(1)
                            if x['winner'].lower() == team_b
                            else '', axis=1)

            try:
                if len(team_a_win) > 0:
                    team_a_loc_win = round(len(team_a_win) / no_of_games_team_a * 100, 2)
                else:
                    # team_a_loc_win = row['team_a_win_per']
                    team_a_loc_win = 0
            except ZeroDivisionError:
                # team_a_loc_win = row['team_a_win_per']
                team_a_loc_win = 0

            try:
                if len(team_b_win) > 0:
                    team_b_loc_win = round(len(team_b_win) / no_of_games_team_b * 100, 2)
                else:
                    team_b_loc_win = 0
            except ZeroDivisionError:
                team_b_loc_win = 0
        # calculate for neutral matches
        elif row['location'].strip().lower() == 'neutral':
            team_a_mask = []
            match_df.apply(lambda x: team_a_mask.append(True)
                           if x['team_a'].lower() == team_a or x['team_b'].lower() == team_a
                           else team_a_mask.append(False), axis=1)
            team_a_df = match_df[team_a_mask]

            team_b_mask = []
            match_df.apply(lambda x: team_b_mask.append(True)
                           if x['team_a'].lower() == team_b or x['team_b'].lower() == team_b
                           else team_b_mask.append(False), axis=1)
            team_b_df = match_df[team_b_mask]

            no_of_games_team_a = team_a_df.shape[0]
            no_of_games_team_b = team_b_df.shape[0]

            team_a_win = []
            team_a_df.apply(lambda x: team_a_win.append(1)
                            if x['winner'].lower() == team_a
                            else '', axis=1)

            team_b_win = []
            team_b_df.apply(lambda x: team_b_win.append(1)
                            if x['winner'].lower() == team_b
                            else '', axis=1)

            try:
                if len(team_a_win) > 0:
                    team_a_loc_win = round(len(team_a_win) / no_of_games_team_a * 100, 2)
                else:
                    team_a_loc_win = 0
            except ZeroDivisionError:
                team_a_loc_win = 0

            try:
                if len(team_b_win) > 0:
                    team_b_loc_win = round(len(team_b_win) / no_of_games_team_b * 100, 2)
                else:
                    team_b_loc_win = 0
            except ZeroDivisionError:
                team_b_loc_win = 0

        match_data.loc[i, 'team_a_loc_win'] = team_a_loc_win
        match_data.loc[i, 'team_b_loc_win'] = team_b_loc_win

    return match_data


def create_bat_order_perf(match_data):
    for i, row in match_data.iterrows():
        match_df = match_data.iloc[0:i + 1, :]

        first_bat = row['first_batting'].lower()
        second_bat = row['second_batting'].lower()

        first_bat_mask = []
        match_df.apply(lambda x: first_bat_mask.append(True)
                       if x['first_batting'].lower() == first_bat
                       else first_bat_mask.append(False), axis=1)
        first_bat_df = match_df[first_bat_mask]

        second_bat_mask = []
        match_df.apply(lambda x: second_bat_mask.append(True)
                       if x['second_batting'].lower() == second_bat
                       else second_bat_mask.append(False), axis=1)
        second_bat_df = match_df[second_bat_mask]

        no_of_games_first_bat = first_bat_df.shape[0]
        no_of_games_second_bat = second_bat_df.shape[0]

        first_bat_win = []
        first_bat_df.apply(lambda x: first_bat_win.append(1)
                           if x['winner'].lower() == first_bat
                           else '', axis=1)

        second_bat_win = []
        second_bat_df.apply(lambda x: second_bat_win.append(1)
                            if x['winner'].lower() == second_bat
                            else '', axis=1)

        try:
            if len(first_bat_win) > 0:
                bat_first_perf = round(len(first_bat_win) / no_of_games_first_bat * 100, 2)
            else:
                bat_first_perf = 0
        except ZeroDivisionError:
            bat_first_perf = 0

        try:
            if len(second_bat_win) > 0:
                bat_second_perf = round(len(second_bat_win) / no_of_games_second_bat * 100, 2)
            else:
                bat_second_perf = 0
        except ZeroDivisionError:
            bat_second_perf = 0

        match_data.loc[i, 'bat_first_perf'] = bat_first_perf
        match_data.loc[i, 'bat_second_perf'] = bat_second_perf

    return match_data


def create_dynamic_attributes(match_data):
    # set the index for the data frame
    match_data_index = [x for x in range(match_data.shape[0])]
    match_data['row_no'] = match_data_index
    match_data.set_index(keys='row_no', inplace=True)

    # create win percent
    match_data['team_a_win_per'] = pd.Series()
    match_data['team_b_win_per'] = pd.Series()
    match_data['team_a_form'] = pd.Series()
    match_data['team_b_form'] = pd.Series()
    match_data['team_a_loc_win'] = pd.Series()
    match_data['team_b_loc_win'] = pd.Series()
    match_data['bat_first_perf'] = pd.Series()
    match_data['bat_second_perf'] = pd.Series()

    match_data = create_win_per(match_data)
    match_data = create_form(match_data)
    match_data = create_loc_form(match_data)
    match_data = create_bat_order_perf(match_data)

    print(match_data.info())
    return match_data


def get_dynamic_attributes(match_format):
    match_data = get_data(match_format)
    match_data = match_data[match_data['test_nat'] == True]
   
    match_data = create_dynamic_attributes(match_data)

    # write file
    match_data.to_csv('model/data/' + match_format + '_dynamic_attrib.csv', index=False)


get_dynamic_attributes('combined')