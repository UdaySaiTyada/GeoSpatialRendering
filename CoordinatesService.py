import StringUtilities

class CoordinatesService:
    a = 1

def DMSToDecimalDegrees(DMSString):
    if(StringUtilities.isBlank(DMSString)):
        return ""

    values = DMSString.split(" ")
    seconds, direction = values[2][0:len(values[2]) - 1], values[2][-1]
    TheLatitudeValue = float(values[0]) + ((float(values[1])) / 60) + ((float(seconds)) / 3600)

    if (direction == "W" or direction == "S"):
        TheLatitudeValue = 0 - TheLatitudeValue

    return TheLatitudeValue