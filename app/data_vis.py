import json
import plotly
import plotly.plotly as py
import plotly.graph_objs as go

# def plotly_scatter_plot(df,_month, _day, _year):
#     day_of_year = single_day_oy_getter(_year,_month,_day)
#
#     yr_list = []
#     # generate a list with the start and end dates to be plotted.
#     for i in range(start, end, rate):
#         yr_list.append(i)
#     df_1980 - df[df['year'].isin(yr_list)]
#     fig = plotly.make_subplots(specs=[[{"secondary_y": True}]])
#     fig.add_trace(
#         go.Scatter(x=df['dayofyear'], y=df['n_extent'], name="NorthExtents"),
#         secondary_y=False,
#     )
#     fig.add_trace(
#         go.Scatter(x=df['dayofyear'], y=df['s_extent'], name="SouthExtents"),
#         secondary_y=True,
#     )
#     fig.show()


#### CODE
# @app.route('/<Whatever Route>')
# def line():
# 	count = 500
#
# 	xScale = np.linspace(0, 100, count)
# 	yScale = np.random.randn(count)
#
# 	# Create a trace
# 	trace = go.Scatter(x = xScale,y = yScale)
#   # create a list of the trace
# 	data = [trace]
#   # Create a dump of the data list
# 	graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
#   # pass graphJSON
# 	return render_template('index.html', graphJSON=graphJSON)

###########
