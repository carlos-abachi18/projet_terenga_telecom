import pandas as pd
import mysql.connector as connector 
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

colum_list= ['Customer ID', 'Gender', 'Age', 'Married', 'Number of Dependents',
       'City', 'Zip Code', 'Latitude', 'Longitude', 'Number of Referrals',
       'Tenure in Months', 'Offer', 'Phone Service',
       'Avg Monthly Long Distance Charges', 'Multiple Lines',
       'Internet Service', 'Internet Type', 'Avg Monthly GB Download',
       'Online Security', 'Online Backup', 'Device Protection Plan',
       'Premium Tech Support', 'Streaming TV', 'Streaming Movies',
       'Streaming Music', 'Unlimited Data', 'Contract', 'Paperless Billing',
       'Payment Method', 'Monthly Charge', 'Total Charges', 'Total Refunds',
       'Total Extra Data Charges', 'Total Long Distance Charges',
       'Total Revenue', 'Customer Status', 'Churn Category', 'Churn Reason']        

def connexion_database ():
    try: 
        connexion = connector.connect (host = "localhost",
                        user = 'root',
                        password = "", 
                        port = 3306 ,
                        database = 'customers_churn_pro')
        
        if connexion.is_connected():
            print("connexion reussi ✅" )
            return connexion
        else:
             print("connexion echouée")
             return None

    except connector.Error as erreur:  
        print(f"❌❌ erreur {erreur.msg}")
        return None
    
def get_data ():
    connexion = connexion_database()   
    if connexion is not None:

    # recuperation des données 
        curseur = connexion.cursor()
        curseur.execute ( "SELECT * FROM telecom_customer_churn" )
        customers_data = curseur.fetchall()
        customers_data = pd.DataFrame(customers_data)
        return customers_data 
    
    else:
        print(" il y a eu une erreur ") 

def data_cleanned ():
        
        customers_data = get_data() 

     # changer les colonnes  
        number = range(0,38)
        place = {}
        for c,n in zip(colum_list,number):    
            place[n]=c

        customers_data.rename(columns= place ,inplace = True )
    

     # changer le type des colonnes
        customers_data= customers_data.astype({
        'Latitude':'float',
        'Longitude':'float',
        'Avg Monthly Long Distance Charges':'float',
        'Avg Monthly GB Download':'float',
        'Monthly Charge':'float',
        'Total Charges':'float',
        'Total Refunds':'float',
        'Total Long Distance Charges':'float',
        'Total Revenue':'float'})

         # traitement des valeurs null
        liste = ["Multiple Lines","Internet Service","Internet Type","Online Security","Online Backup","Device Protection Plan","Premium Tech Support","Streaming TV","Streaming Movies","Streaming Music","Unlimited Data","Contract","Paperless Billing"]
        for colum in liste:
          customers_data[colum].fillna("No",inplace=True)
        
        customers_data.loc[customers_data['Customer Status'] == 'Stayed', 'Churn Reason'] = 'Aucune'
        customers_data.loc[customers_data['Customer Status'] == 'Stayed', 'Churn Category'] = 'Aucune'
        customers_data.loc[customers_data['Customer Status'] == 'Joined', 'Churn Reason'] = 'Aucune'
        customers_data.loc[customers_data['Customer Status'] == 'Joined', 'Churn Category'] = 'Aucune'
        
     #  renommer les colonnes 
        colum_rename = {}
        for colum in colum_list: 
          new_column = colum.replace(' ','_')   
          colum_rename[colum]=new_column

        customers_data.rename(columns=colum_rename,inplace= True)

        # supprimer la ligne de trop
        cond = customers_data["Customer_Status"]=='Customer Status'
        drop_line = customers_data.loc[cond].index
        customers_data = customers_data.drop(index = drop_line)
        return customers_data

def data_clean():
     
     customers_data = data_cleanned()
     columns_use = ['Customer_ID','Gender', 'Age', 'Married', 'Number_of_Dependents', 'City',
       'Latitude', 'Longitude', 'Number_of_Referrals', 'Tenure_in_Months',
       'Offer', 'Phone_Service','Multiple_Lines', 'Internet_Service', 'Internet_Type',
       'Online_Security', 'Online_Backup',
       'Device_Protection_Plan', 'Premium_Tech_Support','Streaming_TV',
       'Streaming_Movies', 'Streaming_Music', 'Unlimited_Data', 'Contract',
       'Paperless_Billing', 'Payment_Method', 'Monthly_Charge',
       'Total_Charges','Total_Revenue', 'Customer_Status','Churn_Category', 'Churn_Reason']

     customers_data_clean = customers_data[columns_use]
     return customers_data_clean






