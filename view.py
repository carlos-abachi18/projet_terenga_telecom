import pandas as pd
import streamlit as st 
import matplotlib.pyplot as plt 
import plotly.graph_objects as go
import plotly.express as px
import folium
from streamlit_folium import st_folium
from fonction import * 
from main import * 


st.set_page_config(
    page_title="Terenga_Telecom", 
    page_icon="📡", 
    layout="wide")

col1, col2 = st.columns([1,3])
with col1:
   st.image("./assets/logo2.png")
with col2:
   st.title("Dashboard Projet teranga_telecom")
   st.subheader("Analyse Global Des Désabonnement")


with st.sidebar:

  st.image("./assets/logo_T.png")

  st.header("Dashboard Filtre")

  st.header("choissez votre filtre ")

  status=st.multiselect(
     "selectionnez le statut des clients",
     options= customers_data['Customer_Status'].unique(),
     default= customers_data['Customer_Status'].unique(),
  )
  
  category=st.multiselect(
     "selectionnez la categorie de churn reason",
     options= customers_data['Churn_Category'].unique(),
     default= customers_data['Churn_Category'].unique(),
  )
  payment=st.multiselect(
     "selectionnez la categorie de churn reason",
     options= customers_data['Payment_Method'].unique(),
     default= customers_data['Payment_Method'].unique(),
  )
  gender=st.multiselect(
     "selectionnez la categorie de churn reason",
     options= customers_data['Gender'].unique(),
     default= customers_data['Gender'].unique(),
  )

  customers_data =  customers_data[
    (customers_data['Churn_Category'].isin(category)) &
    (customers_data['Payment_Method'].isin(payment)) &
    (customers_data['Gender'].isin(gender)) &
    (customers_data['Customer_Status'].isin(status))]

condition = customers_data['Customer_Status'] == 'Churned'
churn_data = customers_data[condition]  

def info():
  
   with st.expander('Customer Table'):
      cust_Show = st.multiselect( "Filtre:", options = customers_data.columns , default=['Customer_ID', 'Gender', 'Age','Customer_Status', 'Churn_Category', 'Churn_Reason'])
      st.write (customers_data[cust_Show])

   total1, total2, total3, total4,=st.columns(4)

   with total1:
      st.info("Ville" , icon ='📌')
      st.metric(label="Total de Ville", value= customers_data["City"].nunique())
   with total2:
      st.info("Chiffre d'Affaire" , icon ='📌')
      st.metric(label="Chiffre d'Affaire en $", value= int(customers_data["Total_Revenue"].sum()))
   with total3:
      st.info("Total Client " , icon ='📌')
      st.metric(label="Nombre de Client", value= customers_data["Customer_ID"].count()) 
   with total4:
      st.info("Total Désabonné" , icon ='📌')
      st.metric(label="Nombre de Désabonné", value= customers_data['Customer_Status'].value_counts().get("Churned",0))
   st.markdown("""-------- """)
info()

def city_graph():

   city_churn = churn_data.groupby("City")["City"].count()
   city_churn = pd.DataFrame({"City": city_churn.index, 'Nombre_de_Désabonné': city_churn.values})
 
   city = customers_data.groupby("City")['Customer_ID'].count().sort_values(ascending=False)
   city = pd.DataFrame({"City": city.index, 'Nombre_de_Client': city.values})

   City_data = pd.merge(city, city_churn, on="City", how='left')
   City_data['Nombre_de_Désabonné'] = City_data['Nombre_de_Désabonné'].fillna(0).astype(int)
   City_data = City_data.sort_values(by="Nombre_de_Client",ascending= False).head(10)

   fig = go.Figure()
   fig.add_trace(go.Bar(
    x=City_data["City"] ,
    y=City_data['Nombre_de_Client'],
   #  text_auto='.1s',
    name="nombre d'abonné",
))
   fig.add_trace(go.Bar(
    x=City_data["City"],
    y=City_data['Nombre_de_Désabonné'],
   #  text_auto='.1s',
    name="nombre de desabonné",
    
))
   fig.update_layout(
     plot_bgcolor="rgba(0,0,0,0)",
     font=dict(color="black"),
     yaxis=dict(showgrid=True, gridcolor='#cecdcd'),  # Show y-axis grid and set its color  
     paper_bgcolor='rgba(0, 0, 0, 0)', )
   
   st.info("Client Par ville " , icon ='📌')
   with st.expander("""Top 10 des villes en Terme de client """): 
      st.plotly_chart(fig,use_container_width=True)  
city_graph()

