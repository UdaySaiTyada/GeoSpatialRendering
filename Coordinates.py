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