import urllib.request as req
import urllib.error as urlerr
import json


_steamFriendsCache = {}

def getFriendsForSteamId(steamId: str, steamApiKey: str):

    print("Retrieving steam friends for id " + steamId)

    if steamId in _steamFriendsCache:
        print("Got data from cache!")
        return _steamFriendsCache[steamId]

    else:

        friendIds = []

        requestUrl = "http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key=" + steamApiKey + "&steamid=" + steamId + "&relationship=friend&format=json"
        print(requestUrl)

        #Handle private profiles
        try:
            response = req.urlopen(requestUrl)
        except urlerr.HTTPError:
            return friendIds

        data = json.load(response)

        #Get all the steamids from the API request in the array. 
        for elem in data["friendslist"]["friends"]:
            friendIds.append(elem["steamid"])

        _steamFriendsCache[steamId] = friendIds

        return friendIds

_steamIdInfoCache = {}

def getInfosFromSteamId(steamId: str, steamApiKey: str):

    print("Retrieving steam infos for id " + steamId)

    if steamId in _steamIdInfoCache:
        print("Got data from cache!")
        return _steamIdInfoCache[steamId]

    name = ""
    requestUrl =  "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=" + steamApiKey + "&steamids=" + steamId
    print(requestUrl)

    #Handle private profiles
    try:
        response = req.urlopen(requestUrl)
    except urlerr.HTTPError:
        return name

    data = json.load(response)

    #Next line is pure oof.
    elem = data["response"]["players"][0]
    
    _steamIdInfoCache[steamId] = elem

    return elem
