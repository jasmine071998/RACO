#PACKAGES
import kneed
import pandas as pd
import io
import numpy as np
from geopy.geocoders import Nominatim
import math
from sklearn.cluster import KMeans
from kneed import KneeLocator
import mlrose
import folium
import tkinter as tk               
from tkinter import font  as tkfont 
from tkinter import ttk

def loca(x):  
  geolocator = Nominatim()
  location = geolocator.geocode(x,timeout=1000000)
  temp=[]
  temp.append(location.latitude)
  temp.append(location.longitude)
  return(temp)
  
def distance(p1,p2):
  return math.sqrt(((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2))

def haversine(coord1, coord2):
      R = 6372800  # Earth radius in meters
      lat1,lon1 = coord1
      lat2,lon2 = coord2 
      phi1,phi2 = math.radians(lat1),math.radians(lat2) 
      dphi = math.radians(lat2-lat1)
      dlambda = math.radians(lon2-lon1)
      a = math.sin(dphi/2)**2 + \
          math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
      return 2*R*math.atan2(math.sqrt(a),math.sqrt(1 - a))

def get_unique_location(dfsales):
  unique_location=dfsales["Customer Location"].unique().tolist()
  unique_locations=[]
  for i in unique_location:
    if(i!="NASHIK"):
      unique_locations.append(i)
  return(unique_locations)
  
def get_all_locations_coord(unique_locations):
  all_locations_coord=[]
  for i in unique_locations:
    all_locations_coord.append(loca(i))
  return(all_locations_coord)
  
def Warehouse_Distribution(all_locations_coord,unique_locations):
  location_in_nashik=[]
  location_in_pune=[]
  both=[]
  bothd=[]
  nashik_in_coord=[]
  pune_in_coord=[]
  distance_pune=[]
  distance_nashik=[] 

  pune=loca("Pune")
  nashik=loca("Nashik")
  them=["Nashik","Pune"]
  themd=[nashik,pune]
  for coord in all_locations_coord:
      distance=(haversine(pune, coord))
      distance1=(haversine(nashik, coord))
      distance_pune.append(distance)
      distance_nashik.append(distance1)  
  for i in range(len(all_locations_coord)):
    if(distance_pune[i]>distance_nashik[i]):
      location_in_nashik.append(unique_locations[i])
      nashik_in_coord.append(all_locations_coord[i])
    else:
      location_in_pune.append(unique_locations[i])
      pune_in_coord.append(all_locations_coord[i])

  both.append(location_in_nashik)
  both.append(location_in_pune)
  bothd.append(nashik_in_coord)
  bothd.append(pune_in_coord)
  return(both,location_in_nashik,location_in_pune,nashik_in_coord,pune_in_coord,them)
  
def tsp(dd,l):
    state=[]
    for i in range(0,len(dd)):
      fitness_dists = mlrose.TravellingSales(distances = dd[i])
      problem_fit = mlrose.TSPOpt(length = len(l[i]), fitness_fn = fitness_dists, maximize=False)
      best_state, best_fitness = mlrose.genetic_alg(problem_fit, random_state = 2)
      state.append(best_state.tolist())
    return(state)
    
def Ideal_Cluster(both,them):
  finals=[]
  for di in range(0,2):
    p1=[]
    for i in range(len(both[di])):
      p1.append(loca(both[di][i]))
    df = pd.DataFrame(p1, columns = ['X','Y'])
    sum_squared_dist = []
    K = range(1,len(p1)+1)
    for k in K:
        km = KMeans(n_clusters=k, random_state=0)
        km = km.fit(p1)
        sum_squared_dist.append(km.inertia_)
    y = []
    for i in range(len(sum_squared_dist)):
        y.append(sum_squared_dist[i] - sum_squared_dist[i-1])
    x = range(1, len(y)+1)

    if(len(both[di])>3):  
      kn = KneeLocator(x, y, curve='convex', direction='decreasing')
      kmeans = KMeans(n_clusters=kn.knee, random_state=0).fit(p1)
      kmeans.labels_

      dl = pd.DataFrame({'Clusters':kmeans.labels_})
      dl1 = pd.DataFrame({'Location':both[di]})
      dd = df.assign(Clusters=dl.values)
      dt =dd.assign(Location=dl1.values)

      aa=set(kmeans.labels_.tolist())
      x=[]
      l=[]
      for i in range(0,len(aa)):
        x.append((dt.groupby("Clusters").get_group(i)).iloc[:,:2].values.tolist())
        l.append((dt.groupby("Clusters").get_group(i)).iloc[:,3].values.tolist())
        l[i].insert(0, them[di])
        x[i].insert(0,loca(them[di]))

    else:

      kmeans = KMeans(n_clusters=1, random_state=0).fit(p1)
      kmeans.labels_

      dl = pd.DataFrame({'Clusters':kmeans.labels_})
      dl1 = pd.DataFrame({'Location':both[di]})
      dd = df.assign(Clusters=dl.values)
      dt =dd.assign(Location=dl1.values)

      aa=set(kmeans.labels_.tolist())
      x=[]
      l=[]
      for i in range(0,len(aa)):
        x.append((dt.groupby("Clusters").get_group(i)).iloc[:,:2].values.tolist())
        l.append((dt.groupby("Clusters").get_group(i)).iloc[:,3].values.tolist())
        l[i].insert(0, them[di])
        x[i].insert(0,loca(them[di]))

    dd=[]
    for k in range(0,len(l)):
      mat=[]  
      for i in range(0,len(x[k])):
        ma=[]
        for j in range(0,i):
          if(i!=j):
            maa=[]
            maa.append(i)
            maa.append(j)
            maa.append(distance(x[k][i],x[k][j])) 
            ma.append(maa) 
        mat.append(ma)  
      dist_list = [x for x in mat if x != []]
      flat_list = []
      for sublist in dist_list:
          for item in sublist:
              flat_list.append(item)
      dd.append(flat_list)  
      
    state= tsp(dd,l)
    route=[]
    for i in range(0,len(state)):  
      print ('\nThe route', i+1,'for',them[di], 'is:') 
      route_list=[]
      for j in range(0,len(state[i])):
        print(l[i][j])
        route_list.append(l[i][j])
      route.append(route_list)
    finals.append(route)
  return(finals)
  
def Draw_Map(location_in_nashik,nashik_in_coord,location_in_pune,pune_in_coord,finals):
  colour=['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'lightred', 'beige', 'darkblue', 'darkgreen', 'cadetblue', 'darkpurple', 'white', 'pink', 'lightblue', 'lightgreen', 'gray', 'black', 'lightgray']

  pmap = folium.Map(loca("Maharashtra"), zoom_start=7)
  nashik=loca("Nashik")
  folium.Marker(location=nashik, popup="Warehouse", icon=folium.Icon(icon='home',color="Purple")).add_to(pmap)
  for i in range(0,len(location_in_nashik)):
    folium.Marker(location=nashik_in_coord[i], popup=location_in_nashik[i]).add_to(pmap)      
  for i in range(0,len(finals[0])):  
    for j in range(0,len(finals[0][i])-1):
      folium.PolyLine([loca(finals[0][i][j]),loca(finals[0][i][j+1])], line_opacity = 0.5, color=colour[i],line_weight=5).add_to(pmap)
  pune=loca("Pune")
  folium.Marker(location=pune, popup="Warehouse2",icon=folium.Icon(icon='home',color="Purple")).add_to(pmap)
  for i in range(0,len(location_in_pune)):
    folium.Marker(location=pune_in_coord[i], popup=location_in_pune[i]).add_to(pmap)
  for i in range(0,len(finals[1])):  
    for j in range(0,len(finals[1][i])-1):
      folium.PolyLine([loca(finals[1][i][j]),loca(finals[1][i][j+1])], line_opacity = 0.5, color=colour[i+10],line_weight=5).add_to(pmap)
  return(pmap)

def NashikDel(dfsales,finals,dff):  
  trucknames=[]
  for m in range(len(finals[0])):
    fii=finals[0] #nashik ka list from finals
    li=[]
    for i in range(1,len(fii[m])):
      b=dfsales.groupby('Customer Location').get_group(fii[m][i])
      c=b['TotalVol'].tolist()
      fors = [float(i) for i in c]
      li.append(sum(fors))
    a=[]
    for items in li:
      items=items*35.315
      a.append(items)
    b=[]
    for item in li:
      item=item*1000
      b.append(item)
    dfj = pd.DataFrame(list(zip(fii, li, a, b)),columns =['Customer Location', 'Total volume of boxes', 'Volume in cubic feet', 'Weight in kgs']) 

  for m in range(dfj.shape[0]):
    Volume=dfj['Volume in cubic feet'][m] 
    Weight=dfj['Weight in kgs'][m]

    best_Id=-1
    for j in range(0,dff.shape[0]):
      if(dff['Volume of Truck(cft)'][j]>=Volume):
        if(dff['Max Loading Weight (KG)'][j]>=Weight):    
          if(best_Id==-1):
            best_Id=j
          elif(dff['Volume of Truck(cft)'][best_Id]>dff['Volume of Truck(cft)'][j]):
            best_Id=j
    trucknames.append(dff['Truck name'][best_Id])
  Outfinal=''    
  for i in range(len(trucknames)):
    dfboxes=pd.DataFrame(columns =['Customer Name','Customer Location', 'Product ID', 'Material', 'No of Boxes' ])
    for count in range(0,len(dfsales)):
      df2 = {'Customer Name': dfsales['Customer Name'].iloc[count], 'Customer Location': dfsales['Customer Location'].iloc[count], 'Product ID': dfsales['Product Code'].iloc[count],'Material':dfsales['Material Discription'].iloc[count],'No of Boxes':dfsales['No. of Boxes'].iloc[count]}
      dfboxes = dfboxes.append(df2, ignore_index=True)
    dfforpath = dfboxes[(dfboxes['Customer Location'].isin(finals[0][i]))]
    clubbed=[]
    clubbed.append(dfforpath['Customer Location'].tolist())
    clubbed.append(dfforpath['Customer Name'].tolist())
    clubbed.append(dfforpath['Product ID'].tolist())
    clubbed.append(dfforpath['Material'].tolist())
    clubbed.append(dfforpath['No of Boxes'].tolist())
    index = pd.MultiIndex.from_arrays(clubbed,names=['Customer Name','Customer Location', 'Product ID', 'Material', 'No of Boxes'])
    hope = pd.Series("", index=index)
    trying=hope.to_string()
    iteration=str(i+1)
    sttr1='For Path '+iteration+' : '+str(finals[0][i])
    sttr2='\nTruck Name : '+str(trucknames[i]+'\n')
    sttr3=trying+'\n'
    Out=sttr1+sttr2+sttr3
    Outfinal+=Out
  return(Outfinal)

def PuneDel(dfsales,finals,dff):
  trucknames=[]
  for m in range(len(finals[1])):
    fii=finals[1] #pune ka list from finals
    li=[]
    for i in range(1,len(fii[m])):
      b=dfsales.groupby('Customer Location').get_group(fii[m][i])
      c=b['TotalVol'].tolist()
      fors = [float(i) for i in c]
      li.append(sum(fors))
    a=[]
    for items in li:
      items=items*35.315
      a.append(items)
    b=[]
    for item in li:
      item=item*1000
      b.append(item)
    dfj = pd.DataFrame(list(zip(fii, li, a, b)),columns =['Customer Location', 'Total volume of boxes', 'Volume in cubic feet', 'Weight in kgs']) 

  for m in range(dfj.shape[0]):
    Volume=dfj['Volume in cubic feet'][m] 
    Weight=dfj['Weight in kgs'][m]

    best_Id=-1
    for j in range(0,dff.shape[0]):
      if(dff['Volume of Truck(cft)'][j]>=Volume):
        if(dff['Max Loading Weight (KG)'][j]>=Weight):    
          if(best_Id==-1):
            best_Id=j
          elif(dff['Volume of Truck(cft)'][best_Id]>dff['Volume of Truck(cft)'][j]):
            best_Id=j
    trucknames.append(dff['Truck name'][best_Id])
  Outfinal=''
  for i in range(len(trucknames)):
    dfboxes=pd.DataFrame(columns =['Customer Name','Customer Location', 'Product ID', 'Material', 'No of Boxes' ])
    for count in range(0,len(dfsales)):
      df2 = {'Customer Name': dfsales['Customer Name'].iloc[count], 'Customer Location': dfsales['Customer Location'].iloc[count], 'Product ID': dfsales['Product Code'].iloc[count],'Material':dfsales['Material Discription'].iloc[count],'No of Boxes':dfsales['No. of Boxes'].iloc[count]}
      dfboxes = dfboxes.append(df2, ignore_index=True)
    dfforpath = dfboxes[(dfboxes['Customer Location'].isin(finals[1][i]))]
    clubbed=[]
    clubbed.append(dfforpath['Customer Location'].tolist())
    clubbed.append(dfforpath['Customer Name'].tolist())
    clubbed.append(dfforpath['Product ID'].tolist())
    clubbed.append(dfforpath['Material'].tolist())
    clubbed.append(dfforpath['No of Boxes'].tolist())
    index = pd.MultiIndex.from_arrays(clubbed,names=['Customer Name','Customer Location', 'Product ID', 'Material', 'No of Boxes'])
    hope = pd.Series("", index=index)
    trying=hope.to_string()
    iteration=str(i+1)
    sttr1='For Path '+iteration+' : '+str(finals[1][i])
    sttr2='\nTruck Name : '+str(trucknames[i]+'\n')
    sttr3=trying+'\n'
    Out=sttr1+sttr2+sttr3
    Outfinal+=Out
  return(Outfinal)

def Mapping(cssv,date):  
    dfsales = pd.read_csv(cssv)
    dfsales = dfsales.groupby('Date').get_group(date) 
    
    unique_location = get_unique_location(dfsales)
    
    all_locations_coord = get_all_locations_coord(unique_location)
    
    both,location_in_nashik,location_in_pune,nashik_in_coord,pune_in_coord,them = Warehouse_Distribution(all_locations_coord,unique_location)
    
    finals = Ideal_Cluster(both,them)
    
    pmap = Draw_Map(location_in_nashik,nashik_in_coord,location_in_pune,pune_in_coord,finals)
    
    pmap.save("mymap.html")
    import webbrowser
    webbrowser.open_new_tab("mymap.html")
    
def DeliveryDetails(cssv,date,textn,textp,sbn,sbp):
    dfsales = pd.read_csv(cssv)
    dfsale = dfsales.groupby('Date').get_group(date) 
    
    unique_location = get_unique_location(dfsale)
    
    all_locations_coord = get_all_locations_coord(unique_location)
    
    both,location_in_nashik,location_in_pune,nashik_in_coord,pune_in_coord,them = Warehouse_Distribution(all_locations_coord,unique_location)   
    finals = Ideal_Cluster(both,them)
    dff = pd.read_csv('truckdatafinal(Changed).csv')
    
    OutNashik = NashikDel(dfsale,finals,dff)
    OutPune = PuneDel(dfsale,finals,dff)
    textn.insert(tk.END,OutNashik)
    
    sbn.pack(side='right', fill='y')
    textn.pack(side='left', expand='yes')
    # Connect the scrollbars to the canvas.
    sbn['command']= textn.yview
    textn['yscrollcommand'] = sbn.set
    textn.place(x= 0,y=350 ,width=700, height=400)
    
    textp.insert(tk.END,OutPune)    
    
    sbp.pack(side='right', fill='y')
    textp.pack(side='left', expand='yes')
    # Connect the scrollbars to the canvas.
    sbp['command']= textp.yview
    textp['yscrollcommand'] = sbp.set
    textp.place(x= 700,y=350 ,width=650, height=400)
    return(textn,textp,sbn,sbp)
    
def sendSMS(mobile,message):
    import requests
    url = "https://www.fast2sms.com/dev/bulk"
    flash='0'
    api_key='yPZJR4XECeaTYWBNsVUzgpi1rm9kbu6xhltIdFnHvA0GOqjMc7tdwbVYJaQuXRho8i6cNKHenOl0p9rU'
    querystring = {"authorization":api_key,"sender_id":"FSTSMS","message":message,"language":"english","route":"p","numbers":mobile,"flash":flash}
    headers = {'cache-control': "no-cache"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    print(response.text)
    
def OpenServer(lbl):    
    import socket			 
    #create a socket object 
    s = socket.socket()		 
    #print("Socket successfully created")
    port = 9001				
    s.bind(('', port))		 
    s.listen(5)	
    running = True
    while running: 		
        # Establish connection with client. 
        c, addr = s.accept()	 
        #print("Got connection from", addr) 
        #message = c.recv(1024).decode() 
        msg=c.recv(1024).decode()
        current_value = lbl.cget("text")
        new_value = current_value +'\n'+ msg
        #Receives Message
        print(msg) 
        # Close the connection with the client 
        c.close() 
        running = False
    return(lbl.config(text=''+new_value,borderwidth=2, relief="solid"))
