import sqlite3
import pandas
import os
from sklearn.compose import make_column_selector as selector
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import  OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.cluster import KMeans


def create_ml_model(database_path : str = "a_database_creation/database",
                    database_name : str = "database.db",
                    data_frame:pandas.DataFrame = 
                    {'Total_Relationship_Count':[6],'Credit_Limit':[10388.0], 'Total_Revolving_Bal':[1961], 
                     'Avg_Open_To_Buy':[8427.0], 'Total_Trans_Amt':[10294], 'Total_Trans_Ct':[61]}) -> None:

    database = os.path.join(database_path, database_name)

    conn = sqlite3.connect(database)

    # code added for k-means clustering model
    df = pandas.read_sql('SELECT * FROM bank_churners', conn)
    conn.close()
    df['avg_amt'] = df["Total_Trans_Amt"]/df['Total_Trans_Ct']
    numeric_transformer = Pipeline(
    steps=[("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler())]
    )
    categorical_transformer =  OneHotEncoder(handle_unknown='ignore')

    preprocessor = ColumnTransformer(transformers=[("num", numeric_transformer, selector(dtype_exclude=object)),('cat', categorical_transformer, selector(dtype_include=object))])

    clf = Pipeline(steps=[('preprocessor', preprocessor),('classifier',  KMeans(n_clusters=3, n_init=10, max_iter=200))])
    km_clusters = clf.fit_predict(df)
    df['km_clusters']=km_clusters

    data_frame = pandas.DataFrame(data=data_frame)

    df_data_frame = df[(df['Total_Relationship_Count'] == data_frame.iloc[0,0])&(df['Credit_Limit'] == data_frame.iloc[0,1]) & (df['Total_Revolving_Bal'] == data_frame.iloc[0,2])&
                        (df['Avg_Open_To_Buy'] == data_frame.iloc[0,3])& (df['Total_Trans_Amt'] == data_frame.iloc[0,4])&(df['Total_Trans_Ct'] == data_frame.iloc[0,5])]


    df3 = df[df['km_clusters']==int(df_data_frame.km_clusters.values[0])]
    
    print("Client is from group ", df_data_frame.km_clusters.values[0])

    print("His/Her client group has", len(df3), 'members' )

    return None


if __name__ == "__main__":
    create_ml_model()