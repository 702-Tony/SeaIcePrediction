from flask import Flask, render_template, request

# local file imports
from app.data_vis import *
from app.data_prep import prep_data, get_avgs
from app.linear_regr import *
from app.cluster import *
from app.helpers import date_transformer

app = Flask(__name__)
# create DataFrame Objects
DF_DATASET, df = prep_data('app/dataset/seaice.csv')
n_clusters = 4
# DF_DATASET, kmeans_model = k_cluster_data(DF_DATASET, n_clusters)
year_col_df_north, year_col_df_south, kmeans_n, kmeans_s = k_cluster_data2(DF_DATASET, n_clusters)
N_L_REGR, S_L_REGR = get_linear_pred(DF_DATASET)
# get Avgs
avg_df = get_avgs(df)
avg_df, avg_kmeans = k_cluster_data(avg_df, n_clusters)

print('#######' * 3, 'DF_DATASET', '#######' * 3)
print(DF_DATASET.head())
print('#######' * 3, 'Averages By Month', '#######' * 3)
print(avg_df.head())


@app.route("/", methods=["GET", "POST"])
def home_view():
    return render_template("index.html")


@app.route("/data_analysis", methods=['POST', 'GET'])
def dashboard_view(DF_DATASET=DF_DATASET):
    # main dashboard view with collected visualizations of data from rawest data set.
    # includes the kmeans plotly plot
    DF_DATASET, kmeans_model = k_cluster_data(DF_DATASET, n_clusters)
    plotly_viol = plotly_violin_plot(1980, 2015, 5, df)
    north_bar_plotly, south_bar_plotly = plotly_bar_plots(DF_DATASET, 'north')
    scatter_plotly = plotly_kmeans_scatter(year_col_df_north)
    return render_template("admin_dboard.html",
                           plotly_viol=plotly_viol,
                           north_bar_plotly=north_bar_plotly,
                           south_bar_plotly=south_bar_plotly,
                           scatter_plotly=scatter_plotly,
                           )


@app.route("/average_analysis")
def average_dash_view():
    # this view will have the data from the dataset that has
    # been transformed from the original and averaged out for each month.
    north_heatmap = plotly_heatmap(avg_df, 'north')
    south_heatmap = plotly_heatmap(avg_df, 'south')
    return render_template("admin_avg_dboard.html",
                           north_heatmap=north_heatmap,
                           south_heatmap=south_heatmap,
                           )


@app.route("/prediction", methods=['POST', 'GET'])
def prediction():
    if request.method == 'POST':
        # this is where you get the info from the date from index.html template
        # before loading the next template
        # as well as pass along the information
        result = request.form.get('predict_date')
        # ORIGINAL
        date_obj = None
        try:
            # parse date
            date_obj = date_transformer(result)  # returns a datetime obj
        except:
            # if that fails then the prediction runs for today
            date_obj = datetime.now()
            result = date_obj.strftime('%Y-%m-%d')
        month_ = date_obj.month
        day_ = date_obj.day
        year_ = date_obj.year
        doy = date_obj.timetuple().tm_yday
        north, south, n_score, s_score = get_prediction(month_, day_, year_, DF_DATASET, N_L_REGR, S_L_REGR)
        print('Prediction queried at', datetime.now())
        print('north prediction for ', month_, '-', day_, '-', year_, ' : ', north[0][0])
        print('north score : ', n_score)
        print('south prediction for ', month_, '-', day_, '-', year_, ' : ', south[0][0])
        print('south score : ', s_score)
        plotly_scatter = plotly_scatter_plot(month_, day_, year_, DF_DATASET, N_L_REGR, S_L_REGR)
        return render_template('prediction.html',
                               result=result,
                               north=north,
                               south=south,
                               n_score=n_score,
                               s_score=s_score,
                               doy=doy,
                               plotly_scatter=plotly_scatter
                               )
