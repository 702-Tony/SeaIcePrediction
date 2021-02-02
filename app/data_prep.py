import pandas as pd
import numpy as np
import app.helpers as hlp



def prep_data(source):

    # PREPARE DATASET
    df = pd.read_csv(source)
    print('CSV Read')
    # rename columns
    df.columns = ['year', 'month','day', 'extent','missing','source_data','hemisphere']
    # remove unnecessary columns, i.e. source data
    df = df.drop(columns=['source_data'])
    # split the data frames
    df_n = df[df['hemisphere'] =='north'] # all north extents
    df_s = df[df['hemisphere'] =='south'] # all south extents
    # merge the dataframes together
    df_n.columns = ['year','month','day','n_extent','n_missing', 'df_n']
    df_s.columns = ['year','month','day','s_extent','s_missing', 'df_s']
    DF_DATASET = df_n.merge(df_s)
    DF_DATASET = DF_DATASET.drop(columns=['df_n', 'df_s'])
    # Now add a column with the date string
    DF_DATASET['date'] = df[['month','day','year']].astype(str).agg('-'.join, axis=1)
    df['date'] = df[['month','day','year']].astype(str).agg('-'.join, axis=1)
    # create dayof the year column

    DF_DATASET['dayofyear'] = hlp.day_of_year_getter(DF_DATASET['date'])
    print('Data Prepped Successfully')
    return DF_DATASET, df

def get_avgs(df):
    # group rows by year and month and average the corresponding values
    avg_df = df.groupby(['year','month','hemisphere']).agg([np.average])
    # set index
    avg_df.index = avg_df.index.set_names(['year', 'month', 'hemisphere'])
    # reset index to fill in vals
    avg_df.reset_index(inplace=True)
    # rename cols
    avg_df.columns = ['year', 'month', 'hemisphere', 'dayavg', 'extentavg', 'missingavg']
    # remove nulls if any
    avg_df.dropna()
    print('Average DataFrame Created')
    return avg_df

def prep_bydoy(DF_DATASET):
    # lets prep the list
    year_list = {}
    year_list_s = {}
    # this puts each year into its own list in the year_list dict
    for year in range(1979, 2015, 5):
        item = DF_DATASET[DF_DATASET['year'] == year]
        year_list[year] = {}
        year_list_s[year] = {}
        for dayofyear in range(1, 366):
            n_it = item[item['dayofyear'] == dayofyear]

            s_it_n = None
            n_it_n = None
            try:
                n_it_n = n_it['n_extent'].values.item()
            except:
                n_it_n = None
            try:
                s_it_n = n_it['s_extent'].values.item()
            except:
                s_it_n = None
            year_list[year][dayofyear] = n_it_n
            year_list_s[year][dayofyear] = s_it_n

    # output is 1979, 1980, etc
    df_yls = pd.DataFrame(data=year_list_s).transpose()
    df_yln = pd.DataFrame(data=year_list).transpose()
    

    return df_yls, df_yln
