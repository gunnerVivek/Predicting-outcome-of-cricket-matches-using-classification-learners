import pandas as pd


def get_match_data():

    # taken as raw string to prevent special character interpretation
    combined_file_path = r'E:/class/Dissertation/data/combined/'

	with open(combined_file_path+'combined_matches.csv', mode='r') as file:
            match_frame = pd.read_csv(file)

    return match_frame


if __name__ == '__main__':
	get_match_data()