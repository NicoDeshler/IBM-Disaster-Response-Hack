# Imports
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import requests
import polyline
import numpy as np
import networkx as nx
import webbrowser
import urllib.request
from PIL import Image

# Google Maps Account Key
API_KEY = "AIzaSyBlPHAYsu_KjwqrZj3LK_3RdCw4aDLdSPI"

# this is just for testing my implementation (ML_output here is dummy test input)
ML_output = [[(37.874824, -122.262206),(37.874383, -122.268643), 3],[(37.874383, -122.268643),(37.874214, -122.268643), 1],[(37.874214, -122.268643),(37.872181, -122.268429), 2],[(37.874214, -122.268643),(37.878380, -122.269159), 1]]

def create_map_and_graph(ML_output):
    G = nx.Graph()
    for i in np.arange(len(ML_output)):
        G.add_edge(ML_output[i][0], ML_output[i][1], weight=ML_output[i][2])
    astar_path = nx.astar_path(G, ML_output[0][0], ML_output[len(ML_output)-1][1], weight='weight')
    
    original_path = ""
    for i in np.arange(len(astar_path)):
        original_path += str(astar_path[i][0]) + "," + str(astar_path[i][1]) + "|"
    original_path = original_path[:-1]
    
    r = requests.post("https://roads.googleapis.com/v1/snapToRoads?path=" + original_path + "&interpolate=true&key=" + API_KEY)
    text = r.text.replace('latitude', 'x').replace('longitude', 'y')
    x_values = []
    y_values = []
    text_len = len(text)
    for i in np.arange(text_len):
        if text[i-1] == '"' and text[i] == 'x' and i+4 < text_len and i+4+text[i+4:].index(',') < text_len:
            x_values += [text[i+4 : i+4+text[i+4:].index(',')]]
        elif text[i-1] == '"' and text[i] == 'y' and i+4 < text_len and i+4+text[i+4:].index('\n') < text_len:
            y_values += [text[i+4 : i+4+text[i+4:].index('\n')]]

    x_y_pairs = []
    for i in np.arange(len(x_values)):
        x_y_pairs.append((float(x_values[i]), float(y_values[i])))

    path="path=color:0x0000ff|weight:5"
    for i in np.arange(len(x_y_pairs)):
        path += "|" + str(x_y_pairs[i][0]) + "," + str(x_y_pairs[i][1])

    print("https://maps.googleapis.com/maps/api/staticmap?size=800x800&zoom=15&" + path + "&key=" + API_KEY)

    urllib.request.urlretrieve("https://maps.googleapis.com/maps/api/staticmap?size=800x800&zoom=15&" + path + "&key=" + API_KEY, "map.jpg")
    nx.draw(G, with_labels=True, edge_color=list(nx.get_edge_attributes(G,'weight').values()), width=9.0, edge_cmap=plt.cm.Reds, font_size=9, labels=dict([[node,node] for node in list(G.nodes)]))
    plt.savefig('graph.jpg', bbox_inches='tight')
    image1 = Image.open("graph.jpg")
    image1.show()
    image2 = Image.open("map.jpg")
    image2.show()

create_map_and_graph(ML_output)