import drop_obsolete_columns as do
import pandas


def combine_matches_data():

    odi_data = do.drop_columns('odi')
    t20_data = do.drop_columns('t20')

    combined_data = pandas.concat([odi_data, t20_data], axis=0, ignore_index=True)

    combined_data = combined_data.sort_values('date')
    if __name__=='__main__':
        combined_data.to_csv("/data/clean_format/combined/"+'combined_matches.csv', index=False)


if __name__ == '__main__':
    combine_matches_data()


