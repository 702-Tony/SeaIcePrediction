import pandas as pd

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
# from app.main import DF_DATASET, df
from app.helpers import *


# Build MODELS for North and South Prediction


def get_linear_pred(DF_DATASET):
    X = DF_DATASET[['year', 'month', 'day', 'dayofyear']]
    n_y = DF_DATASET[['n_extent']]
    s_y = DF_DATASET[['s_extent']]

    N_L_REGR = LinearRegression(normalize=True).fit(X, n_y)
    S_L_REGR = LinearRegression(normalize=True).fit(X, s_y)
    return N_L_REGR, S_L_REGR


def get_prediction(month_, day_, year_, DF_DATASET, N_L_REGR, S_L_REGR):
    date_to_pred = str(month_).zfill(2) + "-" + str(day_).zfill(2) + "-" + str(year_)  # '03-01-2022'
    day_to_predict = Dummy(date_to_pred)
    # list of day of the year values + or - 15 days
    add_subtract_list = get_add_subtract_days(month_, day_, year_, 15)
    df_data = DF_DATASET.loc[(DF_DATASET['dayofyear'].isin(add_subtract_list))]
    # this is will select days that are within the date range + or - 10 days
    X = df_data[['year', 'month', 'day', 'dayofyear']]
    n_y = df_data[['n_extent']]
    s_y = df_data[['s_extent']]
    # North Model Creation and test
    X_train, X_test, y_train, y_test = train_test_split(X, n_y, test_size=0.3, shuffle=True)
    n_l_regr = LinearRegression(normalize=True).fit(X_train, y_train)
    n_score = n_l_regr.score(X_test, y_test)

    # South Model Creation and test
    X_train, X_test, y_train, y_test = train_test_split(X, s_y, test_size=0.3, shuffle=True)
    s_l_regr = LinearRegression(normalize=True).fit(X_train, y_train)
    s_score = s_l_regr.score(X_test, y_test)

    # create an object for the prediction output
    _d = {'year': [int(year_)],
          'month': [int(month_)],
          'day': [int(day_)],
          'dayofyear': day_of_year_getter(day_to_predict)[0]}
    # pass that object for the prediction
    north = N_L_REGR.predict(pd.DataFrame(data=_d))
    south = S_L_REGR.predict(pd.DataFrame(data=_d))
    return north, south, n_score, s_score
