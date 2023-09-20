import networkx as nx
import matplotlib.pyplot as plt

# Create an empty graph
G = nx.DiGraph()

# Define the entities
G.add_node("User")
G.add_node("Email")
G.add_node("Attachment")

# Define the relationships
G.add_edge("User", "Email", label="Send")
G.add_edge("User", "Email", label="Read")
G.add_edge("User", "Email", label="Expand")
G.add_edge("User", "Email", label="Logout")
G.add_edge("Email", "Attachment")

# Position the nodes
pos = nx.spring_layout(G)

# Draw the entities and relationships
nx.draw_networkx_nodes(G, pos, node_size=2000, node_color="lightblue")
nx.draw_networkx_labels(G, pos, font_size=12, font_weight="bold")
nx.draw_networkx_edges(G, pos, edge_color="gray", width=2, arrowsize=20)
nx.draw_networkx_edge_labels(G, pos, font_size=10)

# Display the diagram
plt.axis("off")
plt.show()
