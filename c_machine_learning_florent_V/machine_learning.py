import pandas as pd
import sqlite3
import os


from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import xgboost as xgb

def load_data(db : str = "/home/flotchet/Becode/Projects/Churn prediction/churn_prediction/a_database_creation/database/database.db") -> pd.DataFrame:
    """
    Load the data from the database

    Parameters
    ----------
    db : str, optional
        The path to the database, by default "/home/flotchet/Becode/Projects/Churn prediction/churn_prediction/a_database_creation/database/database.db"

    Returns
    -------
    pandas.DataFrame
        The dataframe of the database

    Raises
    ------
    FileNotFoundError
        If the database is not found
    """
    if not os.path.exists(db):
        raise FileNotFoundError("The database is not found")

    conn = sqlite3.connect(db)
    df = pd.read_sql("SELECT * FROM bank_churners", conn)
    conn.close()
    
    return df

def data_cleaner_for_ml(df : pd.DataFrame) -> pd.DataFrame:
    """
    Clean the data for the machine learning part by transforming all
    string collumn into dummies

    Parameters
    ----------
    df : pandas.DataFrame
        The dataframe to clean

    Returns
    -------
    pandas.DataFrame
        The cleaned dataframe
    """


    for col in df.columns:
        if df[col].dtype == "object":
            #replace the column by its dummy equivalent
            df = pd.concat([df, pd.get_dummies(df[col], prefix=col)], axis=1)
            #drop the original column
            df.drop(columns=[col], inplace=True)
    return df



def data_splitter(df : pd.DataFrame, target : str = "Attrition_Flag_Attrited Customer") -> tuple:
    """
    Split the data into X and y

    Parameters
    ----------
    df : pandas.DataFrame
        The dataframe to split

    target : str, optional
        The target column, by default "Attrition_Flag_Churned Customer"

    Returns
    -------
    tuple
        The X and y dataframes
    """
    X = df.drop(columns=[target])
    y = df[target]
    return X, y

def data_scaler(X : pd.DataFrame) -> pd.DataFrame:
    """
    Scale the data

    Parameters
    ----------
    X : pandas.DataFrame
        The dataframe to scale

    Returns
    -------
    pandas.DataFrame
        The scaled dataframe
    """
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    X = scaler.fit_transform(X)
    return X

if __name__ == "__main__":
    df = load_data()

    #drop the Dependent_count column
    df.drop(columns=["Naive_Bayes_Classifier_Attrition_Flag_Card_Category_Contacts_Count_12_mon_Dependent_count_Education_Level_Months_Inactive_12_mon_1","Naive_Bayes_Classifier_Attrition_Flag_Card_Category_Contacts_Count_12_mon_Dependent_count_Education_Level_Months_Inactive_12_mon_2", "CLIENTNUM"], inplace=True)
    df = data_cleaner_for_ml(df)
    print(df.info)
    print(df.head())
    #print abg value for each column where Attrition_Flag_Attrited Customer == True
    for col in df.columns:
        if col != "Attrition_Flag_Attrited Customer":
            print(col, df[df["Attrition_Flag_Attrited Customer"] == 1][col].mean())
    
    #correlation matrix
    import seaborn as sns
    import matplotlib.pyplot as plt
    corr = df.corr()
    plt.figure(figsize=(20,20))
    sns.heatmap(corr, annot=True, cmap="coolwarm")
   
    plt.show()
   
    #drop the Attrition_Flag_Existing Customer column
    df.drop(columns=["Attrition_Flag_Existing Customer"], inplace=True)
    print(df.columns)
    X, y = data_splitter(df)
    X = data_scaler(X)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = xgb.XGBClassifier()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print(accuracy_score(y_test, y_pred))
    print(confusion_matrix(y_test, y_pred))
    print(classification_report(y_test, y_pred))

    