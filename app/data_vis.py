import json
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import app.helpers as hlp


# creates a plotly scatter plot with historical and predicted data
def plotly_scatter_plot(_month, _day, _year, DF_DATASET, N_L_REGR, S_L_REGR):
    day_of_year = hlp.single_day_oy_getter(_year,_month,_day)
    # get days to plot
    add_subtract_list = hlp.get_add_subtract_days(_month, _day, _year, 15)
    # get days from dataset for plot
    df_data = DF_DATASET.loc[(DF_DATASET['dayofyear'].isin(add_subtract_list))]
    X = df_data[['dayofyear']]
    y_n = df_data[['n_extent']]
    s_n = df_data[['s_extent']]
    # get predictions
    n_prediction = N_L_REGR.predict([[_year, _month, _day ,day_of_year]])
    s_prediction = S_L_REGR.predict([[_year, _month, _day ,day_of_year]])
    # for hover templates
    template_str = '<b>Extent</b>: %{y:.2f}' + '<br><b>Day of Year</b>: %{x}<br>' + '<b>Date</b>: %{text}'
    # create scatter plot for northern historical data
    trace = go.Scatter(
        x=df_data['dayofyear'],
        y=df_data['n_extent'],
        opacity=0.6,
        hovertemplate =template_str,
        text=df_data['date'],
        name="<i>Northern Historical</i>",
        mode='markers')
    # create scatter plot for southern historical data
    trace2 = go.Scatter(
        x=df_data['dayofyear'],
        y=df_data['s_extent'],
        opacity=0.6,
        hovertemplate=template_str,
        text=df_data['date'],
        name="<i>Southern Historical</i>",
        mode='markers')
    # create scatter plots for predictions
    import numpy as np
    n_prediction = go.Scatter(
        x=np.array([day_of_year]),
        y=n_prediction[0],
        mode='markers',
        marker = dict(size=[20],color='#3136cc'),
        visible=True,
        name="<b>Northern Prediction</b>")
    s_prediction = go.Scatter(
        x=np.array([day_of_year]),
        y=s_prediction[0],
        mode='markers',
        marker = dict(size=[20], color='#db432c'),
        visible=True,
        name="<b>Southern Prediction</b>")
    # create list of plots
    data = [trace, trace2, n_prediction, s_prediction]
    # create json data for passing to html output
    graph_json = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return graph_json
# creates a violin plot to be used for the data visualizations
def plotly_violin_plot(start, end, rate, df):
    yr_list = []
    # generate a list with the start and end dates to be plotted.
    for i in range(start, end, rate):
        yr_list.append(i)

    data_fr = df[df['year'].isin(yr_list)]

    left = go.Violin(x=data_fr['year'][ data_fr['hemisphere'] == 'north' ],
                        y=df['extent'][ df['hemisphere'] == 'north' ],
                        legendgroup='north', scalegroup='north', name='north',
                        side='negative',
                        line_color='blue')
    right = go.Violin(x=data_fr['year'][ data_fr['hemisphere'] == 'south' ],
                        y=df['extent'][ df['hemisphere'] == 'south' ],
                        legendgroup='south', scalegroup='south', name='south',
                        side='positive',
                        line_color='orange')

    data = [left, right]
    graph_json = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return graph_json

def get_prediction_plot(month_, day_, year_, extent_val):
    # the purpose of the function is to return a scatter plot dataset to be plotted as well as a prediction for the actual day
    date_to_pred = str(month_).zfill(2)+"-"+str(day_).zfill(2)+"-"+str(year_)# '03-01-2022'
    day_to_predict = hlp.Dummy(date_to_pred)
    # list of day of the year values + or - 15 days
    add_subtract_list = hlp.get_add_subtract_days(month_, day_, year_, 15)
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
     'dayofyear': hlp.day_of_year_getter(day_to_predict)[0]}
    # pass that object for the prediction
    prediction = n_l_regr.predict(pd.DataFrame(data=_d))
    return X_test, y_test, pr, prediction

# def get_plots(_year,_month,_day):
#     n_plots = []
#     s_plots = []
#     for i in range(1, 13):
#         n_plots.append(list(get_prediction_plot(i, 1, 1902, 'n_extent')))
#         s_plots.append(list(get_prediction_plot(i, 1, 1902, 's_extent')))
#     for i in range(len(n_plots)):
#         X_test = n_plots[i][0]
#         y_test = n_plots[i][1]
#         pr = n_plots[i][2]
#         plt.scatter(X_test['dayofyear'], y_test['n_extent'], c='b', s=1, alpha=0.5, label='Actual'if i == 0 else "")
#         plt.scatter(X_test['dayofyear'], pr, c='r', s=1, alpha=0.5, label='Predicted'if i == 0 else "")
#     plt.legend()
#     plt.save_fig('./images/predict_001.png')
# fig = go.Figure()
#
# fig.add_trace(go.Violin(x=df['day'][ df['smoker'] == 'Yes' ],
#                         y=df['total_bill'][ df['smoker'] == 'Yes' ],
#                         legendgroup='Yes', scalegroup='Yes', name='Yes',
#                         side='negative',
#                         line_color='blue')
#              )
# fig.add_trace(go.Violin(x=df['day'][ df['smoker'] == 'No' ],
#                         y=df['total_bill'][ df['smoker'] == 'No' ],
#                         legendgroup='No', scalegroup='No', name='No',
#                         side='positive',
#                         line_color='orange')
#              )
# fig.update_traces(meanline_visible=True)
# fig.update_layout(violingap=0, violinmode='overlay')
# fig.show()
