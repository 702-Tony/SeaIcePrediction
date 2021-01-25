import json
import plotly
import plotly.plotly as py
import plotly.graph_objs as go

from app.linear_regr import *
# creates a plotly scatter plot with historical and predicted data
def plotly_scatter_plot(_month, _day, _year):
    day_of_year = single_day_oy_getter(_year,_month,_day)
    # get days to plot
    add_subtract_list = get_add_subtract_days(_month, _day, _year, 15)
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
def plotly_violin_plot(start, end, rate):
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
