import eda.getting_data as getting_data
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def get_data(match_format):
    return getting_data.get_match_data(match_format.strip())


def draw_wins_per_team(match_data):
    # get the matches for test nations only
    match_data = match_data.loc[match_data['test_nat']==True]
    # get all the team names
    team_names = match_data['team_a'].unique()

    number_of_matches = {}
    number_of_wins = {}
    win_percentage = pd.DataFrame(columns=['country','win_per'])
    wins_frame = pd.DataFrame(columns=['country', 'no_wins'])

    home_away_data = match_data[match_data['location'] == 'home_away']
    neutral_data = match_data[match_data['location'] == 'neutral']
    home_win_frame = pd.DataFrame(columns=['country', 'home_matches', 'home_wins', 'home_win_per'])
    away_win_frame = pd.DataFrame(columns=['country', 'away_matches', 'away_wins', 'away_win_per'])
    neutral_win_frame = pd.DataFrame(columns=['country', 'neutral_matches', 'neutral_wins', 'neutral_win_per'])
    toss_frame = pd.DataFrame(columns=['country', 'match_toss_win_per'])

    rain_data = match_data[match_data['rained'] == 'rained']
    rain_frame = pd.DataFrame(columns=['country', 'rain_win_per'])

    first_bat_frame = pd.DataFrame(columns=['country', 'first_bat_win_per'])
    second_bat_frame = pd.DataFrame(columns=['country', 'second_bat_win_per'])
    count = 0

    for team in team_names:
        count_list = []
        win_list = []
        print(team)
        # counting number of matches for each team
        match_data.apply(lambda x: count_list.append(1) if x['team_a'].lower() == team.lower()
                         or x['team_b'].lower() == team.lower() else ''
                         , axis=1)
        assert len(set(count_list)) == 1
        number_of_matches[team] = len(count_list)

        # counting number of wins for each team
        match_data.apply(lambda x: win_list.append(1) if x['team_a'].lower() == team.lower()
                                                           or x['team_b'].lower() == team.lower()
                                                           and x['winner'].lower() == team.lower()
                                                        else ''
                         , axis=1)
        assert len(set(win_list)) == 1
        number_of_wins[team] = len(win_list)

        wins_frame.loc[count, 'country'] = team
        wins_frame.loc[count, 'no_wins'] = len(win_list)

        win_percentage.loc[count,'country'] = team
        win_percentage.loc[count, 'win_per'] = number_of_wins[team]/number_of_matches[team] * 100

        # counting number of home matches and wins for each team
        home_match_count_list = []
        home_win_list = []
        # count home matches
        home_away_data.apply(lambda x: home_match_count_list.append(1)
                             if x['team_a'].lower() == team.lower()
                             else '', axis=1)
        # count home wins
        home_away_data.apply(lambda x: home_win_list.append(1)
                             if x['team_a'].lower() == team.lower()
                                and x['winner'].lower() == team.lower()
                             else '', axis=1)
        assert len(set(home_win_list)) == 1 and len(set(home_match_count_list)) == 1
        home_win_frame.loc[count, 'country'] = team
        home_win_frame.loc[count, 'home_matches'] = len(home_match_count_list)
        home_win_frame.loc[count, 'home_wins'] = len(home_win_list)
        home_win_frame.loc[count, 'home_win_per'] = home_win_frame.loc[count, 'home_wins']/home_win_frame.loc[count, 'home_matches'] * 100

        # counting number of away matches and wins for each team
        away_match_count_list = []
        away_win_list = []
        # count away matches
        home_away_data.apply(lambda x: away_match_count_list.append(1)
                             if x['team_b'].lower() == team.lower()
                             else ''
                             ,axis=1)
        # count away wins
        home_away_data.apply(lambda x: away_win_list.append(1)
                             if x['team_b'].lower() == team.lower()
                                and x['winner'].lower() == team.lower()
                             else ''
                             ,axis=1)

        assert len(set(away_win_list)) == 1 and len(set(away_match_count_list)) == 1
        away_win_frame.loc[count, 'country'] = team
        away_win_frame.loc[count, 'away_matches'] = len(away_match_count_list)
        away_win_frame.loc[count, 'away_wins'] = len(away_win_list)
        away_win_frame.loc[count, 'away_win_per'] = away_win_frame.loc[count, 'away_wins']/away_win_frame.loc[count, 'away_matches'] * 100

        # count number of neutral matches and wins for each team
        neutral_match_count_list = []
        neutral_win_list = []
        # count neutral matches
        neutral_data.apply(lambda x: neutral_match_count_list.append(1)
                           if x['team_a'].lower() == team.lower()
                              or x['team_b'].lower() == team.lower()
                           else ''
                           , axis=1)
        # count neutral wins
        neutral_data.apply(lambda x: neutral_win_list.append(1)
                           if (x['team_a'].lower() == team.lower() or x['team_b'].lower() == team.lower())
                              and x['winner'].lower() == team.lower()
                           else ''
                           , axis=1)

        assert len(set(neutral_win_list)) == 1 and len(set(neutral_match_count_list)) == 1
        neutral_win_frame.loc[count, 'country'] = team
        neutral_win_frame.loc[count, 'neutral_matches'] = len(neutral_match_count_list)
        neutral_win_frame.loc[count, 'neutral_wins'] = len(neutral_win_list)
        neutral_win_frame.loc[count, 'neutral_win_per'] = neutral_win_frame.loc[count, 'neutral_wins']/neutral_win_frame.loc[count, 'neutral_matches'] * 100

        # count no of wins after winning toss for each team
        toss_match_wins = []
        match_data.apply(lambda x: toss_match_wins.append(1)
                         if x['winner'].strip().lower() == team.strip().lower()
                            and x['toss'].strip().lower() == team.strip().lower()
                         else '',axis=1)
        assert len(set(toss_match_wins)) == 1
        toss_frame.loc[count, 'country'] = team
        toss_frame.loc[count, 'match_toss_win_per'] = len(toss_match_wins)/number_of_wins[team] * 100

        # count no of wins for rainy
        rain_list = []
        rain_win_list = []
        rain_data.apply(lambda x: rain_list.append(1)
                        if x['team_a'].strip().lower() == team.strip().lower() or x['team_b'].strip().lower() == team.strip().lower()
                        else '', axis=1)
        rain_data.apply(lambda x: rain_win_list.append(1)
                        if (x['team_a'].strip().lower() == team.strip().lower() or x['team_b'].strip().lower() == team.strip().lower())
                           and x['winner'].strip().lower() == team.strip().lower()
                        else ''
                        , axis=1)
        assert len(set(rain_list)) == 1 and len(set(rain_win_list)) == 1
        rain_frame.loc[count, 'country'] = team
        rain_frame.loc[count, 'rain_win_per'] = len(rain_win_list)/len(rain_list) * 100

        # bat first/second wins
        first_bat_data = match_data[match_data['first_batting'].apply(lambda x: x.strip().lower()) == team.strip().lower()]
        second_bat_data = match_data[match_data['second_batting'].apply(lambda x: x.strip().lower()) == team.strip().lower()]

        #'first_bat_win_per'])
        #second_bat_frame = pd.DataFrame(columns=['country', 'second_bat_win_per']
        first_bat_win_list = []
        first_bat_data.apply(lambda x: first_bat_win_list.append(1)
                             if x['winner'].strip().lower() == team.strip().lower()
                             else ''
                             , axis=1)
        print(str(len(set(first_bat_win_list))))
        assert len(set(first_bat_win_list)) == 1
        first_bat_frame.loc[count, 'country'] = team
        first_bat_frame.loc[count, 'first_bat_win_per'] = len(first_bat_win_list)/first_bat_data.shape[0] * 100

        second_bat_win_list = []
        second_bat_data.apply(lambda x: second_bat_win_list.append(1)
                              if x['winner'].strip().lower() == team.strip().lower()
                              else ''
                              , axis=1)
        assert len(set(second_bat_win_list)) == 1
        second_bat_frame.loc[count, 'country'] = team
        second_bat_frame.loc[count, 'second_bat_win_per'] = len(second_bat_win_list) / second_bat_data.shape[0] * 100
        count += 1
    # write the combined wins records for each team to disk
    #use of .set_index() is necessary for joining multiple data frames #, on='country'
   
    count plot for number of wins
    no_games = sns.countplot(x='team_a',data=match_data)# hue='team_a',
    plt.setp(no_games.get_xticklabels(), rotation=30)
    plt.ylabel('Number of games(ODI)')
    plt.xlabel('')
    plt.show()
    plt.clf()
    ###############################
    # bar plot for win percentage #
    ###############################

    # prep the data set - sort, and set index of the frame
    win_percentage = win_percentage.sort_values(by=['win_per'], axis=0, ascending=False)
    win_percentage.loc[:,'row_no'] = range(win_percentage.shape[0])
    win_percentage.set_index('row_no', inplace=True)
    # draw the plot
    wins_per_plot = sns.barplot(x='country', y='win_per',  data=win_percentage)#hue='win_per',
    # rotate the x-axis tick labels
    plt.setp(wins_per_plot.get_xticklabels(), rotation=30)
    # label the bars in the plot
    for index,row in win_percentage.iterrows():
        wins_per_plot.text(row.name, row['win_per'], round(row['win_per'], 2), color='black', ha='center')#
    plt.ylabel('Win Percent(ODI)')
    plt.xlabel('')
    plt.suptitle('Percentage wins for each test nation')
    plt.savefig('eda/plots/win_per_bar.jpg')
    plt.clf()

    # draw bar plot for Home wins of each team
    home_win_frame = home_win_frame.sort_values(by='home_win_per', axis=0, ascending=False)
    home_win_frame.loc[:, 'row_no'] = range(home_win_frame.shape[0])
    home_win_frame.set_index('row_no', inplace=True)
    home_wins_plot = sns.barplot(x='country', y='home_win_per', data=home_win_frame)
    plt.setp(home_wins_plot.get_xticklabels(), rotation=30)
    for index, row in home_win_frame.iterrows():
        home_wins_plot.text(row.name, row['home_win_per'], round(row['home_win_per'], 2), color='black', ha='center')
    plt.ylim(0, 100)
    plt.tight_layout()
    plt.ylabel('home win percent')
    plt.xlabel('')
    plt.suptitle('Percentage wins for each test nation in home matches')
    plt.savefig('eda/plots/home_win_per_bar.jpg')
    plt.clf()

    # draw bar plot for Away wins of each team
    away_win_frame = away_win_frame.sort_values(by='away_win_per', axis=0, ascending=False)
    away_win_frame.loc[:, 'row_no'] = range(away_win_frame.shape[0])
    away_win_frame.set_index('row_no', inplace=True)
    away_wins_plot = sns.barplot(x='country', y='away_win_per', data=away_win_frame)
    plt.setp(away_wins_plot.get_xticklabels(), rotation=30)
    for index, row in away_win_frame.iterrows():
        away_wins_plot.text(row.name, row['away_win_per'], round(row['away_win_per'], 2), color='black', ha='center')
    plt.ylim(0, 100)
    plt.tight_layout()
    plt.ylabel('away win percent')
    plt.xlabel('')
    plt.suptitle('Percentage wins for each test nation in away matches')
    plt.savefig('eda/plots/away_win_per_bar.jpg')
    plt.clf()

    # draw bar plot for Neutral wins of each team
    neutral_win_frame = neutral_win_frame.sort_values(by='neutral_win_per', axis=0, ascending=False)
    neutral_win_frame.loc[:, 'row_no'] = range(neutral_win_frame.shape[0])
    neutral_win_frame.set_index('row_no', inplace=True)
    neutral_wins_plot = sns.barplot(x='country', y='neutral_win_per', data=neutral_win_frame)
    plt.setp(neutral_wins_plot.get_xticklabels(), rotation=30)
    for index, row in neutral_win_frame.iterrows():
        neutral_wins_plot.text(row.name, row['neutral_win_per'], round(row['neutral_win_per'], 2), color='black', ha='center')#neutral_win_per
    plt.ylim(0, 100)
    plt.tight_layout()
    plt.ylabel('neutral win percent')
    plt.xlabel('')
    plt.suptitle('Percentage wins for each test nation in neutral matches')
    plt.savefig('eda/plots/neutral_win_per_bar.jpg')
    plt.clf()

    # draw plot for toss effects per team
    toss_frame = toss_frame.sort_values(by='match_toss_win_per', axis=0, ascending=False)
    toss_frame.loc[:, 'row_no'] = range(toss_frame.shape[0])
    toss_frame.set_index('row_no', inplace=True)
    toss_plot = sns.barplot(x='country', y='match_toss_win_per', data=toss_frame)
    plt.setp(toss_plot.get_xticklabels(), rotation=30)
    for index, row in toss_frame.iterrows():
        toss_plot.text(row.name, row['match_toss_win_per'], round(row['match_toss_win_per'], 2), color='black', ha='center')
    plt.ylabel('Matches won after toss wins(%)')
    plt.xlabel('')
    plt.suptitle('Toss won and Match won')
    plt.savefig('eda/plots/toss_match_team.jpg')
    plt.clf()

    # effect of rain plot
    rain_frame = rain_frame.sort_values(by='rain_win_per', axis=0, ascending=False)
    rain_frame.loc[:, 'row_no'] = range(rain_frame.shape[0])
    rain_frame.set_index('row_no', inplace=True)
    rain_plot = sns.barplot(x='country', y='rain_win_per', data=rain_frame)
    plt.setp(rain_plot.get_xticklabels(), rotation=30)
    for index, row in rain_frame.iterrows():
        rain_plot.text(row.name, row['rain_win_per'], round(row['rain_win_per'], 2), color='black', ha='center')
    plt.ylim(0, 100)
    plt.tight_layout()
    plt.ylabel('Win % in rain conditions')
    plt.xlabel('')
    plt.suptitle('Percentage win in rainy conditions')
    plt.savefig('eda/plots/rain_win_team.jpg')
    plt.clf()

    # effect of bat_first
    first_bat_frame = first_bat_frame.sort_values(by='first_bat_win_per', axis=0, ascending=False)
    first_bat_frame.loc[:, 'row_no'] = range(first_bat_frame.shape[0])
    first_bat_frame.set_index('row_no', inplace=True)
    bat_first_plot = sns.barplot(x='country', y='first_bat_win_per', data=first_bat_frame)
    plt.setp(bat_first_plot.get_xticklabels(), rotation=30)
    for index, row in first_bat_frame.iterrows():
        bat_first_plot.text(row.name, row['first_bat_win_per'], round(row['first_bat_win_per'], 2), color='black', ha='center')
    plt.ylim(0, 100)
    plt.tight_layout()
    plt.ylabel('Win % batting first')
    plt.xlabel('')
    plt.suptitle('Percentage win for first batting')
    plt.savefig('eda/plots/first_bat_team.jpg')
    plt.clf()

    #effect of second batting
    second_bat_frame = second_bat_frame.sort_values(by='second_bat_win_per', axis=0, ascending=False)
    second_bat_frame.loc[:, 'row_no'] = range(second_bat_frame.shape[0])
    second_bat_frame.set_index('row_no', inplace=True)
    bat_second_plot = sns.barplot(x='country', y='second_bat_win_per', data=second_bat_frame)
    plt.setp(bat_second_plot.get_xticklabels(), rotation=30)
    for index, row in second_bat_frame.iterrows():
        bat_second_plot.text(row.name, row['second_bat_win_per'], round(row['second_bat_win_per'], 2), color='black', ha='center')
    plt.ylim(0, 100)
    plt.tight_layout()
    plt.ylabel('Win % batting second')
    plt.xlabel('')
    plt.suptitle('Percentage win for second batting')
    plt.savefig('eda/plots/second_bat_team.jpg')
    plt.clf()


