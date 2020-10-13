import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import pylab
import re
import json
import sys
import urllib.request
import dl_steamdata

if __name__ == '__main__':

    #Check if args are provided.
    
    #Input part
    enteredSteamIds = []
    idInput = input("Enter the wished steamIDs. Use a comma ',' for multiple entries:")
    idInput.replace(" ", "")
    enteredSteamIds = idInput.split(",")
    steamAPIKey = input("Enter your steamAPI key. ( https://steamcommunity.com/dev/apikey ):")

    #Create Graph and add edges from entered ids
    G = nx.Graph()
    G.add_nodes_from(enteredSteamIds)

    #Array of colors for draw function
    colorsMap = {}

    #Get friends of entered steam IDs and create edges
    for steamID in enteredSteamIds:
        friends = dl_steamdata.getFriendsForSteamId(steamID, steamAPIKey)
        G.add_nodes_from(friends)
        

        
        #Go through all friends of "steamID" and find connections between their firends and "steamID"'s friends.
        for friend in friends:

            G.add_edges_from([(steamID, friend)])
            
            

            friends2 = dl_steamdata.getFriendsForSteamId(friend, steamAPIKey)
            G.add_nodes_from(friends2)

            for friend2 in friends2:

                G.add_edges_from([(friend, friend2)])
                #Add friend to color map
                colorsMap[friend2] = "#009e4c"

                friends3 = dl_steamdata.getFriendsForSteamId(friend2, steamAPIKey)

                for friend3 in friends3:
                    if friend3 in friends2:
                        G.add_edges_from([(friend2, friend3)])
        
        for friend in friends:
            #Add friend to color map
            colorsMap[friend] = "#00fc60"

    for steamID in enteredSteamIds:  
        #Add color mapping here to prevent overwrites from previous accesses.
        colorsMap[steamID] = "#0a009e"

    #Get names of steamids
    labelDictionary = {}
    for node in G.nodes:
        steamUserInfos = dl_steamdata.getInfosFromSteamId(node, steamAPIKey)
        #Remove $ to fix string problems... 
        nickname: str = re.sub("[$]*", "", steamUserInfos["personaname"])
        if nickname != "":
            labelDictionary[node] = nickname

    colorVals = []

    #Create color array for nodes
    for node in G.nodes():
        colorVals.append(colorsMap[node])

    nx.draw(G, labels=labelDictionary, node_color=colorVals,
            with_labels=True, font_color="#fc009b")

    #nx.draw(G, labels=labelDictionary, node_color=colors, with_labels=True, font_color="#fc009b")

    #H = nx.relabel_nodes(G, labelDictionary, True)
    #nx.write_gml(H, "test.gml")

    plt.show()  # display
