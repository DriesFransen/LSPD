import requests

def distance(loc1, loc2):
    return(abs(loc1[0]-loc2[0]) + abs(loc1[1]-loc2[1]))

def lat_lon(place_str):
    place_params = {"key":"7a56a66322134ad882bccac353755edf", "q":place_str}
    latlon_dict = requests.get("https://api.opencagedata.com/geocode/v1/json?", \
                          params=place_params).json()["results"][0]["geometry"]
    return(latlon_dict["lat"], latlon_dict["lng"])

def closest_to(place_str):
    place_latlon = lat_lon(place_str)
    distdict = {}
    stations = requests.get("https://data.buienradar.nl/2.0/feed/json").json()["actual"]["stationmeasurements"]
    for i in range(len(stations)):
        distdict[stations[i]["stationname"]] = distance((stations[i]["lat"], stations[i]["lon"]), \
                                                  (place_latlon[0], place_latlon[1]))
    return min(distdict, key=distdict.get)

def weather_data(place_str):
    place_latlon = lat_lon(place_str)
    weather_station = closest_to(place_str)
    station_measurements = requests.get("https://data.buienradar.nl/2.0/feed/json").json()\
            ["actual"]["stationmeasurements"]
    parameters = {"key":"48f5620fe7", "locatie":str(place_latlon[0])+','+str(place_latlon[1])}
    temp_dict = requests.get("http://weerlive.nl/api/json-data-10min.php?", \
                             params=parameters).json()['liveweer'][0]
    temp_dict.update([d for d in station_measurements if d["stationname"] == weather_station][0])
    return temp_dict
