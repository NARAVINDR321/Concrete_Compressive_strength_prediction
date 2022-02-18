"""

code     :::::::     Nambakkam Aravind Rakesh

This is the main  python file which is used to connect front end and back end.
Each and every features and module is routed to this application.

"""

import pickle
import joblib
import numpy as np
import pandas as pd
import os
import sys
import shutil
import plotly.express as ex
import plotly.graph_objects as go
from flask import Flask , render_template , request , jsonify , url_for
import logging




"""Application logging"""


path = str(os.getcwd())


app = Flask(__name__)


model = joblib.load('XGBoost_Regressor_model.pkl')  # loading the saved XGBoost_regressor model

@app.route('/')
def home():
    return render_template('index.html')

#Dataset

@app.route("/dataset", methods=["GET", "POST"])
def dataset():
    try:
        #good_dataset = open(path + "/Model_files/good_data.txt", "w")
        #path="C:\Users\aravi\Downloads\ds class downloads\cementStrengthPrediction\INTERNSHIP_INEURON\Concrete-Compressive-Strength-Prediction\Model_files\good_data.txt"
        #good_dataset=open("path","w")

        good_dataset = open(path + "/Model_files/good_data.txt", "r")
        bad_dataset = open(path + "/Model_files/bad_data.txt", "r")

        return render_template("dataset.html", good_data=str(good_dataset.read()), bad_data=str(bad_dataset.read()))

    except Exception as e:
        return render_template("error.html", text=str(e))

# EDA

@app.route("/eda", methods=["GET", "POST"])
def eda():
        try:
            eda_reader = open(path + "/EDA/Metadata.txt", "r")
            return render_template("eda.html", eda=eda_reader.read())
        except Exception as e:
                logging.info("Faced an error")
                logging.info("eda")
                return render_template("error.html", text=str(e))

# Add dataset

@app.route("/add_data_homepage" , methods = ["GET" , "POST"])
def add_data_homepage():
        try:
            logging.info("Adding external data")
            return render_template("/add_dataset.html")
        except Exception as e:
            logging.info("Faced an error add data homepage")
            return render_template("error.html"  , text = str(e))

@app.route("/history" , methods = ["GET" , "POST"])
def history():
        try:
            log_file = open(path + "/Logger/history.txt" , "r")
            return render_template("history.html" , data = str(log_file.read()))
        except Exception as e:
            logging.info("Faced an error,history")
            return render_template("error.html"  , text = str(e))



@app.route('/predict', methods=['GET', 'POST'])
def predict():
    """
    For rendering results on HTML GUI

    """
    if request.method == "POST":
        # ['age', 'cement', 'water', 'fly_ash', 'superplasticizer', 'blast_furnace_slag']
        f_list = [request.form.get('age'), request.form.get('cement'), request.form.get('water'),
                  request.form.get('fa'),
                  request.form.get('sp'), request.form.get('bfs')]  # list of inputs

        # logging operation
#         logging.info(f"Age (in days): {f_list[0]}, Cement (in kg): {f_list[1]},"
#                      f"Water (in kg): {f_list[2]}, Fly ash (in kg): {f_list[3]},"
#                      f"Superplasticizer (in kg): {f_list[4]}, Blast furnace slag (in kg): {f_list[5]}")

        final_features = np.array(f_list).reshape(-1, 6)
        df = pd.DataFrame(final_features)

        prediction = model.predict(df)
        result = "%.4f" % round(prediction[0], 2)

        # logging operation
#         logging.info(f"The Predicted Concrete Compressive strength is {result} MPa")

#         logging.info("Prediction getting posted to the web page.")
        return render_template('index.html',
                               prediction_text=f"The Concrete compressive strength is {result} MPa")


if __name__ == "__main__":
    app.run(debug=True)
