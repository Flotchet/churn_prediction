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

def create_ml_model(database_path : str = "database",
                    database_name : str = "database.db") -> Pipeline:

    database = os.path.join(database_path, database_name)

    conn = sqlite3.connect(database)

    # code added for ml model
    df = pandas.read_sql('SELECT Attrition_Flag, Total_Relationship_Count, Credit_Limit, Total_Revolving_Bal, Avg_Open_To_Buy, Total_Trans_Amt, Total_Trans_Ct FROM bank_churners', conn)
    conn.close()
   
    numeric_transformer = Pipeline(steps=[('poly', PolynomialFeatures(degree =2)), ('scaler', StandardScaler())])
    categorical_transformer = Pipeline(steps=[('onehot', OneHotEncoder(handle_unknown='ignore'))])

    preprocessor = ColumnTransformer(transformers=[
            ('num', numeric_transformer, selector(dtype_exclude="category")),
            ('cat', categorical_transformer, selector(dtype_include="category"))])
    clf = Pipeline(steps=[('preprocessor', preprocessor),('classifier',  DecisionTreeClassifier(max_depth=12, random_state=1))])
    X = df[['Total_Relationship_Count', 'Credit_Limit', 'Total_Revolving_Bal', 'Avg_Open_To_Buy', 'Total_Trans_Amt', 'Total_Trans_Ct']]
    y = df[['Attrition_Flag']]
    clf.fit(X, y)
    print(clf.score(X,y))
    
    # Saving model to pickle file  Dump function is used to write the object into the created file in byte format
    with open("models/churn_model.pickle", "wb") as file:
        pickle.dump(clf, file)
        
    '''
    frame = {'Total_Relationship_Count':5, 'Credit_Limit':12691.0 ,'Total_Revolving_Bal':777, 'Avg_Open_To_Buy':11914.0, 'Total_Trans_Amt':1144, 'Total_Trans_Ct':42}
    data_frame = pandas.DataFrame([frame])
   
    with open("churn_model.pkl", "rb") as file:
        model = pickle.load(file)

    print("The client is", model.predict(data_frame)[0])
    print("The probability:", round(list(model.predict_proba(data_frame)[:,1])[0],2),'%')
    '''
    
    return clf


if __name__ == "__main__":
    create_ml_model()
