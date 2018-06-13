import pandas as pd
import datetime

Y = 2000 # dummy leap year to allow input X-02-29 (leap day)
seasons = [(0, (datetime.date(Y,  1,  1),  datetime.date(Y,  3, 20))), #winter
           (1, (datetime.date(Y,  3, 21),  datetime.date(Y,  6, 20))), #spring
           (2, (datetime.date(Y,  6, 21),  datetime.date(Y,  9, 22))), #summer
           (3, (datetime.date(Y,  9, 23),  datetime.date(Y, 12, 20))), #autumn
           (4, (datetime.date(Y, 12, 21),  datetime.date(Y, 12, 31)))] #winter

def get_season(timestamp):
    '''
    Given a date, return the season of the year (an integer from 0 to 3)
    '''
    date_time = timestamp.split(' ')
    date = date_time[0].split('-')

    yyyy = int(date[0])
    mm = int(date[1])
    dd = int(date[2])

    date = datetime.date(yyyy, mm, dd)

    def get_season_auxiliary(date):
        '''
        Given a date, return the season of the year (an integer from 0 to 3)
        '''
        if isinstance(date, datetime.datetime):
            date = date.date()
        now = date.replace(year=Y)
        return next(season for season, (start, end) in seasons
                    if start <= now <= end)

    season = get_season_auxiliary(date)

    return int(season)

def get_hour(timestamp):
    date_time = timestamp.split(' ')
    time = date_time[1].split(':')
    hour = time[0]

    return int(hour)

def get_day_of_the_week(timestamp):
    date_time = timestamp.split(' ')
    date = date_time[0].split('-')

    yyyy = int(date[0])
    mm = int(date[1])
    dd = int(date[2])

    date = datetime.date(yyyy, mm, dd)

    day_of_the_week = date.weekday() # categorical

    return int(day_of_the_week)

def extract_prior_on_user(df_train, df_test):

    # Compute the prior on the training set
    prior = df_train.groupby(['uid'])['click'].agg(['mean', 'count', 'sum'])

    # Join the prior to the training set
    enriched_df_train = df_train.join(prior, on=['uid'])
    enriched_df_train.rename(index=str,
                             columns={"mean": "prior_uid_click_trough_rate", "count": "prior_uid_nb_observations"},
                             inplace=True)

    # Join the prior to the test set
    enriched_df_test = df_test.join(prior, on=['uid'])
    enriched_df_test.rename(index=str,
                             columns={"mean": "prior_uid_click_trough_rate", "count": "prior_uid_nb_observations"},
                             inplace=True)

    return enriched_df_train, enriched_df_test

def main():
    # Load train and test set
    df_train = pd.read_csv('data/data_train.csv', header=0, sep=',', parse_dates=['logged_at'])
    df_test = pd.read_csv('data/data_test.csv', header=0, sep=',', parse_dates=['logged_at'])

    print("Computing prior knowledge on users")
    df_enriched_train, df_enriched_test = extract_prior_on_user(df_train, df_test)

    print("Extracting time information")
    df_enriched_train['day_of_the_week'] = (df_enriched_train['logged_at'].astype(str)).apply(lambda x: get_day_of_the_week(x))
    df_enriched_train['hour'] = (df_enriched_train['logged_at'].astype(str)).apply(lambda x: get_hour(x))
    df_enriched_train['season'] = (df_enriched_train['logged_at'].astype(str)).apply(lambda x: get_season(x))

    df_enriched_test['day_of_the_week'] = (df_enriched_test['logged_at'].astype(str)).apply(lambda x: get_day_of_the_week(x))
    df_enriched_test['hour'] = (df_enriched_test['logged_at'].astype(str)).apply(lambda x: get_hour(x))
    df_enriched_test['season'] = (df_enriched_test['logged_at'].astype(str)).apply(lambda x: get_season(x))

    df_enriched_train.to_csv(path_or_buf='data/enriched_data_train.csv', index=False)
    df_enriched_test.to_csv(path_or_buf='data/enriched_data_test.csv', index=False)

main()