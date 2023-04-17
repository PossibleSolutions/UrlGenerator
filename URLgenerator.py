# coding: utf-8

#this script produces additional link columns named 'Paikkatietoikkuna' and 'VanhatKartat'
#these additional map services include historical aerial images and basemaps for visual
#inspection of time dependent changes

#the user needs to change data input "YourDataPath" (row 16) and output "DataOut.gpkg" (row 70) names 

#load necessary modules
import re
import geopandas as gpd
import pandas as pd
import numpy as np

#read data that will get additional columns describink links to external services such as paikkatietoikkuna and vanhat kartat
df = gpd.read_file(r"YourDataPath")


#PAIKKATIETOIKKUNA (https://kartta.paikkatietoikkuna.fi/)
#produces a centroid coulumn used for zooming
df['centroid']=df.centroid

#link in parts
part1=r'https://kartta.paikkatietoikkuna.fi/?zoomLevel=10&coord='
centroidstring=df['centroid'].astype(str)
part3='_'
part2=centroidstring.str.extract('(\\d\\d\\d\\d\\d\\d)')
part4=centroidstring.str.extract('( \\d\\d\\d\\d\\d\\d\\d)')
#shortened version of a too long url
part5=r'&mapLayers=801+100+,3400+100+ortokuva:indeksi,90+100+,99+100+,2622+61+,722+50+,511+50+&timeseries=1950&noSavedState=true&showMarker=true&showIntro=false'
#alternative ways
#shortened version of too long url,without map marker
#part5=r'&mapLayers=801+100+default,3400+100+ortokuva:indeksi,90+100+default,99+100+default,2622+61+default,722+50+default,511+50+default&timeseries=1950&noSavedState=true&showIntro=false'
#with other maps on top
#part5=r'&mapLayers=801+100+default,3400+100+ortokuva:indeksi,90+100+default,99+100+default,2622+61+default,722+50+default,511+50+default&timeseries=1950&noSavedState=true&showMarker=true&showIntro=false'
#without map marker
#part5=r'&mapLayers=801+100+default,722+100+default,511+100+default,2622+100+default,90+100+default,99+100+default,3400+100+ortokuva:indeksi&timeseries=1950&noSavedState=true&showIntro=false'
#with map marker
#part5=r'&mapLayers=801+100+default,722+100+default,511+100+default,2622+100+default,90+100+default,99+100+default,3400+100+ortokuva:indeksi&timeseries=1950&noSavedState=true&showMarker=true&showIntro=false'
#without extra layers
#part5=r'&mapLayers=801+100+default,3400+100+ortokuva:indeksi&timeseries=1950&noSavedState=true&showIntro=false&lang=fi'
df['Paikkatietoikkuna']=part1+part2+part3+part4+part5
df['Paikkatietoikkuna']=df['Paikkatietoikkuna'].str.replace(" ","")



# VANHAT KARTAT (https://vanhatkartat.fi/#12.3/65.00854/25.46662)
#vanhatkartat.fi is in wgs84, so the data is reprojected to wgs84
df=df.to_crs(4326)
df['centroid']=df.centroid
centroidstring_wgs84=df['centroid'].astype(str)

#link in parts
part1=r'https://vanhatkartat.fi/#13/'
part2=centroidstring_wgs84.str.extract('( \\d\\d\\.\\d\\d\\d\\d\\d)')
part3='/'
part4=centroidstring_wgs84.str.extract('(\\d\\d\\.\\d\\d\\d\\d\\d)')
df['VanhatKartat']=part1+part2+part3+part4
df['VanhatKartat']=df['VanhatKartat'].str.replace(" ","")



#two geometry columns creates problems
df=df.drop(columns='centroid')

#convert back to eureffin (most common projection in Finland)
df=df.to_crs(3067)

#save to file. can also be other format than geopackage
df.to_file(r"DataOut.gpkg", layer='LayerName', driver="GPKG")