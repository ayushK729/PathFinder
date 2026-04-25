import osmnx as ox

def get_nearest_node(G, x, y):
    """
    Convert lat/lon → nearest road node
    """
    return ox.distance.nearest_nodes(G, x, y)