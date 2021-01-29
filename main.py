import requests
from pyproj import Proj, transform
from xml.dom import minidom
from geopy import distance 
from shapely.wkt import loads

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


def coorOrganizer__(input=str):
    # Coordinates in [1.2, 5.7, 6.8, 9.1] style is converted to LineString(1.2 5.7, 6.8 9.1) style by this function.
    coorPair = [input[i:i + 2] for i in range(0, len(input), 2)]
    usefulPoly = []
    for i in coorPair:
        usefulPoly.append(" ".join(map(str, i)))
    wkt = 'LineString(%s)' % (','.join(usefulPoly))
    return wkt

def wktMaker__(response=str):
    responseData = minidom.parseString(response)
    coors = responseData.getElementsByTagName('coordinates')[0].firstChild.nodeValue.strip()
    commaCoors = coors.replace('\n', ',')
    usefulCoorList = []
    for i in commaCoors.split(','):
        usefulCoorList.append(float(i))

    return coorOrganizer__(usefulCoorList)



x1 = 7952815.486011353
y1 = 6654045.979371076
x2 = 7951729.234373041
y2 = 6650724.0702911215
x1,y1 = transform_projection(x1,y1)
x2,y2 = transform_projection(x2,y2)
yourNavigationBaseURL__ = 'http://www.yournavigation.org/api/dev/route.php?flat=%s&distance=gc&flon=%s&tlat=%s&tlon=%s&v=motorcar&fast=0&layer=mapnik&instructions=0'
url = yourNavigationBaseURL__ % (x1,y1,x2,y2)
r = requests.get(url)
wkt = wktMaker__(r.text)

# distance.VincentyDistance.ELLIPSOID = 'WGS-84'
# d = distance.distance

# line = loads(wkt)

# # convert the coordinates to xy array elements, compute the distance
# # dist = d(line.xy[0], line.xy[1])

print (r.text)
