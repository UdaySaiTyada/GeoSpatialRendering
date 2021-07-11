import json
import xmltodict
import DataProcessingService
import FileUtilities

NSW_FIRE_INCIDENTS = "nswFireIncidents.xml"


if __name__ == '__main__':
    ## POC 1  [XML to Json data]
    # jsonData = FileUtilities.convertXmlToJson(NSW_FIRE_INCIDENTS)
    # FileUtilities.writeToFile("nswFireIncidents.json", jsonData)

    ## POC 2   [Process nswFireIncidents.json]
    # DataProcessingService.processNswFireIncidents()

    ## POC 3 [Create GeoJson from nswFireIncident.json]
    # DataProcessingService.createFireIncidentsGeoJson()
    DataProcessingService.processPrdData()