def draw_toss_effect(match_data):
    # get the matches for test nations only
    match_data = match_data.loc[match_data['test_nat'] == True]
    #match_data = match_data.groupby(['year'])
    # get all the years
    years = match_data['year'].unique()
    toss_frame = pd.DataFrame(columns=['year', 'toss_match_won', 'toss_match_win_per'])
    iteration = 0
    for year in years:
        match_frame = match_data[match_data['year'] == year]
        #print(match_frame.columns)
        count_list = []
        match_frame.apply(lambda x: count_list.append(1)
                          if x['winner'].strip().lower() == x['toss'].strip().lower()
                          else '',
                          axis=1)
        toss_frame.loc[iteration, 'year'] = year
        toss_frame.loc[iteration, 'toss_match_won'] = len(count_list)
        toss_frame.loc[iteration, 'toss_match_win_per'] = toss_frame.loc[iteration, 'toss_match_won']/match_frame.shape[0] * 100
        iteration+=1

    plt.plot(toss_frame['year'], toss_frame['toss_match_win_per'])
    plt.xlim(1996, 2017)
    plt.ylim(20, 100)
    plt.ylabel('Matches won after toss wins(%)')
    plt.xlabel('Years')
    plt.suptitle('Toss and Match win combination(%)')
    plt.savefig('eda/plots/toss_match_year.jpg')
    plt.clf()

    plt.clf()


