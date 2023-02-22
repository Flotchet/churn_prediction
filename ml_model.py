import sqlite3
import pandas
import os
import warnings
import sqlite3
import pandas
import pickle
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import PolynomialFeatures
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import LabelBinarizer
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

def create_ml_model(database_path : str = "/Users/emiliagenadieva/Desktop/PythonLessons/MLLessons/include/Work/Clusters",
                    database_name : str = "database.db") -> None:

    database = os.path.join(database_path, database_name)

    conn = sqlite3.connect(database)

    # code added for ml model
    df = pandas.read_sql('SELECT Gender, Education_Level, Marital_Status, Income_Category, Card_Category, Credit_Limit, Avg_Utilization_Ratio FROM bank_churners', conn)
    y = pandas.read_sql('SELECT Attrition_Flag FROM bank_churners', conn)
    conn.close()
    
    numeric_features = df.select_dtypes(exclude="object").columns
    numeric_transformer = Pipeline(steps=[('poly', PolynomialFeatures(degree =2)), ('scaler', StandardScaler())])

    categorical_features = df.select_dtypes(include='object').columns
    categorical_transformer = Pipeline(steps=[('onehot', OneHotEncoder(handle_unknown='ignore'))])

    preprocessor = ColumnTransformer(transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)])
    clf = Pipeline(steps=[('preprocessor', preprocessor),('classifier',  DecisionTreeClassifier(max_depth=6, random_state=1))])
    X = df
    y = y
    clf.fit(X, y)
    print(clf.score(X,y))
    
    # Saving model to pickle file  Dump function is used to write the object into the created file in byte format
    with open("model-name.pkl", "wb") as file:
        pickle.dump(clf, file)
        
    # The model has now been deserialized, next is to make use of it as you normally would.
    frame = {'Gender':'F', 'Education_Level':'Graduate', 'Marital_Status':'Single', 'Income_Category':'Less than $40K', 'Card_Category':'Blue', 'Credit_Limit':8256.0,'Avg_Utilization_Ratio':0.9}

    data_frame = pandas.DataFrame([frame])
    # Opening saved model
    with open("model-name.pkl", "rb") as file:
        model = pickle.load(file)

    prediction = model.predict(data_frame)
    print("The result is",prediction[0])

    return None


if __name__ == "__main__":
    create_ml_model()
