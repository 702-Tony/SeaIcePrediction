from flask import Flask, render_template, request
from app.linear_regr import *
from app.data_vis import *

app = Flask(__name__)

# _date = None # date to be predicted

@app.route("/", methods = ["GET","POST"])
def home_view():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard_view():
    # create K Means Clustering and build visualizations
    # uses df to create violing plots
    viol = violin_plot(1980, 2015, 5)
    # perhaps I can create a drop down for each val and create a plot on the fly


    line_p = get_line_plot()
    return render_template("admin_dboard.html", viol=viol, line_p = line_p)
# use K Nearest Neighbor
@app.route("/prediction", methods=['POST','GET'])
def prediction():
    if request.method == 'POST':
        # this is where you get the info from the current form
        # before loading the next template
        # as well as pass along the information
        result=request.form.get('predict_date')
        # here is where I do my python work
        date_obj = date_transformer(result) # returns a datetime obj
        month_ = date_obj.month
        day_ = date_obj.day
        year_ = date_obj.year
        doy = date_obj.timetuple().tm_yday
        north, south, n_score, s_score = get_prediction(month_, day_, year_)
        plotly_img = plotly_scatter_plot(month_,day_,year_)
        png_img = get_p(month_, day_, year_) # get_pred_plots(month_, day_, year_)
        return render_template('prediction.html', result=result, north=north, south=south, n_score=n_score, s_score=s_score, plot_=png_img, doy=doy, plotly_img=plotly_img)

def get_p(_month, _day, _year):
    # gets a prediction for the date passed in from the webpage
    # and returns a png image encoded as a base64 string
    day_of_year = single_day_oy_getter(_year,_month, _day)
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    n_prediction = N_L_REGR.predict([[_year, _month, _day ,day_of_year]])
    s_prediction = S_L_REGR.predict([[_year, _month, _day ,day_of_year]])
    add_subtract_list = get_add_subtract_days(_month, _day, _year, 15)
    df_data = DF_DATASET.loc[(DF_DATASET['dayofyear'].isin(add_subtract_list))]
    X = df_data[['dayofyear']]
    y_n = df_data[['n_extent']]
    s_n = df_data[['s_extent']]
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.set_title("Prediction")
    axis.set_xlabel("Day of Year")
    axis.set_ylabel("Extents")
    # axis.grid()
    axis.scatter(X, y_n, s=10, alpha=0.5, label='Northern Historical')
    axis.scatter(X, s_n, s=10, alpha=0.5, c='g', label='Southern Historical')
    axis.scatter(day_of_year, n_prediction, s=20, c='r')
    axis.scatter(day_of_year, s_prediction, s=20, c='purple')
    _bBox= dict(facecolor='white',edgecolor='black', pad=0.5)
    axis.text(day_of_year+.5, n_prediction, "Northern Prediction", fontweight='bold', bbox=_bBox)
    axis.text(day_of_year+.5, s_prediction, "Southern Prediction", fontweight='bold', bbox=_bBox)
    axis.legend()
    pngImage = io.BytesIO()
    FigureCanvas(fig).print_png(pngImage)
    # Encode PNG image to base64 string
    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
    return pngImageB64String

def violin_plot(start, end, rate):
    # this will generate a violin plot using the df dataframe
    # this dataframe is closes to the row data in that it does not have the
    # extent data split between columns and allows for easier plotting
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    yr_list = []
    # generate a list with the start and end dates to be plotted.
    for i in range(start, end, rate):
        yr_list.append(i)

    df_1980 = df[df['year'].isin(yr_list)]

    fig,ax = plt.subplots(figsize=(6,6))
    sns.violinplot(x='year', y='extent', data=df_1980, hue='hemisphere', split=True)
    canvas=FigureCanvas(fig)
    png_img = io.BytesIO()
    fig.savefig(png_img)
    png_img.seek(0)

    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(png_img.getvalue()).decode('utf8')
    return pngImageB64String

