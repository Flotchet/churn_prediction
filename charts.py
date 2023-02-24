import sqlite3
import pandas
import os
import seaborn as sns
import matplotlib.pyplot as plt
def create_ml_model(database_path : str = "a_database_creation/database",
                    database_name : str = "database.db") -> None:

    database = os.path.join(database_path, database_name)

    conn = sqlite3.connect(database)

    # code added for ml model
    df = pandas.read_sql('SELECT Attrition_Flag, Gender,Dependent_count,Education_Level,Marital_Status, Income_Category, Card_Category, Total_Relationship_Count, Months_Inactive_12_mon, Credit_Limit, Total_Revolving_Bal, Avg_Open_To_Buy, Total_Trans_Amt, Total_Trans_Ct FROM bank_churners', conn)
    conn.close()
    df['avg_amt'] = df["Total_Trans_Amt"]/df['Total_Trans_Ct']
    
    colors = sns.color_palette('pastel')[0:10]
    def my_autopct(pct):
        return ('%1.0f%%' % pct) if pct > 20 else ''
    colors = sns.color_palette('pastel')[0:10]

    fig, axs = plt.subplots(1, 3, figsize=(22,6), sharey=True)
    labels = ['$47 - $76', '$19 - $48', '$76 - $105', '$105 - $133', '$133 - $161', '$161 - $190']
    axs[0].pie( df['avg_amt'].value_counts(bins=6) ,autopct=my_autopct, colors=colors, shadow=True, startangle=90)
    axs[0].legend(labels, bbox_to_anchor=(1, 1), fontsize = 'small')
    axs[0].set_xlabel('Avg Transaction Amount', fontsize = 'xx-large')

    names_card = ['Blue', 'Gold', 'Silver', 'Platinum']
    values_card = list(df.value_counts('Card_Category', normalize=True))
    axs[1].pie(values_card ,autopct=my_autopct, colors=colors, shadow=True, startangle=90)
    axs[1].legend(names_card, bbox_to_anchor=(1, 1), fontsize = 'small')
    axs[1].set_xlabel('Card Category', fontsize = 'xx-large')

    values_card = list(df['Months_Inactive_12_mon'].value_counts(normalize=True))
    axs[2].pie(values_card ,autopct=my_autopct, colors=colors, shadow=True, startangle=90)
    axs[2].legend(df['Months_Inactive_12_mon'].unique(), bbox_to_anchor=(1, 1), fontsize = 'small')
    axs[2].set_xlabel('12 Months Inactive', fontsize = 'xx-large')
    fig.suptitle('KPI - I')
    plt.tight_layout()
    plt.show()

    fig, axs = plt.subplots(1, 3, figsize=(22,6), sharey=True)
    names = ['Less than $40K', '$40K - $60K', '$80K - $120K', '$60K - $80K', 'Unknown', '$120K +']
    values = list(df.value_counts('Income_Category', normalize=True))
    axs[0].tick_params(axis='both', which='major', labelsize=9)
    axs[0].bar(names, values)
    axs[0].set_xlabel('Income Category', fontsize = 'x-large')

    labels_credit_limit =['2.5 - 3.3', '1.6 - 2.5', '0.8 - 1.6', '3.3 - 4.1', '0 - 0.8', '4.1 - 5']
    axs[1].bar(labels_credit_limit, df['Dependent_count'].value_counts(bins=6, normalize=True))
    axs[1].set_xlabel('Dependents', fontsize = 'x-large')
    axs[1].tick_params(axis='both', which='major', labelsize=9)

    names_education = ['Graduate', 'High School', 'Unknown', 'Uneducated', 'College', 'Post-Graduate', 'Doctorate']
    values_education = df.value_counts('Education_Level', normalize=True)
    axs[2].tick_params(axis='both', which='major', labelsize=7)
    axs[2].bar(names_education, values_education)
    axs[2].set_xlabel('Education Category', fontsize = 'x-large')

    fig.suptitle('KPI - II')
    plt.tight_layout()
    plt.show()

    return None


if __name__ == "__main__":
    create_ml_model()