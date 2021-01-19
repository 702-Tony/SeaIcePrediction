from flask import Flask, render_template, request
from app.linear_regr import *


app = Flask(__name__)

# _date = None # date to be predicted

@app.route("/", methods = ["GET","POST"])
def home_view():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard_view(name=None):
    return render_template("admin_dboard.html", name=name)
# use K Nearest Neighbor
@app.route("/prediction", methods=['POST','GET'])
def prediction():
    if request.method == 'POST':
        # this is where you get the info from the current form
        # before loading the next template
        # as well as pass along the information
        result=request.form.get('predict_date')
        # here is where I do my python work
        date_obj = date_transformer(result)
        month_ = date_obj.month
        day_ = date_obj.day
        year_ = date_obj.year
        north, south = get_prediction(month_, day_, year_)

        return render_template('prediction.html', result=result, north=north, south=south)