def per_year_team_stats(match_data):

    match_data = match_data[match_data['test_nat'] == True]

    unique_teams = match_data['team_a'].unique()
    # create a data frame grouped by year
    year_frame = match_data.groupby(['year'])

    plt.figure(figsize=(12, 12))
    # run loop for every unique team
    for count, team in enumerate(unique_teams):
        # create an empty frame to hold data for games played by each team every year
        year_wise_games = pd.DataFrame(columns=['year', 'games'])
        # run loop for each year
        for i, year in enumerate(year_frame.groups.keys()):
            games_list = []
            temp_frame = match_data[match_data['year'] == year]
            temp_frame.apply(lambda x: games_list.append(1)
                             if x['team_a'].strip().lower() == team.strip().lower()
                             or x['team_b'].strip().lower() == team.strip().lower()
                             else '', axis=1)
            year_wise_games.loc[i, 'year'] = year
            year_wise_games.loc[i, 'games'] = len(games_list)

        # draw the sub-plot
        #subplot(no_of_rows_of_master_plot, no_of_columns_of_master_plot, num(sub_plot_number))
        plt.subplot(5, 2, count + 1)
        wins_sub_plot = sns.barplot(x='year', y='games', data=year_wise_games)
        plt.setp(wins_sub_plot.get_xticklabels(), rotation=25)
        for index, row in year_wise_games.iterrows():
            wins_sub_plot.text(row.name, row['games'], round(row['games'], 0), color='black',
                               ha='center')
        plt.ylabel('Games played')
        plt.xlabel('')
        plt.title(team)

    # draw the main plot
    #plt.suptitle('Year wise Matches played by each Country')
    plt.tight_layout()
    plt.savefig('eda\plots\year_wise_matches.jpg')
    plt.clf()


draw_wins_per_team(get_data('combined'))
per_year_team_stats(get_data('combined'))
#draw_toss_effect(get_data('combined'))
#draw_wins_per_team(get_data('combined'))
#innings_score_avg(get_data('combined'))
#get_std_mean(get_data('combined'))
#draw_all_box_plots(get_data('combined'))