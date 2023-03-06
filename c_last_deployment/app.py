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

import hashlib

app = Flask(__name__, template_folder='templates', static_folder='templates/assets')

def models_loader() -> dict[str : any]:
    #get the all the file name in the model folder 
    models = {} 
    for file in os.listdir('models'):
        if file.endswith(".pickle"):
            name = file[:-7]
            models[name] = pickle.load(open(f'models/{file}', 'rb'))

    return models


def password_handling(user : str, password : str):
    #check if the user is in the database
    #if not create a new user
    #if yes check the password
    #if the password is correct return True
    #if the password is incorrect return False
    #if the user is not in the database return False

    #check if the table exist
    conn = sqlite3.connect('database/database.db')
    data = pandas.read_sql("SELECT name FROM sqlite_master WHERE type='table' AND name='users'", conn)
    if data.empty:
        #create the table
        conn.execute("CREATE TABLE users (USERNAME TEXT, ENCRYPTED_PASSWORD TEXT)")
        conn.commit()

    #check if the user is in the database
    data = pandas.read_sql(f"SELECT * FROM users WHERE USERNAME = '{user}'", conn)

    if data.empty:
        #create a new user
        #encrypt the password
        password = hashlib.sha256(password.encode()).hexdigest()

        #add the user to the database
        conn.execute(f"INSERT INTO users (USERNAME, ENCRYPTED_PASSWORD) VALUES ('{user}', '{password}')")
        conn.commit()
        return True

    #check the password
    if data['ENCRYPTED_PASSWORD'].values[0] == hashlib.sha256(password.encode()).hexdigest():
        return True

    return False
    
@app.route('/')
def form():
    return render_template('index.html', result=Markup(f"<h1> See if the client is likely to churn </h1>"), graphs = "ACCESS DENIED")

@app.route('/', methods=['POST', 'post'])
def result():

    #get the data from the form
    errors = ""
    r = ""
    if request.form['ID'] != "" and request.form['ID'] != None and request.form['password'] != "" and request.form['password'] != None:
        if not password_handling(request.form['ID'], request.form['password']):
            return render_template('index.html', result=Markup(f"<h1> Wrong username or password </h1>", graphs = "ACCESS DENIED"))    
    else:
        return render_template('index.html', result=Markup(f"<h1> empty username or password </h1>", graphs = "ACCESS DENIED"))
 
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

        return render_template('index.html', result=Markup(f"<h1> The client is {r}likely to churn </h1>") + errors, graphs = graph)


    try:
        Client_ID = int(request.form['Client_ID'])
    except:
        Client_ID = 0
        errors += "Warning error during converting"


        
    data = db.loc[db['CLIENTNUM'] == Client_ID]

    if data.empty:
        return render_template('index.html', result=Markup(f"<h1> The client is not in the database </h1>", graphs = graph))

    if clf.predict(data)[0] != 'Attrited Customer':
        r = 'not '

    return render_template('index.html', result=Markup(f"<h1> The client is {r}likely to churn </h1>") + errors, graphs = graph)

    




    
    


    

database = "database/database.db"

#serve(app, host="0.0.0.0", port=8080)
#load the csv in a data frame

graph = Markup("""
	<div class='tableauPlaceholder' id='viz1677705562080' style='position: relative'><noscript><a href='#'><img alt='Tableau de bord 1 ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Cl&#47;Cluster_16775116554160&#47;Tableaudebord1&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='Cluster_16775116554160&#47;Tableaudebord1' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Cl&#47;Cluster_16775116554160&#47;Tableaudebord1&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='fr-FR' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1677705562080');                    var vizElement = divElement.getElementsByTagName('object')[0];                    if ( divElement.offsetWidth > 800 ) { vizElement.style.minWidth='755px';vizElement.style.maxWidth='1355px';vizElement.style.width='100%';vizElement.style.minHeight='287px';vizElement.style.maxHeight='1087px';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';} else if ( divElement.offsetWidth > 500 ) { vizElement.style.minWidth='755px';vizElement.style.maxWidth='1355px';vizElement.style.width='100%';vizElement.style.minHeight='287px';vizElement.style.maxHeight='1087px';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';} else { vizElement.style.width='100%';vizElement.style.height='1127px';}                     var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>
	<div class='tableauPlaceholder' id='viz1677746820346' style='position: relative'><noscript><a href='#'><img alt='Tableau de bord 2 ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;In&#47;Income_16777458109470&#47;Tableaudebord2&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='Income_16777458109470&#47;Tableaudebord2' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;In&#47;Income_16777458109470&#47;Tableaudebord2&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='fr-FR' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1677746820346');                    var vizElement = divElement.getElementsByTagName('object')[0];                    if ( divElement.offsetWidth > 800 ) { vizElement.style.minWidth='755px';vizElement.style.maxWidth='1355px';vizElement.style.width='100%';vizElement.style.minHeight='287px';vizElement.style.maxHeight='1087px';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';} else if ( divElement.offsetWidth > 500 ) { vizElement.style.minWidth='755px';vizElement.style.maxWidth='1355px';vizElement.style.width='100%';vizElement.style.minHeight='287px';vizElement.style.maxHeight='1087px';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';} else { vizElement.style.width='100%';vizElement.style.height='1027px';}                     var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>								</section>
""")

models : dict[str:any] = models_loader()
clf : Pipeline = create_ml_model()

conn = sqlite3.connect(database)
db = pandas.read_sql('SELECT CLIENTNUM, Attrition_Flag, Total_Relationship_Count, Credit_Limit, Total_Revolving_Bal, Avg_Open_To_Buy, Total_Trans_Amt, Total_Trans_Ct FROM bank_churners', conn)
for model in models.keys():
    print(f"model {model} loaded")

app.run(debug=False)