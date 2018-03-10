import pandas as pd
import math
import numpy as np
from sklearn.model_selection import KFold

import eda.getting_data as getting_data


def get_data(match_format):
    return getting_data.get_match_data(match_format.strip().lower())


def prep_probability_matrix(match_data):
    """
    :param match_data:
    :return: matrix of probabilities of each tem against the other
    """
    # get the team names
    team_names = list(match_data['team_a'].unique())
    #print(type(team_names))

    # prepare the column names
    column_names = ['country']
    column_names.extend(team_names)
    # set up the column names
    matrix_frame = pd.DataFrame(columns=column_names)
    matrix_frame.loc[:, 'country'] = team_names
    matrix_frame.set_index(keys='country',inplace=True)

   # print(team_names)
    for team in team_names:
        # get a temp frame to hold this team's data
        mask_list = []
        match_data.apply(lambda x: mask_list.append(True)
                         if x['team_a'].strip().lower() == team.strip().lower()
                         or x['team_b'].strip().lower() == team.strip().lower()
                         else mask_list.append(False), axis=1)
        team_frame = match_data[mask_list]
        #team_frame = match_data[match_data['team_a']==team or match_data['team_b']==team]
        # set the diagonal values of the matrix
        matrix_frame.loc[team, team] = 0
        # get each of the opponents
        opponents = list(team_names)
        opponents.remove(team)
     
        # calculate win percentage against each opponent
        for opponent in opponents:
            team_oppn_mask = list()
            team_frame.apply(lambda x: team_oppn_mask.append(True)
                             if x['team_a'].strip().lower() == opponent.strip().lower()
                             or x['team_b'].strip().lower() == opponent.strip().lower()
                             else team_oppn_mask.append(False), axis=1)
            team_oppn_frame = team_frame[team_oppn_mask]

            no_of_matches = team_oppn_frame.shape[0]
            
            no_of_wins = []
            team_frame.apply(lambda x: no_of_wins.append(1)
                             if (x['team_a'].strip().lower() == opponent.strip().lower()
                             or x['team_b'].strip().lower() == opponent.strip().lower())
                             and x['winner'].strip().lower() == team.strip().lower()
                             else '', axis=1)
            if no_of_matches > 0:
                matrix_frame.loc[team, opponent] = round(len(no_of_wins) / no_of_matches * 100, 2)
                #matrix_frame.loc[team, opponent] = no_of_matches#len(no_of_matches)
            elif no_of_matches <= 0:
                matrix_frame.loc[team, opponent] = 9999
            else:
                matrix_frame.loc[team, opponent] = 'dirty data'

    #print(matrix_frame)
    #matrix_frame.to_csv('eda\plots\\team_oppn_win_per.csv')
    #print(matrix_frame.info())
    return matrix_frame


def probabilistic_model(match_data, probability_matrix):
    """
    :param match_data:
    :param probability_matrix:
    :return: data frame with predicted winner column attached
    """
    prediction_frame = match_data.loc[:,['date', 'team_a', 'team_b', 'win_team']]

    prediction_frame['pred_win_team'] = 'inital_value'
    pred_win_team = list()
    prediction_frame.apply(lambda x: pred_win_team.append('team_a')
                            if probability_matrix.loc[x['team_a'], x['team_b']] >
                               probability_matrix.loc[x['team_b'], x['team_a']]
                            else(pred_win_team.append('team_b')
                                 if probability_matrix.loc[x['team_b'], x['team_a']] >
                                    probability_matrix.loc[x['team_a'], x['team_b']]
                                 else pred_win_team.append('tie'))
                           , axis=1)
    prediction_frame.loc[:, 'pred_win_team'] = pred_win_team

    return prediction_frame


def performance_measure(prediction_frame):
    """
    :param prediction_frame:
    :return: the accuracy of the learner over testing data
    """
    true_count = list()
    prediction_frame.apply(lambda x: true_count.append(1)
                           if x['win_team'].strip().lower() == x['pred_win_team'].strip().lower()
                           else '', axis=1)
    accuracy = len(true_count)/prediction_frame.shape[0] * 100

    return accuracy


def get_probabilistic_accuracy(match_format):
    match_data = get_data(match_format)
    match_data = match_data[match_data['test_nat'] == True]

    # splitting the data into 70:30 split
    train_end_index = int(math.floor((70 * match_data.shape[0])/100))
    test_start_index = train_end_index + 1
    
    train_data = match_data.loc[0:train_end_index, :]
    
    test_data = match_data.loc[test_start_index:, :]
    
    probability_matrix = prep_probability_matrix(train_data)
    probability_matrix.reset_index()
    predicted_data = probabilistic_model(test_data, probability_matrix)
    performance = round(performance_measure(predicted_data), 2)

    print(performance)


get_probabilistic_accuracy('combined')