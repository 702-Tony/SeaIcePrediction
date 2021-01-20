from flask import Flask, render_template, request
from app.linear_regr import *


app = Flask(__name__)

# _date = None # date to be predicted

@app.route("/", methods = ["GET","POST"])
def home_view():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard_view():
    # create K Means Clustering and build visualizations


    return render_template("admin_dboard.html")
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
        png_img = get_p(month_, day_, year_) # get_pred_plots(month_, day_, year_)
        return render_template('prediction.html', result=result, north=north, south=south, n_score=n_score, s_score=s_score, plot_=png_img, doy=doy)

def get_p(_month, _day, _year):
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
