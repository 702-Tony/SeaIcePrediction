from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home_view(name=None):
    return render_template("index.html", name=name)

# use K Nearest Neighbor
