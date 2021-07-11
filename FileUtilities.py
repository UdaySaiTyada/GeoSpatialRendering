import xmltodict
import json


class FileUtilities:
    help = ""


def writeToFile(fileName, data):
    with open(fileName, 'w') as outfile:
        json.dump(data, outfile)

def convertXmlToJson(name):
    with open(name) as xml_file:
        data_dict = xmltodict.parse(xml_file.read())

    xml_file.close()
    json_data = json.dumps(data_dict)
    return json.loads(json_data)

def createGeoJsonFilePrefix():
    geojson = dict(type = "FeatureCollection", features = [])
    return geojson