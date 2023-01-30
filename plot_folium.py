import os
from exif import Image
import folium
from folium import LayerControl, FeatureGroup
from folium.plugins import MeasureControl, LocateControl, Search
from pathlib import Path
from os.path import getmtime

pasta = r"D:\Originais de Voo\Ibaté- parte 4"


name_file = (pasta.split('\\')[-1])

doc = {}
for nome_arquivo in os.listdir(pasta):
    nome, extensao = os.path.splitext(nome_arquivo)
    caminho = fr'{pasta}/{nome_arquivo}'
    if extensao == ".JPG":
        with open(caminho, 'rb') as image_file:
            my_image = Image(image_file)
            my_image.has_exif
            latitude = -1* (int(my_image.gps_latitude[0]) + ((my_image.gps_latitude[1]/60) + (my_image.gps_latitude[2]/3600)))
            longitude = -1* (int(my_image.gps_longitude[0]) + ((my_image.gps_longitude[1]/60) + (my_image.gps_longitude[2]/3600)))
            doc[nome] = (latitude,longitude)

if len(doc) == 0:
    print('Pasta sem imagens')
    exit()


# Descobrir uma coordenada para abrir o mapa
center_map = list(doc.values())[int(len(doc)/2)]

# Abrir mapa na coordenada central da localização
map = folium.Map(location = center_map, 
                 zoom_start = 15, zoom_control= True, 
                 max_zoom= 30, 
                 tiles = None 
                 )

# Inserindo camadas do Google
folium.TileLayer(
    tiles= 'OpenStreetMap',
    name= 'OpenStreetMap',
    overlay= False,
    control= True,
    max_zoom= 30,   
).add_to(map)
folium.TileLayer(
    tiles= 'http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
    attr= 'google',
    name= 'Satélite',
    subdomains = ['mt0','mt1','mt2','mt3'],
    overlay= False,
    control= True,
    max_zoom= 30,   
).add_to(map)
folium.TileLayer(
    tiles= 'http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',
    attr= 'google',
    name= 'Google Maps',
    subdomains = ['mt0','mt1','mt2','mt3'],
    overlay= False,
    control= True,
    max_zoom= 30    
).add_to(map)
folium.TileLayer(
    tiles= 'http://{s}.google.com/vt/lyrs=p&x={x}&y={y}&z={z}',
    attr= 'google',
    name= 'Terrain',
    subdomains = ['mt0','mt1','mt2','mt3'],
    overlay= False,
    control= True,
    max_zoom= 50    
).add_to(map)
folium.TileLayer(
    tiles= 'https://{s}.google.com/vt/lyrs=m@221097413,traffic&x={x}&y={y}&z={z}',
    attr= 'google',
    name= 'Traffic',
    subdomains = ['mt0','mt1','mt2','mt3'],
    overlay= False,
    control= True,
    max_zoom= 30    
).add_to(map)
map.add_child(folium.LatLngPopup())
MeasureControl(position= 'bottomleft').add_to(map)
LayerControl(position= 'bottomright').add_to(map)
LocateControl(position= 'bottomright', returnToPrevBounds = True, strings = {'title':'Ver sua localização atual', 'popup':"Sua Posição" }).add_to(map)

for key, value in doc.items():
    folium.Circle(location= value, popup= f'http://moduloautoma.ddns.net:888/plataforma/originaisdevoo/{name_file}/{key}.png', radius= 4, fill_color="grey", fill_opacity=0.7, color="grey", weight=1, tooltip= key).add_to(map)
map.save(f'{name_file}.html')     

print(name_file)
# Relatorio arquivos
#directory = Path(pasta)
#files = directory.glob('*.JPG')
#arquivo_mais_recente = max(files, key=getmtime)

