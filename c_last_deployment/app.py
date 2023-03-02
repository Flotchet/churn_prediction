from flask import Flask, render_template, request, Markup
from flask_sqlalchemy import SQLAlchemy
from waitress import serve
import pickle
import os
import pandas as pd
import datetime

from ml_model import create_ml_model

import os
import sqlite3
import pandas
import pickle
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import PolynomialFeatures
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.compose import make_column_selector as selector

app = Flask(__name__, template_folder='templates', static_folder='templates/assets')

def models_loader() -> dict[str : any]:
    #get the all the file name in the model folder 
    models = {} 
    for file in os.listdir('models'):
        if file.endswith(".pickle"):
            name = file[:-7]
            models[name] = pickle.load(open(f'models/{file}', 'rb'))

    return models

@app.route('/')
def form():
    return render_template('index.html', result=Markup(f"<h1> See if the client is likely to churn </h1>"))

@app.route('/', methods=['POST', 'post'])
def result():

    #get the data from the form
    errors = ""
    r = ""

    if request.form['Client_ID'] == "" or request.form['Client_ID'] == None:
        
        try:
            Total_Relationship_Count = int(request.form['Total_Relationship_Count'])
        except:
            Total_Relationship_Count = 0
            errors += "Warning error during converting"

        try:
            Credit_Limit = float(request.form['Credit_Limit'])
        except:
            Credit_Limit = 0
            errors += "Warning error during converting"

        try:
            Total_Revolving_Bal = float(request.form['Total_Revolving_Bal'])
        except:
            Total_Revolving_Bal = 0
            errors += "Warning error during converting"

        try:
            Avg_Open_To_Buy = float(request.form['Avg_Open_To_Buy'])
        except:
            Avg_Open_To_Buy = 0
            errors += "Warning error during converting"

        try:
            Total_Trans_Amt = float(request.form['Total_Trans_Amt'])
        except:
            Total_Trans_Amt = 0
            errors += "Warning error during converting"

        try:
            Total_Trans_Ct = int(request.form['Total_Trans_Ct'])
        except:
            Total_Trans_Ct = 0
            errors += "Warning error during converting"

        data = pd.DataFrame({
        'Total_Relationship_Count': [Total_Relationship_Count],
        'Credit_Limit': [Credit_Limit],
        'Total_Revolving_Bal': [Total_Revolving_Bal],
        'Avg_Open_To_Buy': [Avg_Open_To_Buy],
        'Total_Trans_Amt' : [Total_Trans_Amt],
        'Total_Trans_Ct' : [Total_Trans_Ct]
        })

        #predict
        if clf.predict(data)[0] != 'Attrited Customer':
            r = 'not '

        return render_template('index.html', result=Markup(f"<h1> The client is {r}likely to churn </h1>") + errors)


    try:
        Client_ID = int(request.form['Client_ID'])
    except:
        Client_ID = 0
        errors += "Warning error during converting"


        
    data = db.loc[db['CLIENTNUM'] == Client_ID]

    if data.empty:
        return render_template('index.html', result=Markup(f"<h1> The client is not in the database </h1>"))

    if clf.predict(data)[0] != 'Attrited Customer':
        r = 'not '

    return render_template('index.html', result=Markup(f"<h1> The client is {r}likely to churn </h1>") + errors)

    




    
    


    

database = "database/database.db"

#serve(app, host="0.0.0.0", port=8080)
#load the csv in a data frame

models : dict[str:any] = models_loader()
clf : Pipeline = create_ml_model()

conn = sqlite3.connect(database)
db = pandas.read_sql('SELECT CLIENTNUM, Attrition_Flag, Total_Relationship_Count, Credit_Limit, Total_Revolving_Bal, Avg_Open_To_Buy, Total_Trans_Amt, Total_Trans_Ct FROM bank_churners', conn)
for model in models.keys():
    print(f"model {model} loaded")

app.run(debug=False)