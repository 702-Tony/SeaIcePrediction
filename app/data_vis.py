import json

import numpy as np
import plotly
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


def plotly_heatmap(avg_df, hemisphere):
    template_str = '<b>Extent</b>: %{z:.2f}' + '<br><b>Year</b>: %{x}<br>' + '<b>Month</b>: %{y}'
    # takes a string as hemisphere and returns a heatmap JSON
    avgs = avg_df[avg_df['hemisphere'] == hemisphere]
    heat = go.Heatmap(x=avgs['year'],
                      y=avgs['month'],
                      z=avgs['extentavg'],
                      hovertemplate=template_str,
                      colorscale='Viridis',
                      name='<b>'+hemisphere.capitalize()+'</b>')
    data = [heat]
    graph_json = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return graph_json

def plotly_kmeans_scatter(DF_DATASET):
    # this will plot the Dataset with the kmeans cluster from data that was
    # transformed so that each year was on an evenly matched 366 day year of values
    tr_df = DF_DATASET.transpose()
    tr_df.columns = tr_df.iloc[0]
    tr_df.drop(['year'], inplace=True)
    tr_df.reset_index(inplace=True)
    tr_df.drop(columns=['index'], inplace=True)

    charts = []
    for i in range(1979, 2018):
        X = tr_df[i].index[:-1]
        Y = tr_df[i][:-1]
        cluster = int(tr_df[i][366].item())
        colrs = ['#0d0887', '#46039f', '#7201a8', '#9c179e']
        charts.append(
            go.Scatter(x=X,
                       y=Y,
                       marker=dict(
                           color=colrs[cluster],
                           # colorscale='Viridis'
                       ),
                       legendgroup=cluster,
                       opacity=0.6,
                       mode='lines',
                       text=i,
                       name=i

                       )
        )
    data = charts
    graph_json = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return graph_json

# Create a dataframe with the DF_DATASET dataframe and averages made up from that
def plotly_bar_plots(DF_DATASET, s):
    df_year = DF_DATASET
    df_year_agg = df_year.groupby(['year','month']).agg([np.average])
    df_year_agg.index = df_year_agg.index.set_names(['year', 'month'])
    # reset index to fill in vals
    df_year_agg.reset_index(inplace=True)
    # rename cols
    df_year_agg.columns = ['year','month','dayavg','n_ext','n_miss','s_ext','s_miss','dayoyavg','cls']
    df_year_agg.head()

    years = [1980,1985,1990, 1995, 2000, 2005, 2010, 2015, 2018]
    data = []
    data2 = []
    # bar plot of extent values for each month of each year
    for year in years:
        df_year = df_year_agg[df_year_agg['year']==year]
        north = str(year) + ' North'
        data.append(go.Bar(
            y=df_year['n_ext'],
            x=df_year['month'],
            name=north
        ))
        south = str(year) + ' South'
        data2.append(go.Bar(
            y=df_year['s_ext'],
            x=df_year['month'],
            name=south
        ))
    data = go.Figure(data=data)
    data2 = go.Figure(data=data2)
    n_graph_json = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    s_graph_json = json.dumps(data2, cls=plotly.utils.PlotlyJSONEncoder)
    return n_graph_json, s_graph_json
