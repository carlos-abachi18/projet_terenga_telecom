import pandas as pd
from fonction import * 

# Données
customers_data = data_clean()
print(customers_data.info())

# les donnée des clients churners uniquements  
condition = customers_data['Customer_Status'] == 'Churned'
churn_data = customers_data[condition]

# chiffre d'affaire
chiffre_A = customers_data["Total_Revenue"].sum()
print(chiffre_A)

# nombre total d'Abonné 
Nbre_cust = customers_data['Customer_ID'].count()

# Nombre de desabonné
churn_number = customers_data['Customer_Status'].value_counts().get("Churned",0)

# Top 10 DES VILLES AVEC LE PLUS DE CHURNER
city_churn = churn_data.groupby("City")["City"].count()
city_churn = pd.DataFrame({"City": city_churn.index, 'Nombre_de_Désabonné': city_churn.values})

# repartion des clients par ville 
city = customers_data.groupby("City")['Customer_ID'].count().sort_values(ascending=False)
city = pd.DataFrame({"City": city.index, 'Nombre_de_Client': city.values})

# donné par ville 
City_data = pd.merge(city, city_churn, on="City", how='left')
City_data['Nombre_de_Désabonné'] = City_data['Nombre_de_Désabonné'].fillna(0).astype(int)
city_data = City_data.sort_values(by = 'Nombre_de_Client',ascending=False).head(30)
print(city_data)

# Repartition des client churn par category de churn
category_churn = churn_data.groupby("Churn_Category")["Churn_Category"].count().sort_values(ascending=False)
category_churn= pd.DataFrame({"CHURN CATEGORY ": category_churn.index, 'value': category_churn.values})
print(category_churn)

# Répartition des clients par status 
customers_repartiton  = customers_data['Customer_Status'].value_counts()
customers_repartiton  = pd.DataFrame(customers_repartiton)
customers_repartiton["percent"] = (customers_repartiton["count"]/customers_repartiton ["count"].sum())*100
print(customers_repartiton)

# nombre de mois passé par le client avant le churn
# donnéés
Month = churn_data["Tenure_in_Months"].value_counts().sort_index()
relativ_frequence =( Month / Month.sum())*100
cumul_frequence = relativ_frequence.cumsum()
Month_data = pd.DataFrame({"frequence":Month,"relativ_frequence":relativ_frequence,"cumul_frequence":cumul_frequence})

# les nombres de mois avec le plus d'effectif 
churn_month = Month_data[["frequence","relativ_frequence"]].sort_values(by="relativ_frequence",ascending=False).head(10)
print(churn_month)

# repartition par ans 
cumul_month = Month_data['cumul_frequence'].loc[[12,24,36,48,60,72]]
print(cumul_month)

# repartion des churned par ofrre
services = ['Phone_Service','Multiple_Lines', 'Internet_Service', 'Internet_Type',
       'Online_Security', 'Online_Backup',
       'Device_Protection_Plan', 'Premium_Tech_Support','Streaming_TV',
       'Streaming_Movies', 'Streaming_Music', 'Unlimited_Data',
       'Paperless_Billing']
number = []
for serv in services:
  service = {}
  service["service"] = serv
  count = churn_data[serv].value_counts()
  # service["total_number"] = count.sum()
  service["percent_of_churn_customers"] = (count.get("Yes",0)/count.sum())*100
  number.append(service)
offer_data = pd.DataFrame(number)
offer_data.set_index('service' , inplace= True)
print(offer_data)

# # Exemple d'utilisation
# ville = "Paris"
# latitude, longitude = obtenir_coordonnees(ville)
# print(f"Latitude: {latitude}, Longitude: {longitude}")

df = {"City":["Los Angeles" ,"San Diego","San Jose" ,"Sacramento","San Francisco","Fresno","Long Beach","Oakland","Escondido","Stockton",'Fallbrook', 'Glendale', 'Bakersfield', 'Temecula', 'Berkeley',
          'Riverside', 'Whittier', 'Pasadena', 'Anaheim', 'Irvine','Modesto', 'San Bernardino', 'Santa Barbara', 'Inglewood','Santa Monica', 'Burbank', 'Torrance', 'Santa Ana', 'Santa Rosa',
          'Chula Vista', 'Orange'],
        "latitude" : [34.053691,32.717420,37.336166,38.581061,37.779259,36.739442,33.769016,37.804456,33.121675,37.957702,33.3744,34.1425,35.3733,33.4936, 37.8716,33.9806, 33.9791,34.1478,33.8366,33.6846,37.6391, 34.1083, 34.4208, 33.9164, 34.0194, 34.1808, 33.8358, 33.7455, 38.4405, 32.6401, 33.7879 ],
       "Longitude" : [-118.242766,-117.162772,-121.890591,-121.493895,-122.419329,-119.784830,-118.191604,-122.271356,-117.081485,-121.290779,   -117.2333,-118.2551,-119.0187,-117.1484,-122.2727,-117.3755,-118.0328,-118.1445,-117.9143,-117.8265,-120.9969, -117.2898, -119.6982, -118.3526, -118.4912, -118.3089, -118.3406, -117.8677, -122.7141, -117.0842, -117.8531]
}

df= pd.DataFrame(df)
print(df)

big_city_data = pd.merge(city_data,df,on='City',how='left')
print(big_city_data.info())