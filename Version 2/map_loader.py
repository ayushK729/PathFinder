import osmnx as ox

def load_map(place):
    G = ox.graph_from_place(place, network_type="drive")
    return G