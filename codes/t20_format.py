import os
import inspect
import re
import glob
import pandas as pd


print('---------Running t20_format-------------------')
t20_data_path = 'data/t20/';
os.chdir(t20_data_path)

# re to match all non world cup matches.
t20_file_regex = re.compile('^matches_t20_\d{4}\.csv$')
# re to all world cup matches
t20_wc_file_regex = re.compile('^t20_worldcup_\d{4}\.csv$')
# grab all the .csv files
t20_csv_files = glob.glob('*.csv')

# list of all yearly dataframes
all_t20_data = []

# count of sum of total rows in each yearly data_frame
frame_row_count = 0


def drop_columns(data_frame, file_name):
    """
        @param data_frame - yearly match data frame
        @param file_name - only needed to print in except

        @return - a dataframe without below mentioned columns

        this function drops the two columns - Var.1 and &nbsp
    """
    try:
        # drop the var.1(row no.) and scorecard columns
        return data_frame.drop(['Var.1', '&nbsp'], axis=1)
    except ValueError:
        print('Columns not found to drop: %s'.format(file_name))
        return


def format_and_clean():
    '''
        this function: - 1) drops columns
                         2) renames columns - removes spaces and converts to lower case
                         3) changes column type of date to pandas datetime
                         4) assigns match format odi/t20
                         5) creates the list for creating the main dataframe from
    '''
    for file_name in t20_csv_files:

        # pick only the non world cup matches
        if t20_file_regex.match(file_name):

            # read yearly match data
            with open(file_name, mode='r') as file:
                data_frame = pd.read_csv(file, encoding='utf-8')

            # function call to drop the var.1(row no.) and scorecard columns
            data_frame = drop_columns(data_frame, file_name)

            # remove spaces from column name and convert to lower case.
            data_frame.rename(columns=lambda x: x.strip().replace(' ', '_').lower(), inplace=True)

            # strip leading and trailing whitespcaes
            def remove_white_space(column):
                # if column.dtype == "object":
                #    column = column.apply(lambda x : x.strip())
                # else:
                col_type = column.dtype
                column = column.astype(str)
                column = column.apply(lambda x: x.strip())
                column = column.astype(col_type)

                return column

            data_frame = data_frame.apply(remove_white_space, axis=0)

            # change type of date column
            data_frame.loc[:, 'date'] = pd.to_datetime(data_frame['date'], dayfirst=True)

            # clean the wckts_ovrs_rr column data.
            # use .replace() to get rid of all \n and &nbsp.
            # Then feed it to regex to detect continous two or more white space
            data_frame.loc[:, 'wckts_ovrs_rr'] = data_frame.loc[:, 'wckts_ovrs_rr'].apply(
                lambda x: re.sub(r'[ ]{2,}', ';',
                                 x.replace('\n', '').replace('&nbsp', '')
                                 )
            )

            # mark the match format by introducing a new column
            data_frame.loc[:, 'format'] = 't20'

            # count the no of rows for every year, used for verification checking before master frame creation
            global frame_row_count
            frame_row_count = frame_row_count + data_frame.shape[0]

            # write to the dataframe list for creating combined dataframe
            global all_t20_data
            all_t20_data.append(data_frame)

            # on an independent run write yearly data to disk
            if __name__ == '__main__':
                data_frame.to_csv('data/clean_format/t20/' + str(file_name),
                                  index=False
                                  )


def merge_all(all_t20_data):
    """
        @param - list containig all the data frames for individual years
        @retun - combined master dataframe
        creates the master(combined) dataframe
    """

    try:
        assert len(all_t20_data) > 0
        master_frame = pd.concat(all_t20_data, axis=0, ignore_index=True)
        global frame_row_count
        assert frame_row_count == master_frame.shape[0]
        return master_frame
    except AssertionError:
        print("Merge of dataframes failed. t20 frame list incorrect.")
        raise SystemExit(1)


def detect_unwanted_result(row):
    '''
        @param - a row of a dataframe(combined data dataframe)
        @return - bool

        This function takes every row and checks if the result of the match is
        either 'no result', 'abandoned', 'cancelled', 'conceded',
        'won by default' or 'tied'. Returns a boolean series with row wise
        true (if either of the above stated values) else false.
    '''

    unwanted_results = ['Match abandoned', 'Match cancelled', 'Match Tied',
                        'No result', 'conceded', 'default', 'walkover'
                        ]

    flag = False
    for i in range(len(unwanted_results)):
        if unwanted_results[i] in row:
            flag = True
            break

    return flag


def remove_unwanted_matches(master_data):
    """

       Remove all the observations with unwanted results
    """
    try:
        # remove any observation with empty result column
        if master_data['result'].hasnans:
            master_data.dropna(axis=0, subset=['result'], inplace=True)

        # remove unwanted results
        temp = pd.DataFrame(master_data['result'])
        mask = temp['result'].apply(detect_unwanted_result)
        master_data = master_data[~mask]
        return master_data

    except Exception as e:
        # log the error
        # print('Error raised in: %s'.format(str(e)))
        print(e)


# match_format
def get_wc_dates():
    """

    """
    try:
        # assert str(match_format).strip().casefold() in ['odi','t20']
        wc_date = []
        for file_name in t20_csv_files:

            if t20_wc_file_regex.match(file_name):
                with open(file_name, mode='r') as file:
                    data_frame = pd.read_csv(file, encoding='utf-8')

                unique = data_frame['Date'].unique()
                wc_date.extend(unique)

        # print("Wc_DATE: ", len(wc_date))
        return pd.to_datetime(wc_date, dayfirst=True)

    except AssertionError as ae:
        print(inspect.currentframe().f_code.co_name + ' :', ae)


def mark_wc_match(clean_master):
    try:
        wc_date = get_wc_dates()

        def confirm_wc_date(date_col):
            return date_col.apply(lambda x: x in wc_date)

        wc_match_index = pd.Series(confirm_wc_date(clean_master['date']))

        clean_master.loc[:, 'wc_match'] = wc_match_index.values

        return clean_master
    except Exception as ae:
        print(inspect.currentframe().f_code.co_name + ' :', ae)


def clean_format_data():
    """
        entry point to the code
    """
    format_and_clean()
    global all_t20_data
    master_data = merge_all(all_t20_data)
    try:
        # on an independent run write combined data to disk
        if __name__ == '__main__':
            master_data.to_csv('data/clean_format/t20/' + 'master_t20_data.csv',
                               index=False,
                               # na_rep='NA'
                               )

        # function call to remove unwanted columns
        clean_master = remove_unwanted_matches(master_data)
        # function call to mark matches with bool, if world cup match
        clean_master = mark_wc_match(clean_master)

        # on an independent run write cleaned combined data to disk
        if __name__ == '__main__':
            clean_master.to_csv('data/clean_format/t20/' + 't20_master_clean.csv', index=False)

        # when script is being executed from another script return the cleaned combined frame
        if __name__ != '__main_':
            return clean_master

    except AssertionError:
        print("Row count of master file not equal to sum of row counts of individual frames.")


# main function of the file
if __name__=='__main__':
    clean_format_data()