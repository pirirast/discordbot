import json
import requests
import html
import re
#Module for reading from the SFU Road Conditions API
#Returns pretty formatted plaintext strings for whatever use.
#API URL: http://www.sfu.ca/security/sfuroadconditions/api/2/current


def get():
    #returns a dictionary with the data retrieved from the api call
    response = requests.get("http://www.sfu.ca/security/sfuroadconditions/api/3/current")
    return response.json()


def announcements(campus="burnaby"):
    #fetch data
    data = get()
    #extract string
    str = data["campuses"][campus.lower()]["announcements"]
    #fix html entities
    str = html.unescape(str)
    #fix html tags
    str = re.sub('<[^<]+?>', '', str)
    str = re.sub("\n\s*\n*", "\n", str)
    if str == "":
        str = "No announcement for the {0} campus.".format(campus.capitalize())
    return str


def road_condition(campus="burnaby"):
    #fetch data
    data = get()
    #start building return string
    doc = "{0} road conditions:\n".format(campus.capitalize())
    try:
        for condition in data["campuses"][campus.lower()]["roads"].items():
            doc += "{0} => {1}\n".format(condition[0].capitalize(), condition[1].capitalize())
    except KeyError:
        doc = "Campus {0} not found.".format(campus.capitalize())
    return doc
