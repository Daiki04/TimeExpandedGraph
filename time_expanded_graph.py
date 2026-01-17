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


def visualize_time_expanded_graph_3d(G, m, n, T):
    """
    Visualize the time-expanded graph in 3D using matplotlib.
    X-axis: x coordinate
    Y-axis: y coordinate
    Z-axis: time (t)
    
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
    """
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # Prepare node positions and colors
    node_positions = []
    node_colors = []
    
    for node in G.nodes():
        x, y, t = node
        node_positions.append([x, y, t])
        # Color nodes by time step (handle T=0 case)
        node_colors.append(t / T if T > 0 else 0)
    
    # Draw nodes
    node_positions = list(zip(*node_positions))
    ax.scatter(node_positions[0], node_positions[1], node_positions[2],
              c=node_colors, cmap='viridis', s=100, alpha=0.8, 
              edgecolors='black', linewidths=0.5)
    
    # Draw edges
    for edge in G.edges():
        x1, y1, t1 = edge[0]
        x2, y2, t2 = edge[1]
        
        # Distinguish between waiting edges and movement edges
        if x1 == x2 and y1 == y2:
            # Waiting edge (vertical line in time)
            ax.plot([x1, x2], [y1, y2], [t1, t2], 
                   'b-', alpha=0.3, linewidth=1)
        else:
            # Movement edge
            ax.plot([x1, x2], [y1, y2], [t1, t2], 
                   'r-', alpha=0.3, linewidth=0.8)
    
    # Set labels and title
    ax.set_xlabel('X Coordinate', fontsize=11)
    ax.set_ylabel('Y Coordinate', fontsize=11)
    ax.set_zlabel('Time (t)', fontsize=11)
    ax.set_title(f'3D Time-Expanded Graph for {m}×{n} Grid with T={T}', 
                fontsize=13, pad=20)
    
    # Set axis limits
    ax.set_xlim(-0.5, n - 0.5)
    ax.set_ylim(-0.5, m - 0.5)
    ax.set_zlim(-0.5, T + 0.5)
    
    # Add grid
    ax.grid(True, alpha=0.3)
    
    # Add colorbar
    sm = plt.cm.ScalarMappable(cmap='viridis', 
                               norm=plt.Normalize(vmin=0, vmax=T))
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax, pad=0.1, shrink=0.8)
    cbar.set_label('Time Step', fontsize=10)
    
    # Adjust viewing angle
    ax.view_init(elev=20, azim=45)
    
    plt.tight_layout()
    plt.savefig('time_expanded_graph_3d.png', dpi=300, bbox_inches='tight')
    print("3D Graph saved as 'time_expanded_graph_3d.png'")
    plt.show()


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
    
    # Create layout for 2D visualization
    pos = create_layout(G, m, n, T)
    
    # Visualize the graph in 2D
    print("Visualizing the graph in 2D...")
    visualize_time_expanded_graph(G, pos, m, n, T)
    
    # Visualize the graph in 3D
    print("Visualizing the graph in 3D...")
    visualize_time_expanded_graph_3d(G, m, n, T)
    
    print("Done!")


if __name__ == "__main__":
    main()
