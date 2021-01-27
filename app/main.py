from flask import Flask, render_template, request

# local file imports
from app.data_vis import *
from app.data_prep import prep_data
from app.linear_regr import *
from app.cluster import *

app = Flask(__name__)
# create DataFrame Objects
DF_DATASET, df = prep_data('app/dataset/seaice.csv')
n_clusters = 4
DF_DATASET, kmeans_model = k_cluster_data(DF_DATASET, n_clusters)
N_L_REGR, S_L_REGR = get_linear_pred(DF_DATASET)
print('#######'*3,'DF_DATASET','#######'*3)
print(DF_DATASET.head())


@app.route("/", methods = ["GET","POST"])
def home_view():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard_view():
    # create K Means Clustering and build visualizations
    # uses df to create violing plots
    # viol = violin_plot(1980, 2015, 5)
    # perhaps I can create a drop down for each val and create a plot on the fly
    plotly_viol = plotly_violin_plot(1980,2015,5,df)

    # line_p = get_line_plot()
    line_p = 'LinePlotPlaceholder' # to be changed out with plotly line plot
    return render_template("admin_dboard.html", line_p = line_p, plotly_viol=plotly_viol)
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
        north, south, n_score, s_score = get_prediction(month_, day_, year_, DF_DATASET, N_L_REGR, S_L_REGR)
        plotly_scatter = plotly_scatter_plot(month_,day_,year_, DF_DATASET, N_L_REGR, S_L_REGR)
        return render_template('prediction.html', result=result, north=north, south=south, n_score=n_score, s_score=s_score, doy=doy, plotly_scatter=plotly_scatter)



# def get_line_plot():
#     # returns  a line plot of all of the dataset
#     from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
#     from matplotlib.figure import Figure
#     # Red is north extent
#     fig, ax = plt.subplots(figsize=(8,6))
#     plt.plot(DF_DATASET['date'].index, DF_DATASET['n_extent'], c='lightcoral', label='North Extent')
#     # Blue is south extent
#     plt.plot(DF_DATASET['date'].index, DF_DATASET['s_extent'], c='slateblue', label='South Extent', markersize=3)
#     ax.set_xlabel('Days since 1978-10-26')
#     ax.set_ylabel('Extent')
#     plt.grid()
#
#     legend = ax.legend()
#     canvas=FigureCanvas(fig)
#     png_img = io.BytesIO()
#     fig.savefig(png_img)
#     png_img.seek(0)
#     pngImageB64String = "data:image/png;base64,"
#     pngImageB64String += base64.b64encode(png_img.getvalue()).decode('utf8')
#     return pngImageB64String
