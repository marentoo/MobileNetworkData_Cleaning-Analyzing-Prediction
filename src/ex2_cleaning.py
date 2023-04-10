import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler, StandardScaler

from ex2_loading import load_df

df1 = pd.read_csv('o2_download_nexus5x.csv'); df2 = pd.read_csv('telekom_download_nexus5x.csv'); df3 = pd.read_csv('vodafone_download_nexus5x.csv')
df4 = pd.read_csv('o2_upload_nexus5x.csv'); df5 = pd.read_csv('telekom_upload_nexus5x.csv'); df6 = pd.read_csv('vodafone_upload_nexus5x.csv')
df_downloads,df_uploads = load_df(df1,df2,df3,df4,df5,df6)

# print(df_downloads.head(3)); # print(df_uploads.head(3))

##Cleaning data
#------------------------------------------------------------------------------------
        ##check duplicates and ##Checking percentage of duplicates and ##Removing all duplicates

def clean_dupl(df, df_name):
    duplicateRows = df[df.duplicated()]
    print(f'No. duplicated rows - {df_name}: {len(duplicateRows.index)}')
    percentage = int(len(duplicateRows.index) * 100) / len(df.index)
    print(f'Duplicate percentage - {df_name}: {percentage:.2f}%')    
    df.drop_duplicates(keep='last', inplace = True)
    print("\n","Droping duplicates!","\n")
    return df

#------------------------------------------------------------------------------------
        ##Checking for missing data and Handle missing data - no missing data! but if ... then:

def clean_miss(df,df_name):
    sNaN = df.isnull().values.any()
    print(f"Any missing data - {df_name}?: {sNaN}\n")
    if sNaN:
        df.fillna(df.median(), inplace=True)
        print("\n","Droping missing data!","\n")
    return df

#------------------------------------------------------------------------------------
        ##Detect outliers -  Define z_score for checking outliers and Percentage of outliers in whole dataset:

def detect_outliers(df, df_name):
    z_scores = np.abs((df - df.mean(numeric_only=True)) / df.std(numeric_only=True))
    outliers = df[(z_scores > 4).any(axis=1)]
    print(f'No. of outliers - {df_name}: {len(outliers.index)}')
    percout = int((len(outliers.index)*100)/len(df.index))
    print(f' outliers percentage- {df_name}: {percout} %\n')
    return df

        ##Vizualize outliers - boxplot
def vis_outl_bxplt(df, columns, dfbx_name):
    df_num = df.loc[:,columns]
    _, ax = plt.subplots(figsize=(20,6))
    df_num.plot(kind = 'box', ax=ax)
    plt.savefig(f'evaluation/boxplot_{dfbx_name}.png')

        ##Handling outliers <-- Drop outliers from the dataframes #<<-dziala ale zle <<--- pytanie gdzie umieścic
## df_downloads = df_downloads.drop(outliersD.index,)
## df_uploads = df_uploads.drop(outliersU.index)
## print("\n","Droping outliers!","\n")
## print(f'Rd:{len(df_downloads.index)}');print(f'Ru:{len(df_uploads.index)}')

#------------------------------------------------------------------------------------
        ##Standardize data - Check for inconsistent data formats and standardize them to make analysis easier.
##https://www.analyticsvidhya.com/blog/2020/04/feature-scaling-machine-learning-normalization-standardization/#Why_Should_We_Use_Feature_Scaling?

##for normalization we may leave outliers, for standarization let's remove outliers before.
scaler_norm = MinMaxScaler() #scale between <0,1> (for e.g. algor: KNN or NN)
scaler_stand = StandardScaler() #scale differently ( for e.g. Logistic Regression, Linear Discriminant Analysis)

def scaling_data(df, scaler):
        ##Scaling data -select numeric data to scale -  Scale the numeric columns for better performance of machine learning algorihms
        ##???nie wiem czy nie powinniśmy wybierac dokładnych kolumn ktore on normalizuje/standaryzuje
        num_cols = df.select_dtypes(include=['int64' , 'float64']).columns
        ##Fit and transform the data using the scaler
        df[num_cols]=scaler.fit_transform(df[num_cols])
        print(df.head(1)) #let's check it
        return df

#------------------------------------------------------------------------------------
def clean_df(XDdf_downloads, XDdf_uploads, XDscaler_norm):
        clean_dupl(XDdf_downloads, 'downloads')
        clean_dupl(XDdf_uploads, 'uploads')
        clean_miss(XDdf_downloads,'downloads')
        clean_miss(XDdf_uploads,'uploads')
        detect_outliers(XDdf_downloads,'downloads')
        detect_outliers(XDdf_uploads,'uploads')
        vis_outl_bxplt(XDdf_downloads, ['throughput','tp_cleaned'],'downloads_th_tp')
        vis_outl_bxplt(XDdf_downloads, ['rsrq', 'rsrp', 'rssi'],'downloads__rsrq_rsrp_rssi')
        vis_outl_bxplt(XDdf_uploads, ['rsrq', 'rsrp', 'rssi'],'uploads_rsrq_rsrp_rssi')
        vis_outl_bxplt(XDdf_uploads, ['tp_cleaned'],'uploads_tp')
        XDdf_scale_d = scaling_data(XDdf_downloads, XDscaler_norm)
        XDdf_scale_u = scaling_data(XDdf_uploads, XDscaler_norm)
        return XDdf_scale_d, XDdf_scale_u

## let's test it
# df_scale_d, df_scale_u = clean_df(df_downloads, df_uploads, scaler_norm)
