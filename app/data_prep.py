import pandas as pd
import app.helpers as hlp



def prep_data(source):

    # PREPARE DATASET
    df = pd.read_csv(source)

    # rename columns
    df.columns = ['year', 'month','day', 'extent','missing','source_data','hemisphere']
    print(df.columns)
    # remove unnecessary columns
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
    return DF_DATASET, df
