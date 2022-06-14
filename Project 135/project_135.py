# -*- coding: utf-8 -*-
"""Project 135.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1XuuMnmq3Qe9jLIBO69y8BjMuEpNu676V
"""

from google.colab import files
filesToUpload = files.upload()

from sklearn.cluster import KMeans

import csv
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

row = []

with open("final.csv", "r") as f:
  csvReader = csv.reader(f)

  for i in csvReader:
    row.append(i)


headers = row[0]
planet_data = row[1:] 

print(headers)
print(planet_data[0])

headers[0] = "row_num"

no_of_planet_in_solar_system = {}

for j in planet_data:
  if no_of_planet_in_solar_system.get(j[11]):
    no_of_planet_in_solar_system[j[11]]+=1
  else:
    no_of_planet_in_solar_system[j[11]] = 1
  
max_solar_system = max(no_of_planet_in_solar_system, key = no_of_planet_in_solar_system.get)

print("The Solar System {} has maximum planets {} out of the entire data".format(max_solar_system, no_of_planet_in_solar_system[max_solar_system]))

KOI_351_planet_list = []

for k in planet_data:
  if max_solar_system == k[11]:
    KOI_351_planet_list.append(k)
  
print(len(KOI_351_planet_list))
print(KOI_351_planet_list)

planet_data_conversion = list(planet_data)

for l in planet_data_conversion:
  planet_mass = l[3]
  
  if planet_mass == "Unknown":
    planet_data.remove(l)
    continue
  else:
    planet_mass_value = planet_mass.split(" ")[0]
    planet_mass_ref = planet_mass.split(" ")[1]
    
    if planet_mass_ref == "Jupiters":
      planet_mass_value = float(planet_mass_value) * 317.8 
    
    l[3] = planet_mass_value
    
    planet_radius = l[7]
    
    if planet_radius == "Unknown":
      planet_data.remove(l)
      continue
    else:
      planet_radius_value = planet_radius.split(" ")[0]
      planet_radius_ref = planet_radius.split(" ")[2]

      if planet_radius_ref == "Jupiters":
        planet_radius_value = float(planet_radius_value) * 11.2

    l[7] = planet_radius_value

print(len(planet_data))
print(planet_data_conversion)

KOI_351_planet_mass = []
KOI_351_planet_names = []

for m in KOI_351_planet_list:
  KOI_351_planet_mass.append(m[3])
  KOI_351_planet_names.append(m[1])

KOI_351_planet_mass.append(1)
KOI_351_planet_names.append("Earth")

fig = px.bar(x = KOI_351_planet_names, y = KOI_351_planet_mass)
fig.show()

planet_masses = []
planet_names = []
planet_radii = []

for n in planet_data:
  planet_masses.append(n[3])
  planet_radii.append(n[7])
  planet_names.append(n[1])

planet_gravity = []

for o, name in enumerate(planet_names):
  gravity = (float(planet_masses[o])* 5.972e+24) / (float(planet_radii[o])*float(planet_radii[o]) * 6371000 * 6371000) * 6.674e-11
  planet_gravity.append(gravity)

fig = px.scatter(x = planet_radii, y = planet_masses, size = planet_gravity, hover_data = [planet_names]) 
fig.show()

low_gravity_planet = []
high_gravity_planet = []

for p, gravity in enumerate(planet_gravity):
  if gravity < 200:
    low_gravity_planet.append(planet_data[p])
  else:
    high_gravity_planet.append(planet_data[p])

print(len(low_gravity_planet))
print(len(high_gravity_planet))

planet_type_var = []

for q in planet_data:
  planet_type_var.append(q[6])

print(list(planet_type_var))

planet_masses_type = []
planet_radii_type = []

for r in planet_data:
  planet_masses_type.append(r[3])
  planet_radii_type.append(r[7])

fig = px.scatter(x = planet_radii_type, y = planet_masses_type)
fig.show()

X = []

for s,t in enumerate(planet_masses_type):
  temp_list = [planet_radii_type[s], t]
  X.append(temp_list)

wcss = []

for u in range(1, 11):
  kmeans = KMeans(n_clusters = u, init = "k-means++", random_state = 42)
  kmeans.fit(X)
  wcss.append(kmeans.inertia_)

plt.figure(figsize = (10, 5))

sns.lineplot(range(1, 11), wcss, marker = "o", color = "orange")

plt.title("Planet Type - Elbow Method")
plt.xlabel("No. of clusters")
plt.ylabel("wcss")
plt.show()

fig = px.scatter(x = planet_radii_type, y = planet_masses_type, color = planet_type_var)
fig.show()

fig = px.bar(x = planet_names, y = planet_masses, hover_data = [planet_names]) 
fig.show()

fig = px.bar(x = planet_names, y = planet_radii, hover_data = [planet_names]) 
fig.show()

fig = px.bar(x = planet_names, y = planet_gravity, hover_data = [planet_names]) 
fig.show()