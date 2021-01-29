# принимает два  csv файла с проекцией 3857
import csv
import requests
from pyproj import Proj, transform
from xml.dom import minidom
from geopy import distance 
from shapely.wkt import loads
from bs4 import BeautifulSoup

yourNavigationBaseURL__ = 'http://www.yournavigation.org/api/dev/route.php?flat=%s&distance=v&flon=%s&tlat=%s&tlon=%s&v=motorcar&fast=0&layer=mapnik&instructions=0'


with open('building.csv', mode='r') as csv_file:
    building = []
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for row in csv_reader:
        building.append(row)

with open('medical.csv', mode='r') as csv_file:
    medical = []
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for row in csv_reader:
        medical.append(row)


def transform_back(x,y):
    outProj = Proj('epsg:3857')
    inProj = Proj('epsg:4326')
    x,y = transform(inProj,outProj,x,y)
    return x,y


def transform_projection(x,y):
    inProj = Proj('epsg:3857')
    outProj = Proj('epsg:4326')
    x,y = transform(inProj,outProj,x,y)
    return x,y

def get_distance(x1,y1,x2,y2):
    x1 ,y1 = transform_projection(x1,y1)
    x2 , y2 = transform_projection(x2,y2)
    url = yourNavigationBaseURL__ % (x1,y1,x2,y2)
    r = requests.get(url)
    return parser(r.text)




def parser(r):
    soup = BeautifulSoup(r,"lxml")
    distance = soup.find('distance').text
    return distance
    # responseData = minidom.parseString(r)
    # distance = responseData.getElementsByTagName('distance')[0].text
    # print (distance)


csv_columns = ['fid','q','x','y','distance_to_point']
def return_output():
    csv_file = "new_building.csv"
    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in building:
                writer.writerow(data)
    except IOError:
        print("I/O error")

for build in building:
    #do такую то функцию и возврати расстояние через апи
    x1,y1 = build['x'],build['y']
    distances = []
    
    for med in medical:
        x2,y2 = med['x'],med['y']
        dist = get_distance(x1,y1,x2,y2)
        distances.append(dist)
    build['distance_to_point'] = (min(distances))
    print(distances)
    return_output()

print (building)
