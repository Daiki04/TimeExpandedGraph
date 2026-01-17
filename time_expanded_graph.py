"""
Time-Expanded Graph (TEG) for Grid Map
Creates a time-expanded graph from a grid map and visualizes it.
"""

import networkx as nx
import matplotlib.pyplot as plt


def create_time_expanded_graph(m, n, T):
    """
    Create a time-expanded graph for an m×n grid with T time steps.
    
    Parameters:
    -----------
    m : int
        Grid height (number of rows)
    n : int
        Grid width (number of columns)
    T : int
        Maximum time steps (0 to T)
    
    Returns:
    --------
    G : nx.DiGraph
        Directed graph representing the time-expanded graph
    """
    G = nx.DiGraph()
    
    # Create nodes: (x, y, t) for all positions and time steps
    for t in range(T + 1):
        for x in range(m):
            for y in range(n):
                G.add_node((x, y, t))
    
    # Create edges
    for t in range(T):
        for x in range(m):
            for y in range(n):
                current_node = (x, y, t)
                
                # Waiting edge: stay at the same position
                next_node_wait = (x, y, t + 1)
                G.add_edge(current_node, next_node_wait)
                
                # Movement edges: move to 4-neighbors (up, down, left, right)
                neighbors = [
                    (x - 1, y),  # up
                    (x + 1, y),  # down
                    (x, y - 1),  # left
                    (x, y + 1)   # right
                ]
                
                for nx_pos, ny_pos in neighbors:
                    # Check if the neighbor is within grid bounds
                    if 0 <= nx_pos < m and 0 <= ny_pos < n:
                        next_node_move = (nx_pos, ny_pos, t + 1)
                        G.add_edge(current_node, next_node_move)
    
    return G


def create_layout(G, m, n, T):
    """
    Create a layout for visualizing the time-expanded graph.
    X-axis: time (t)
    Y-axis: spatial position (flattened grid index)
    
    Parameters:
    -----------
    G : nx.DiGraph
        The time-expanded graph
    m : int
        Grid height
    n : int
        Grid width
    T : int
        Maximum time steps
    
    Returns:
    --------
    pos : dict
        Dictionary mapping nodes to (x, y) positions for visualization
    """
    pos = {}
    
    for node in G.nodes():
        x, y, t = node
        # Flatten the grid: position = x * n + y
        spatial_pos = x * n + y
        # X-axis: time, Y-axis: spatial position
        pos[node] = (t, spatial_pos)
    
    return pos


def visualize_time_expanded_graph(G, pos, m, n, T):
    """
    Visualize the time-expanded graph using matplotlib.
    
    Parameters:
    -----------
    G : nx.DiGraph
        The time-expanded graph
    pos : dict
        Node positions for visualization
    m : int
        Grid height
    n : int
        Grid width
    T : int
        Maximum time steps
    """
    plt.figure(figsize=(14, 10))
    
    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', 
                          node_size=300, alpha=0.9)
    
    # Draw edges
    nx.draw_networkx_edges(G, pos, edge_color='gray', 
                          arrows=True, arrowsize=10, 
                          alpha=0.5, arrowstyle='->')
    
    # Draw labels with (x, y, t) format
    labels = {node: f"({node[0]},{node[1]},{node[2]})" for node in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels, font_size=6)
    
    plt.xlabel('Time (t)', fontsize=12)
    plt.ylabel('Spatial Position (Grid Index)', fontsize=12)
    plt.title(f'Time-Expanded Graph for {m}×{n} Grid with T={T}', fontsize=14)
    plt.grid(True, alpha=0.3)
    
    # Set axis limits with some padding
    plt.xlim(-0.5, T + 0.5)
    plt.ylim(-0.5, m * n - 0.5)
    
    plt.tight_layout()
    plt.savefig('time_expanded_graph.png', dpi=300, bbox_inches='tight')
    print("Graph saved as 'time_expanded_graph.png'")
    plt.show()


def main():
    """
    Main function to create and visualize the time-expanded graph.
    """
    # Parameters
    m = 3  # Grid height
    n = 3  # Grid width
    T = 5  # Maximum time steps (0 to 5)
    
    print(f"Creating Time-Expanded Graph for {m}×{n} grid with T={T}...")
    
    # Create the time-expanded graph
    G = create_time_expanded_graph(m, n, T)
    
    print(f"Graph created with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")
    
    # Create layout
    pos = create_layout(G, m, n, T)
    
    # Visualize the graph
    print("Visualizing the graph...")
    visualize_time_expanded_graph(G, pos, m, n, T)
    
    print("Done!")


if __name__ == "__main__":
    main()
