import os
from exif import Image
import json
import utm
import sys
import pdb

pasta = r'C:\Originais de Voo\Ibaté'
name_file = (pasta.split('\\')[-1])
zone_number = 22
zone_letter = 'K'

def get_dji_meta( filepath ):
    """
    Returns a dict with DJI-specific metadata stored in the XMB portion of the image
    """
    # list of metadata tags
    djimeta=["AbsoluteAltitude","RelativeAltitude","GimbalRollDegree","GimbalYawDegree",\
         "GimbalPitchDegree","FlightRollDegree","FlightYawDegree","FlightPitchDegree"]
    
    # read file in binary format and look for XMP metadata portion
    fd = open(filepath,'rb')
    d= fd.read()
    xmp_start = d.find(b'<x:xmpmeta')
    xmp_end = d.find(b'</x:xmpmeta')

    # convert bytes to string
    xmp_b = d[xmp_start:xmp_end+12]
    xmp_str = xmp_b.decode()
    
    fd.close()
    
    # parse the XMP string to grab the values
    xmp_dict={}
    for m in djimeta:
        istart = xmp_str.find(m)
        ss=xmp_str[istart:istart+len(m)+10]
        val = float(ss.split('"')[1])
        xmp_dict.update({m : val})

    return xmp_dict


def document(name, datetime, photographic_sensitivity, focal_length, exposure_time, aperture_value, exposure_bias_value, latitude, longitude, easting,northing,zone_number,zone_letter, altitude_abs, altitude_rel, gimbalrolldegree, gimbalyawdegree, gimbalpitchdegree, flightrolldegree, flightyawdegree, flightpitchdegree):
    doc = {'Name': name,
        'Datetime' : datetime,
        'PhotographicSensitivity' : photographic_sensitivity,
        'FocalLength' : focal_length,
        'ExposureTime' : exposure_time,
        'ApertureValue' : aperture_value,
        'ExposureBiasValue' : exposure_bias_value,
        'Latitude' : latitude,
        'Longitude' : longitude,
        'Easting' : easting,
        'Northing' : northing,
        'ZoneNumber': zone_number,
        'ZoneLetter': zone_letter,
        'AbsoluteAltitude': altitude_abs, 
        'RelativeAltitude': altitude_rel, 
        'GimbalRollDegree': gimbalrolldegree, 
        'GimbalYawDegree': gimbalyawdegree, 
        'GimbalPitchDegree': gimbalpitchdegree, 
        'FlightRollDegree': flightrolldegree, 
        'FlightYawDegree': flightyawdegree, 
        'FlightPitchDegree': flightpitchdegree}
    return doc


json_data = {
    'project name' : name_file,
    'path' : pasta,
    'database' : []
}


for nome_arquivo in os.listdir(pasta):
    nome, extensao = os.path.splitext(nome_arquivo)
    caminho = fr'{pasta}/{nome_arquivo}'
    if extensao == ".JPG":
        with open(caminho, 'rb') as image_file:
            my_image = Image(image_file)
            lat = -1* (int(my_image.gps_latitude[0]) + ((my_image.gps_latitude[1]/60) + (my_image.gps_latitude[2]/3600)))
            long = -1* (int(my_image.gps_longitude[0]) + ((my_image.gps_longitude[1]/60) + (my_image.gps_longitude[2]/3600)))            
            coordenadas_utm = utm.from_latlon(lat, long, zone_number, zone_letter)
            datetime = my_image.datetime
            photographic_sensitivity = my_image.photographic_sensitivity
            focal_length = my_image.focal_length
            exposure_time = my_image.exposure_time
            aperture_value = my_image.aperture_value
            exposure_bias_value = my_image.exposure_bias_value
            xmp = get_dji_meta(caminho)
            altitude_abs = xmp['AbsoluteAltitude']
            altitude_rel = xmp['RelativeAltitude']
            gimbalrolldegree = xmp['GimbalRollDegree']
            gimbalyawdegree = xmp['GimbalYawDegree']
            gimbalpitchdegree = xmp['GimbalPitchDegree']
            flightrolldegree = xmp['FlightRollDegree']
            flightyawdegree = xmp['FlightYawDegree']
            flightpitchdegree = xmp['FlightPitchDegree']
            json_data['database'].append(document(nome, datetime, photographic_sensitivity, focal_length, exposure_time, aperture_value, exposure_bias_value, lat, long, coordenadas_utm[0],coordenadas_utm[1],zone_number,zone_letter, altitude_abs, altitude_rel, gimbalrolldegree, gimbalyawdegree, gimbalpitchdegree, flightrolldegree, flightyawdegree, flightpitchdegree))
           
with open(f'{name_file}.json', 'w', encoding= 'utf-8') as f:
    json.dump(json_data, f)
