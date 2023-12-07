import matplotlib.pyplot as plt
import networkx as nx
from collections import Counter

def sorted_routes_count(routes = None):

    sample_routes = [
        ("sensor1", "sensor2"),
        ("sensor2", "sensor1"),
        ("sensor1", "sensor6"),
        ("sensor1", "sensor6"),
        ("sensor6", "sensor5"),
        ("sensor5", "sensor6"),
        ("sensor6", "sensor5"),
        ("sensor5", "sensor2"),
        ("sensor5", "sensor3"),
        ("sensor5", "sensor4"),
        ("sensor5", "sensor4"),
        ("sensor4", "sensor3"),
        ("sensor3", "sensor2"),
        ("sensor3", "sensor2"),
        ("sensor3", "sensor2")
    ]

    if routes == None:
        routes = sample_routes

    sorted_routes_count = Counter([tuple(sorted(pair)) for pair in routes])

    # Print the counts of each route pair
    for pair, count in sorted_routes_count.items():
        print(f"{pair}: {count}")

    sorted_routes = [tuple(sorted(route)) for route in routes]

    route_frequency = {}
    for route in sorted_routes:
        route_frequency[route] = route_frequency.get(route, 0) + 1

    G = nx.Graph()

    # Define sensors positions
    node_positions = {
        "sensor1": (0, 2),
        "sensor2": (2, 2),
        "sensor3": (3, 1),
        "sensor4": (2, -1),
        "sensor5": (1.5, 0.5),
        "sensor6": (0, 1),
    }

    # Add sensors with positions
    for node, pos in node_positions.items():
        G.add_node(node, pos=pos)

    #Calculate edges
    for route in sorted_routes:
        G.add_edge(route[0], route[1])

    # Draw sensors
    pos = nx.get_node_attributes(G, 'pos')
    nx.draw(G, pos, with_labels=True, node_size=200, node_color='skyblue')

    # Draw edges
    for edge in G.edges():
        frequency = route_frequency.get(edge, 0)
        nx.draw_networkx_edges(G, pos, edgelist=[edge], width=frequency*2)

    # Display the plot
    plt.axis("off")
    plt.show()

# sorted_routes_count()
