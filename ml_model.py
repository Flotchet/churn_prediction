import sqlite3
import pandas
import os
import warnings
import sqlite3
import pandas
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import PolynomialFeatures
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import LabelBinarizer
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

def create_ml_model(database_path : str = "/Users/emiliagenadieva/Desktop/PythonLessons/MLLessons/include/Work/Clusters",
                    database_name : str = "database.db") -> None:

    database = os.path.join(database_path, database_name)

    conn = sqlite3.connect(database)

    # code added for ml model
    df = pandas.read_sql('SELECT * FROM bank_churners', conn)
    numeric_features = df.select_dtypes(include=['float64'])
    categorical_features = df.select_dtypes(include=['object'])
    lb = LabelBinarizer()
    for var in categorical_features:
        df[var] = lb.fit_transform(df[var])
    df = df.drop(['CLIENTNUM'], axis = 1)
    for var in numeric_features:
        df.merge(df[var])
    X = df.drop(['Attrition_Flag'], axis = 1)
    y = df['Attrition_Flag'].values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.33, shuffle = False, random_state = 0)
    SEED = 1
    numeric_transformer = Pipeline(steps=[('poly',PolynomialFeatures(degree =2)), ('scaler', StandardScaler())])
    preprocessor = ColumnTransformer(transformers=[('num', numeric_transformer, X.columns.values)])
    clf = Pipeline(steps=[('preprocessor', preprocessor),('classifier', DecisionTreeClassifier(max_depth=6, random_state=SEED))])

    clf.fit(X_train,y_train)
    print(clf.score(X_train,y_train))
    print(clf.score(X_test, y_test))
    accuracy_score(y_test, clf.predict(X_test))


    conn.close()

    return None


if __name__ == "__main__":
    create_ml_model()