import pyexiv2 as ev
import math

def to_deg(value, loc):
    """convert decimal coordinates into degrees, munutes and seconds tuple

    Keyword arguments: value is float gps-value, loc is direction list ["S", "N"] or ["W", "E"]
    return: tuple like (25, 13, 48.343 ,'N')
    """
    if value < 0:
        loc_value = loc[0]
    elif value > 0:
        loc_value = loc[1]
    else:
        loc_value = ""
    abs_value = abs(value)
    deg =  int(abs_value)
    t1 = (abs_value * 60 - deg * 60)
    min = int(t1)
    sec = round((t1 - min) * 60, 5)
    return (deg, min, sec, loc_value)


def set_gps_location(file_name, lat, lng, alt):
    """Adds GPS position as EXIF metadata

    Keyword arguments:
    file_name -- image file
    lat -- latitude (as float)
    lng -- longitude (as float)
    alt -- altitude (as float)
    """
    lat_deg = to_deg(lat, ["S", "N"])
    lng_deg = to_deg(lng, ["W", "E"])
    if alt < 0:
        alt_deg = (alt, bytes(1))
    else:
        alt_deg = (alt, bytes(0))

    print lat_deg
    print lng_deg
    print alt_deg

    # class pyexiv2.utils.Rational(numerator, denominator) => convert decimal coordinates into degrees, munutes and seconds
    exiv_lat = (ev.Rational(lat_deg[0]*60+lat_deg[1],60),ev.Rational(lat_deg[2]*100,6000), ev.Rational(0, 1))
    exiv_lng = (ev.Rational(lng_deg[0]*60+lng_deg[1],60),ev.Rational(lng_deg[2]*100,6000), ev.Rational(0, 1))
    exiv_alt = (ev.Rational(alt * 1000, 1000))

    exiv_image = ev.ImageMetadata(file_name)
    exiv_image.read()

    # modify GPSInfo of image
    exiv_image["Exif.GPSInfo.GPSLatitude"] = exiv_lat
    exiv_image["Exif.GPSInfo.GPSLatitudeRef"] = lat_deg[3]
    exiv_image["Exif.GPSInfo.GPSLongitude"] = exiv_lng
    exiv_image["Exif.GPSInfo.GPSLongitudeRef"] = lng_deg[3]
    exiv_image["Exif.GPSInfo.GPSAltitude"]= exiv_alt
    exiv_image["Exif.GPSInfo.GPSAltitudeRef"] = alt_deg[1]
    exiv_image["Exif.Image.GPSTag"] = 654
    exiv_image["Exif.GPSInfo.GPSMapDatum"] = "WGS-84"
    exiv_image["Exif.GPSInfo.GPSVersionID"] = '2 2 0 0'

    exiv_image.write()

set_gps_location('IMG_5719.JPG', 30.22222, 110.22222, 9.8111)