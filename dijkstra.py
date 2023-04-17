# Import necessary libraries
import networkx as nx
import matplotlib.pyplot as plt
from time import sleep
from matplotlib.lines import Line2D
import heapq

# Define Dijkstra's algorithm
def dijkstra(graph, start):
    # Initialize shortest path distances and previous nodes dictionaries
    shortest_path_distances = {node: float('inf') for node in graph}
    previous_nodes = {node: None for node in graph}

    # Initialize unvisited nodes with the start node
    unvisited_nodes = [(0, start)]

    # Process unvisited nodes
    while unvisited_nodes:
        # Get the node with the smallest distance
        current_distance, current_node = heapq.heappop(unvisited_nodes)

        # Skip if the node's distance has been updated
        if current_distance > shortest_path_distances[current_node]:
            continue

        # Update distances of neighbor nodes
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight

            if distance < shortest_path_distances[neighbor]:
                shortest_path_distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(unvisited_nodes, (distance, neighbor))

    # Return shortest path distances and previous nodes
    return shortest_path_distances, previous_nodes

# Reconstruct shortest path from start node to end node
def reconstruct_path(previous_nodes, start_node, end_node):
    path = [end_node]
    while path[-1] != start_node:
        path.append(previous_nodes[path[-1]])
    return path[::-1]

# Animate the shortest path
def animate_path(graph, pos, start_node, end_node, previous_nodes, ax):
    path = reconstruct_path(previous_nodes, start_node, end_node)
    
    # Draw path on the graph
    for i in range(len(path) - 1):
        node1, node2 = path[i], path[i + 1]
        x_values = [pos[node1][0], pos[node2][0]]
        y_values = [pos[node1][1], pos[node2][1]]

        ax.plot(x_values, y_values, color="blue", linewidth=3, zorder=1)
        plt.draw()
        plt.pause(2)

    plt.gca().set_title(f"Shortest path from {start_node} to {end_node}: {path}")

# Handle click events on the graph
def onclick(event, graph, pos, start_node, previous_nodes):
    ax = plt.gca()
    # Hide existing lines
    for artist in ax.lines:
        artist.set_visible(False)
    plt.draw()

    # Find the closest node to the click
    closest_node = None
    closest_distance = float("inf")
    for node in pos:
        distance = ((pos[node][0] - event.xdata) ** 2 + (pos[node][1] - event.ydata) ** 2) ** 0.5
        if distance < closest_distance:
            closest_node = node
            closest_distance = distance

    # Animate path if the closest node is not the start node
    if closest_distance < 0.1 and closest_node != start_node:
        animate_path(graph, pos, start_node, closest_node, previous_nodes, ax)

def plot_graph(graph, shortest_path_distances, previous_nodes, start_node):
    G = nx.DiGraph()

    for node in graph:
        G.add_node(node)
        for neighbor, weight in graph[node].items():
            G.add_edge(node, neighbor, weight=weight)

    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(12, 8))

    nx.draw(G, pos, with_labels=True, node_size=2000, node_color="skyblue", edge_color="gray", linewidths=1,
            font_size=15, font_weight="bold", arrowsize=20)

    edge_labels = {(u, v): f"{d['weight']}" for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=12, font_weight="bold")

    for node, distance in shortest_path_distances.items():
        path = reconstruct_path(previous_nodes, start_node, node)
        plt.text(pos[node][0], pos[node][1] - 0.1, f"d={distance}\n{path}", horizontalalignment="center",
                 fontsize=10, fontweight="bold", zorder=2)

    cid = plt.gcf().canvas.mpl_connect('button_press_event', 
                                       lambda event: onclick(event, graph, pos, start_node, previous_nodes))
    plt.show()

if __name__ == "__main__":
    graph = {
        'A': {'B': 10, 'C': 5},
        'B': {'C': 2, 'D': 1},
        'C': {'B': 3, 'D': 9, 'E': 2},
        'D': {'E': 4},
        'E': {'D': 6, 'A': 7}
    }
    start_node = 'A'
    shortest_path_distances, previous_nodes = dijkstra(graph, start_node)
    plot_graph(graph, shortest_path_distances, previous_nodes, start_node)