def graph():
   # graphique
   category_churn = churn_data.groupby("Churn_Category")["Churn_Category"].count().sort_values(ascending=False)
   category_churn= pd.DataFrame({"CHURN CATEGORY ": category_churn.index, 'value': category_churn.values})

   fig_category= px.bar(category_churn,
       x= category_churn["CHURN CATEGORY "],
       y=category_churn['value'], 
       text_auto='.',
       title="<b> RAISON DE DESABONNEMENT  </b>",
       color_discrete_sequence=["#0083B8"]*len(category_churn),
       template="plotly_white",
   )
   fig_category.update_layout(
     plot_bgcolor="rgba(0,0,0,0)",
     font=dict(color="black"),
     yaxis=dict(showgrid=True, gridcolor='#cecdcd'),  # Show y-axis grid and set its color  
     paper_bgcolor='rgba(0, 0, 0, 0)',
   )
   customers_repartiton  = customers_data['Customer_Status'].value_counts()
   customers_repartiton  = pd.DataFrame(customers_repartiton)
   fig_raison= px.pie(customers_repartiton,
               values= customers_repartiton['count'],
               names=customers_repartiton.index, 
               title="<b> REPARTION DES CLIENTS PAR STATUS  </b>",
               # color_discrete_sequence=["#0083B8"]*len(),
               template="plotly_white",
   )
   fig_raison.update_layout(
     plot_bgcolor="rgba(0,0,0,0)",
     font=dict(color="black"),
     yaxis=dict(showgrid=True, gridcolor='#cecdcd'),)
   
   # Tableaux
   Month = churn_data["Tenure_in_Months"].value_counts().sort_index()
   relativ_frequence =( Month / Month.sum())*100
   cumul_frequence = relativ_frequence.cumsum()
   Month_data = pd.DataFrame({"frequence":Month,"relativ_frequence":relativ_frequence,"cumul_frequence":cumul_frequence})
   churn_month = Month_data[["frequence","relativ_frequence"]].sort_values(by="relativ_frequence",ascending=False).head(15)
   cumul_month = pd.DataFrame(Month_data['cumul_frequence'].loc[[12,24,36,48,60,72]])
   nombre_d_année = [1,2,3,4,5,6]
   cumul_month.index = nombre_d_année
   
   fig = go.Figure(data=[go.Table(
    header=dict(values= [ 'Nombre_de_Mois','Nombre_de_Client', 'Pourcentage'],
                fill_color='steel blue',
                align='left'),
    cells=dict(values=[churn_month.index, churn_month.frequence, churn_month.relativ_frequence],
               fill_color='black',
               align='left',))
])
   fig_A = go.Figure(data=[go.Table(
    header=dict(values= [ "Nombre_d'Année",'Pourcentage'],
                fill_color='steel blue',
                align='left'),
    cells=dict(values=[cumul_month.index, cumul_month.cumul_frequence,],
               fill_color='black',
               align='left',))
])     
# repartion des churned par ofrre
   services = ['Phone_Service','Multiple_Lines', 'Internet_Service',
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

   fig_of = go.Figure(data=[go.Table(
   header=dict(values= [ "Offres",'Pourcentage_of_churn'],
                fill_color='steel blue',
                align='left'),
    cells=dict(values=[offer_data.index, offer_data.percent_of_churn_customers,],
               fill_color='black',
               align='left',))
   ])
# positionnement 
   total1, total2, total3=st.columns(3)
   with total1:
      st.plotly_chart(fig_raison,use_container_width=True)
   with total2:
      st.plotly_chart(fig_category,use_container_width=True)
   with total3:
      st.title('                 ')
      st.markdown('                 ')
      st.markdown('                 ')
      st.markdown('                 ')
      with st.expander(""" Nombre de Mois d'Abonnement"""):
         st.markdown("*Ce tableau presente le nombre de  clients desabonnés en fonction de la durée  en mois de leur abonnement*")
         st.plotly_chart(fig,use_container_width=True)
         st.markdown('                 ')
         st.markdown('                 ')
      with st.expander(""" Nombre d'Année d'Abonnement"""):
         st.markdown("*Ce tableau presente le nombre de  clients desabonnés en fonction de la durée  en Année de leur abonnement*")
         st.plotly_chart(fig_A,use_container_width=True)
         st.markdown('                 ')
         st.markdown('                 ')
      with st.expander(""" les Offres """):
         st.markdown("*Ce tableau presente les ofrres de TERENGA_TELECOM et le pourcentage des desabonnée qui y avait souscrit*")
         st.plotly_chart(fig_of,use_container_width=True)
graph()

def Map_grap():
   # Définir le centre de la carte
   moyenne_lat = big_city_data["latitude"].mean()
   moyenne_lon = big_city_data['Longitude'].mean()

   # Créer une carte Folium centrée sur les coordonnées moyennes
   m = folium.Map(location=[moyenne_lat, moyenne_lon], zoom_start=5)

   # Ajouter des marqueurs pour chaque ville
   for _, row in big_city_data.iterrows():
      folium.Marker(
         location=[row["latitude"], row['Longitude']],
         tooltip=row[['City','Nombre_de_Client','Nombre_de_Désabonné']].values
      ).add_to(m)

   # Afficher la carte dans Streamlit
   st.title("Carte de visualisation des villes ")
   st_folium(m, width=700, height=500)
col1,col2 = st.columns([2,2])
with col1:
   Map_grap()

with col2:
   st.title("Taux de Couverture des Villes")
   # Sélecteur pour choisir une ville
   selected_city = st.selectbox(
      "Choisissez une ville",
      options=City_data['City'].tolist(),
   )

   # Filtrer les données pour la ville sélectionnée
   city_data = City_data[City_data['City'] == selected_city].iloc[0]

   # Créer les données pour le diagramme circulaire
   coverage_data = pd.DataFrame({
      "Metric": ["taux_de_couverture", "Marché_potentiel"],
      "Value": [city_data['taux_de_couverture'], 100 - city_data['taux_de_couverture']]
   })

   # Créer le diagramme circulaire
   fig_t = px.pie(
      coverage_data,
      values='Value',
      names='Metric',
      title=f'Taux de Couverture pour {selected_city}',
      labels={'Value': 'Pourcentage'},
      hole=0.3)
   
   st.plotly_chart(fig_t)
      
      