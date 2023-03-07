import sqlite3
from matplotlib.figure import Figure
import pandas
import os
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.compose import make_column_selector as selector
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import  OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.cluster import KMeans
import base64
from io import BytesIO

def read_database(database_path : str = "a_database_creation/database",
                    database_name : str = "database.db") -> None:
    database = os.path.join(database_path, database_name)
    conn = sqlite3.connect(database)
    df = pandas.read_sql('SELECT * FROM bank_churners', conn)
    conn.close()
    return df

def create_ml_model():
    df = read_database()
    df['avg_amt'] = df["Total_Trans_Amt"]/df['Total_Trans_Ct']
    numeric_transformer = Pipeline(
    steps=[("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler())]
    )
    categorical_transformer =  OneHotEncoder(handle_unknown='ignore')

    preprocessor = ColumnTransformer(transformers=[("num", numeric_transformer, selector(dtype_exclude=object)),('cat', categorical_transformer, selector(dtype_include=object))])

    clf = Pipeline(steps=[('preprocessor', preprocessor),('classifier',  KMeans(n_clusters=3, n_init=10, max_iter=200))])
    km_clusters = clf.fit_predict(df)
    df['km_clusters']=km_clusters
    return df
def get_cluster(data_frame : pandas.DataFrame = 
                    {'Total_Relationship_Count':[6],'Credit_Limit':[10388.0], 'Total_Revolving_Bal':[1961], 
                     'Avg_Open_To_Buy':[8427.0], 'Total_Trans_Amt':[10294], 'Total_Trans_Ct':[61]}):
    df = create_ml_model()
    data_frame = pandas.DataFrame(data=data_frame)

    df_data_frame = df[(df['Total_Relationship_Count'] == data_frame.iloc[0,0])&(df['Credit_Limit'] == data_frame.iloc[0,1]) & (df['Total_Revolving_Bal'] == data_frame.iloc[0,2])&
                        (df['Avg_Open_To_Buy'] == data_frame.iloc[0,3])& (df['Total_Trans_Amt'] == data_frame.iloc[0,4])&(df['Total_Trans_Ct'] == data_frame.iloc[0,5])]
    df3 = df[df['km_clusters']==int(df_data_frame.km_clusters.values[0])]
    return df3

def my_autopct(pct):
    return ('%1.0f%%' % pct) if pct > 8 else ''

def unpack(val:pandas._libs.interval.Interval):
    var_list = []
    for k in val.keys():
        res = round(k.left,1).astype(str) +" - "+ round(k.right,1).astype(str)
        var_list.append(res)
    return var_list

def show_pie_charts(cluster_number : int = 0):

    df = create_ml_model()
    df3 = df[df['km_clusters']==cluster_number]
    
    colors = sns.color_palette('pastel')[0:10]
    fig = Figure(figsize=(16,6))
    axs = fig.subplots(1, 3, sharey=True)

    avg_amt_values = df3['avg_amt'].value_counts(bins=6, normalize=True)
    labels = unpack(avg_amt_values)
    axs[0].pie(avg_amt_values, colors=colors, autopct=my_autopct, shadow=True, startangle=90)
    axs[0].legend(labels, bbox_to_anchor=(1, 1), fontsize = 'small')
    axs[0].set_xlabel('Average Transaction Amount', fontsize = 'xx-large')

    values_card = df3.value_counts('Card_Category', normalize=True)
    axs[1].pie(values_card, colors=colors, autopct=my_autopct, shadow=True, startangle=90)
    axs[1].legend(list(values_card.keys()), bbox_to_anchor=(1, 1), fontsize = 'small')
    axs[1].set_xlabel('Card Category', fontsize = 'xx-large')

    months_inactive_12_mon_values = df3['Months_Inactive_12_mon'].value_counts(normalize=True)
    axs[2].pie(months_inactive_12_mon_values,  colors=colors, autopct=my_autopct, shadow=True, startangle=90)
    axs[2].legend(list(months_inactive_12_mon_values.keys()), bbox_to_anchor=(1, 1), fontsize = 'small')
    axs[2].set_xlabel('12 Months Inactive', fontsize = 'xx-large')
    fig.suptitle('KPI - I - '+ 'Cluster ' + str(cluster_number))
    plt.tight_layout()

    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data

def show_bar_charts(cluster_number : int = 0):
    df = create_ml_model()
    df3 = df[df['km_clusters']==cluster_number]

    fig = Figure(figsize=(16,6))
    axs = fig.subplots(1, 3, sharey=True)

    income_category_values = df3.value_counts('Income_Category', normalize=True)
    axs[0].tick_params(axis='both', which='major', labelsize=9)
    axs[0].bar(list(income_category_values.keys()), income_category_values)
    axs[0].set_xlabel('Income Category', fontsize = 'x-large')

    dependent_count_values = df3['Dependent_count'].value_counts(bins=6, normalize=True)
    axs[1].bar(unpack(dependent_count_values), dependent_count_values)
    axs[1].set_xlabel('Dependents', fontsize = 'x-large')
    axs[1].tick_params(axis='both', which='major', labelsize=9)

    values_education = df3.value_counts('Education_Level', normalize=True)
    axs[2].tick_params(axis='both', which='major', labelsize=7)
    axs[2].bar(list(values_education.keys()), values_education)
    axs[2].set_xlabel('Education Category', fontsize = 'x-large')
    fig.suptitle('KPI - II - '+ 'Cluster ' + str(cluster_number))
    plt.tight_layout()
    
    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data


if __name__ == "__main__":
    read_database()
    create_ml_model()
    get_cluster()
    show_pie_charts()
    show_bar_charts()