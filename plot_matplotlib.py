import json
import matplotlib.pyplot as plt
import pandas as pd


with open('Ibaté_utm.json') as f:
    data = json.load(f)

df = pd.DataFrame(data['database'])

plt.scatter(df['Easting'], df['Northing'], s = 1)
plt.show()

'''
# Metodo muito demorado
for i in data['database']:
    plt.scatter(i['easting'], i['northing'], c= 'orange')
plt.show()
'''