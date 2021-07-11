import json
# import Coordinates
import FileUtilities
import pandas as pd
import CoordinatesService as cs


class Coordinates(object):

    latitude = 0
    longitude = 0
    name = ""
    description = ""

    def __init__(self, latitude, longitude, name, description):
        self.latitude = latitude
        self.longitude = longitude
        self.name = name
        self.description = description

class DataProcessingService:
    a = 1

def addNswFireIncidents(geojson, nswFireIncidents):
    nswFireIncidents = processNswFireIncidents()
    print(type(nswFireIncidents))

    # {"type": "Feature",
    #  "geometry": {"type": "Point", "coordinates": [102.0, 0.5]},
    #  "properties": {"prop0": "value0"}
    # }
    features = list()
    for coordinate in nswFireIncidents:
        feature = dict(type="Feature",
                       geometry={"type": "Point",
                                 "coordinates": [float(coordinate.longitude), float(coordinate.latitude)]},
                       properties={"name": coordinate.name, "description": coordinate.description, "size": 4000})
        features.append(feature)
    geojson['features'] = features
    return geojson


def createFireIncidentsGeoJson():
    geojson = FileUtilities.createGeoJsonFilePrefix()
    geojson = addNswFireIncidents(processNswFireIncidents())
    FileUtilities.writeToFile("fire.geojson", geojson)

def processNswFireIncidents():
    coordinatesList = list()
    jsonData = json.load(open("nswFireIncidents.json"))
    items = jsonData['rss']['channel']['item']
    for item in items:
        coordinates = item['point']['#text'].split(" ")
        name = item['title']
        description = item['description']
        coordinatesObject = Coordinates(coordinates[0], coordinates[1], name, description)
        coordinatesList.append(coordinatesObject)
    return (coordinatesList)

def populatePrdData(geojson, prdData):
    # {
    #     "type": "Feature",
    #     "properties": {"party": "Republican"},
    #     "geometry": {
    #         "type": "Polygon",
    #         "coordinates": [[
    #             [-104.05, 48.99],
    #             [-97.22, 48.98],
    #             [-96.58, 45.94],
    #             [-104.03, 45.94],
    #             [-104.05, 48.99]
    #         ]]
    #     }
    # }

    polygonIds = list(set(prdData['ID']))
    print(polygonIds)
    features = list()

    for polygonId in polygonIds:
        if(polygonId != "D104C"):
            continue
        feature = dict(type="Feature",
                       geometry={"type": "Polygon",
                                 "coordinates": list()},
                       properties={"ID": polygonId})
        coordinates = list()
        prdDataIndividuals = prdData[prdData['ID'] == polygonId]
        print(polygonId + "-> " + str(prdDataIndividuals.shape[0]))
        print(prdDataIndividuals['latitude'])

        firstCoordinate = [0,0]
        for i in prdDataIndividuals.index:
            latitude = float(prdDataIndividuals['latitude'][i])
            longitude = float(prdDataIndividuals['longitude'][i])
            coordinate = [longitude, latitude]
            if (int(prdDataIndividuals['Seqn'][i]) == 1):
                firstCoordinate =coordinate
            coordinates.append(coordinate)
        coordinates.append(firstCoordinate)
        coordinatesList = list()
        coordinatesList.append(coordinates)

        feature['geometry']['coordinates'] = coordinatesList
        features.append(feature)
    geojson['features'] = features
    return geojson


def processPrdData():
    geojson = FileUtilities.createGeoJsonFilePrefix()
    prdData = cleanPrdDate("prd.csv")
    geojson = populatePrdData(geojson, prdData)
    FileUtilities.writeToFile("prdData.geojson", geojson)

def cleanPrdDate(fileName):
    prdDataSet = pd.read_csv(fileName)

    # Latitude, Longitude cleaning
    coordinates = pd.DataFrame(columns=['latitude', 'longitude', 'latitudeOfOrigin', 'longitudeOfOrigin'], index=prdDataSet.index)

    for id in prdDataSet.index:
        coordinates['latitude'][id] = cs.DMSToDecimalDegrees(str(prdDataSet['Latitude'][id]))
        coordinates['longitude'][id] = cs.DMSToDecimalDegrees(str(prdDataSet['Longitude'][id]))
        coordinates['latitudeOfOrigin'][id] = cs.DMSToDecimalDegrees(str(prdDataSet['Latitude of Origin'][id]))
        coordinates['longitudeOfOrigin'][id] = cs.DMSToDecimalDegrees(str(prdDataSet['Longitude of Origin'][id]))

    prdDataSet = pd.concat([prdDataSet, coordinates], axis=1)

    prdDataSet = prdDataSet.drop(['Latitude', 'Longitude', 'Latitude of Origin', 'Longitude of Origin'], axis=1)
    prdDataSet.to_csv('prdFinal.csv', index=False, header=True)

    return prdDataSet



