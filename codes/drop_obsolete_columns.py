import attribute_creation as ae


def drop_columns(match_format):
    all_match_frame = ae.create_attributes(match_format)
    print(all_match_frame.info())
    columns_to_drop = ['countries', 'ground', 'result', 'day_night', 'wckts_ovrs_rr', 'rain']
    
    all_match_frame.drop(columns_to_drop, axis=1, inplace=True)

    rearrange_cols = ['date', 'team_a', 'team_b', 'winner', 'loser', 'location', 'day_and_night', 'toss', 'wc_match',
                      'rained', 'year','month', 'day', 'first_batting', 'second_batting','team_bat_first',
                      'team_bat_second','firstinn_score', 'secondinn_score', 'extras', 'first_inn_wckts',
                      'first_inn_ovrs', 'first_inn_rr', 'win_margin', 'country', 'sub_country', 'city', 'test_nat',
                      'format', 'win_team']
    all_match_frame = all_match_frame[rearrange_cols]
    if __name__ == '__main__':
        all_match_frame.to_csv('data/clean_format/'+match_format+'/'+match_format+'_all_attrib_req.csv', index=False)
    
    if __name__!= '__main__':
        return all_match_frame


if __name__ == '__main__':
    drop_columns('combined')
    