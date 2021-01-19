import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

class Dummy:
    def __init__(self, _val):
        self.values = []
        self.values.append(_val)


print('Hello World!')
print('linear_regr loaded!', flush=True)
def date_transformer(date_str):
    # this returns a date time obj
    format = '%Y-%m-%d'
    new_date = datetime.strptime(date_str, format)
    return new_date

def day_of_year_getter(date_vals):
    # takes in an object with a list stored in the values attribute
    str_list = date_vals.values
    rt_list = []
    for date_str in str_list:
        date_format = '%m-%d-%Y'
        current_date = datetime.strptime(date_str, date_format)
        # day_delta = current_date - START_DATE
        day_delta = current_date.timetuple().tm_yday
        rt_list.append(day_delta)
    return rt_list

# PREPARE DATASET
DF_DATASET = pd.read_csv('app/dataset/seaice_fixed_sep_extent2.csv')
# create dayof the year column
DF_DATASET['dayofyear'] = day_of_year_getter(DF_DATASET['date'])
# Build MODELS for North and South Prediction
X = DF_DATASET[['year','month','day','dayofyear']]
n_y = DF_DATASET[['n_extent']]
s_y = DF_DATASET[['s_extent']]

N_L_REGR = LinearRegression(normalize=True).fit(X, n_y)
S_L_REGR = LinearRegression(normalize=True).fit(X, s_y)



def day_of_year_add_subtract(date_str, _days):
    # takes in date string
    date_format = '%m-%d-%Y'
    current_date = datetime.strptime(date_str, date_format)

    rt_list = []
    plus_day = current_date + timedelta(days=_days)
    rt_list.append(plus_day.timetuple().tm_yday)
    minus_day = current_date - timedelta(days=_days)
    rt_list.append(minus_day.timetuple().tm_yday)
    # returns a list with 0 = plus_day and 1 = minus_day
    return rt_list

def get_add_subtract_days(date_str, _days):
    # this will return a list of daysofyear
    date_format = '%m-%d-%Y'
    current_date = datetime.strptime(date_str, date_format)
    rt_list = []
    rt_list.append(current_date.timetuple().tm_yday)
    for d in range(1, _days+1):
        rt_list.append((current_date + timedelta(days=d)).timetuple().tm_yday)
        rt_list.append((current_date - timedelta(days=d)).timetuple().tm_yday)
    return rt_list
def get_prediction(month_, day_, year_):
    date_to_pred = str(month_).zfill(2)+"-"+str(day_).zfill(2)+"-"+str(year_)# '03-01-2022'
    day_to_predict = Dummy(date_to_pred)
    # list of day of the year values + or - 15 days
    add_subtract_list = get_add_subtract_days(date_to_pred, 15)
    df_data = DF_DATASET.loc[(DF_DATASET['dayofyear'].isin(add_subtract_list))]
    # this is will select days that are within the date range + or - 10 days
    X = df_data[['year','month','day','dayofyear']]
    n_y = df_data[['n_extent']]
    s_y = df_data[['s_extent']]
    n_l_regr = LinearRegression(normalize=True).fit(X, n_y)
    s_l_regr = LinearRegression(normalize=True).fit(X, s_y)
    # create an object for the prediction output
    _d = {'year': [int(year_)],
      'month': [int(month_)],
      'day' : [int(day_)],
     'dayofyear': day_of_year_getter(day_to_predict)[0]}
    # pass that object for the prediction
    north = N_L_REGR.predict(pd.DataFrame(data=_d))
    south = S_L_REGR.predict(pd.DataFrame(data=_d))
    return north, south

def get_prediction_plot(month_, day_, year_, extent_val):
    # the purpose of the function is to return a scatter plot dataset to be plotted as well as a prediction for the actual day
    date_to_pred = str(month_).zfill(2)+"-"+str(day_).zfill(2)+"-"+str(year_)# '03-01-2022'
    day_to_predict = Dummy(date_to_pred)
    # list of day of the year values + or - 15 days
    add_subtract_list = get_add_subtract_days(date_to_pred, 15)
    df_data = DF_DATASET.loc[(DF_DATASET['dayofyear'].isin(add_subtract_list))]
    # this is will select days that are within the date range + or - 10 days
    X = df_data[['year','month','day','dayofyear']]
    y = df_data[[extent_val]]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, shuffle=True)
    n_l_regr = LinearRegression(normalize=True).fit(X_train, y_train)
    pr = n_l_regr.predict(X_test)
    # create an object for the prediction output
    _d = {'year': [year_],
      'month': [month_],
      'day' : [day_],
     'dayofyear': day_of_year_getter(day_to_predict)[0]}
    # pass that object for the prediction
    prediction = n_l_regr.predict(pd.DataFrame(data=_d))
    return X_test, y_test, pr, prediction