def get_pred_plots(_month, _day, _year):
    n_plots = []
    s_plots = []
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    for i in range(1, 13):
        # appends X_test, y_test, pr, prediction
        n_plots.append(list(get_prediction_plot(i, _day, _year, 'n_extent')))
        s_plots.append(list(get_prediction_plot(i, _day, _year, 's_extent')))

    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.set_title("Prediction")
    axis.set_xlabel("Day of Year")
    axis.set_ylabel("Extents")
    axis.grid()
    for i in range(len(n_plots)):
        X_test = n_plots[i][0]
        y_test = n_plots[i][1]
        pr = n_plots[i][2]
        ########

        axis.scatter(X_test['dayofyear'], y_test['n_extent'], c='b', s=1, alpha=0.5, label='Actual'if i == 0 else "")
        axis.scatter(X_test['dayofyear'], pr, c='r', s=1, alpha=0.5, label='Predicted'if i == 0 else "")

        ########
    for i in range(len(s_plots)):
        X_test = s_plots[i][0]
        y_test = s_plots[i][1]
        pr = s_plots[i][2]
        ########

        axis.scatter(X_test['dayofyear'], y_test['s_extent'], c='b', s=1, alpha=0.5)
        axis.scatter(X_test['dayofyear'], pr, c='r', s=1, alpha=0.5)

        ########
    # day_oy = day_of_year_getter(Dummy(str(_month).zfill(2)+"-"+str(_day).zfill(2)+"-"+str(_year)))
    day_list = [[x for x in range(1,365)]]
    axis.legend()

    # Generate plot


    # Convert plot to PNG image
    pngImage = io.BytesIO()
    FigureCanvas(fig).print_png(pngImage)

    # Encode PNG image to base64 string
    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
    return pngImageB64String

def get_line_plot():
    # returns  a line plot of all of the dataset
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    # Red is north extent
    fig, ax = plt.subplots(figsize=(8,6))
    plt.plot(DF_DATASET['date'].index, DF_DATASET['n_extent'], c='lightcoral', label='North Extent')
    # Blue is south extent
    plt.plot(DF_DATASET['date'].index, DF_DATASET['s_extent'], c='slateblue', label='South Extent', markersize=3)
    ax.set_xlabel('Days since 1978-10-26')
    ax.set_ylabel('Extent')
    plt.grid()

    legend = ax.legend()
    canvas=FigureCanvas(fig)
    png_img = io.BytesIO()
    fig.savefig(png_img)
    png_img.seek(0)
    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(png_img.getvalue()).decode('utf8')
    return pngImageB64String

def plotly_scatter_plot(_month, _day, _year):

    day_of_year = single_day_oy_getter(_year,_month,_day)
    n_prediction = N_L_REGR.predict([[_year, _month, _day ,day_of_year]])
    s_prediction = S_L_REGR.predict([[_year, _month, _day ,day_of_year]])
    add_subtract_list = get_add_subtract_days(_month, _day, _year, 15)
    df_data = DF_DATASET.loc[(DF_DATASET['dayofyear'].isin(add_subtract_list))]
    X = df_data[['dayofyear']]
    y_n = df_data[['n_extent']]
    s_n = df_data[['s_extent']]
    n_prediction = N_L_REGR.predict([[_year, _month, _day ,day_of_year]])
    s_prediction = S_L_REGR.predict([[_year, _month, _day ,day_of_year]])

    # hovertemplate =
    # '<i>Price</i>: $%{y:.2f}'+
    # '<br><b>X</b>: %{x}<br>'+
    # '<b>%{text}</b>',
    trace = go.Scatter(
        x=df_data['dayofyear'],
        y=df_data['n_extent'],
        opacity=0.6,
        hovertemplate ='<i>Extent</i>: %{y:.2f}'+
        '<br><b>Day of Year</b>: %{x}<br>'+
        '<b>%{text}</b>',
        text=df_data['date'],
        name="North")
    trace2 = go.Scatter(x=df_data['dayofyear'], y=df_data['s_extent'], opacity=0.6,
        hovertemplate='<i>Extent</i>: %{y:.2f}'+
        '<br><b>Day of Year</b>: %{x}<br>'+
        '<b>%{text}</b>',
        text=df_data['date'],
        name="South")
    prediction = go.Scatter(x=[day_of_year], y=[n_prediction] )
    # prediction_s = go.Scatter(x=day_of_year, y=s_prediction)
    data = [trace, trace2, prediction] #, prediction_s]
    graph_json = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    # return  html.Div([dcc.Graph(figure=fig)])
    return graph_json
