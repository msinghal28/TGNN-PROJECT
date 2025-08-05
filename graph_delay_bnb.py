# -*- coding: utf-8 -*-
"""
File: graph_delay_bnb.py
Description: Visualizes blockchain transactions as a directed graph,
             updating dynamically in batches using matplotlib animation.
"""

import json
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time # Still useful for a controlled delay if desired, though FuncAnimation handles timing

# --- Configuration ---
TRANSACTIONS_FILE = "bnb_transactions.json" # Ensure this file exists and contains your transaction data
BATCH_SIZE = 50 # Number of transactions to process in each update step
ANIMATION_INTERVAL_MS = 1000 # Interval between updates in milliseconds (e.g., 1000ms = 1 second)

# --- Load Transaction Data ---
try:
    with open(TRANSACTIONS_FILE, "r") as f:
        transactions = json.load(f)
except FileNotFoundError:
    print(f"Error: {TRANSACTIONS_FILE} not found.")
    print("Please ensure 'bnb_transactions.json' is in the same directory.")
    print("Creating a dummy file for demonstration.")
    # Create a dummy bnb_transactions.json for demonstration if not found
    dummy_transactions = []
    for i in range(500): # 500 dummy transactions
        sender_prefix = f"0xSender{np.random.randint(0, 50):02d}" # Simulate limited unique senders
        receiver_prefix = f"0xReceiver{np.random.randint(0, 50):02d}" # Simulate limited unique receivers
        dummy_transactions.append({
            "Sender Address": f"{sender_prefix}{i % 100:02d}",
            "Receiver Address": f"{receiver_prefix}{(i + 5) % 100:02d}" # Simple connection logic
        })
    with open(TRANSACTIONS_FILE, "w") as f:
        json.dump(dummy_transactions, f, indent=4)
    transactions = dummy_transactions
    print(f"Dummy '{TRANSACTIONS_FILE}' created with {len(dummy_transactions)} transactions.")

# --- Graph Initialization ---
G = nx.DiGraph() # Create a directed graph

# Initialize plot
fig, ax = plt.subplots(figsize=(12, 8))
# Set the title, which will be updated dynamically
current_batch_idx = 0
total_batches = (len(transactions) + BATCH_SIZE - 1) // BATCH_SIZE # Ceiling division
ax.set_title(f"Blockchain Graph - Batch {current_batch_idx}/{total_batches}")


# --- Animation Update Function ---
def update(frame):
    """
    This function is called by FuncAnimation for each frame to update the graph.
    'frame' is the current frame number, which we use as the batch index.
    """
    global current_batch_idx # Access the global batch index counter

    start_idx = current_batch_idx * BATCH_SIZE
    end_idx = start_idx + BATCH_SIZE
    batch = transactions[start_idx:end_idx]

    if not batch:
        # If there are no more transactions, stop the animation (optional)
        print("No more transactions to process. Animation stopping.")
        ani.event_source.stop() # Stop the animation source
        return

    # Add edges from the current batch
    new_nodes_added = False
    for tx in batch:
        sender = tx.get("Sender Address")
        receiver = tx.get("Receiver Address")
        if sender and receiver:
            # Check if adding new nodes, so layout can be recomputed if needed
            if sender not in G:
                new_nodes_added = True
            if receiver not in G:
                new_nodes_added = True
            G.add_edge(sender, receiver)

    # Clear the previous plot content
    ax.clear()

    # Update title
    current_batch_idx += 1
    ax.set_title(f"Blockchain Graph - Batch {current_batch_idx}/{total_batches} ({len(G.nodes())} nodes, {len(G.edges())} edges)")

    # Calculate positions for the nodes
    # Re-calculate layout for new nodes to appear in a sensible position.
    # For very large graphs, this can be computationally expensive.
    # In such cases, consider incremental layout updates or pre-calculating for all known nodes.
    pos = nx.spring_layout(G, k=0.15, iterations=20, seed=42) # k adjusts optimal distance, iterations for stability

    # Draw nodes and edges
    nx.draw_networkx_nodes(G, pos, ax=ax, node_size=500, node_color='skyblue', alpha=0.9, linewidths=1.0, edgecolors='gray')
    nx.draw_networkx_edges(G, pos, ax=ax, arrows=True, arrowsize=10, alpha=0.7, edge_color='gray')
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=6, font_color='black')

    # Adjust plot limits and turn off axis
    ax.set_xlim([min(p[0] for p in pos.values()) - 0.1, max(p[0] for p in pos.values()) + 0.1])
    ax.set_ylim([min(p[1] for p in pos.values()) - 0.1, max(p[1] for p in pos.values()) + 0.1])
    ax.axis('off')

    # Optional: If you want a small pause between updates managed by this function, uncomment:
    # time.sleep(0.1) # Shorter pause than the animation interval

# --- Create and Run Animation ---
# `frames` specifies the number of frames (batches) to animate.
# `repeat=False` ensures the animation runs only once through all batches.
ani = animation.FuncAnimation(
    fig,
    update,
    frames=total_batches, # Number of batches to process
    interval=ANIMATION_INTERVAL_MS,
    repeat=False, # Do not repeat the animation after all batches are processed
    blit=False # Set to True for performance, but can cause issues with complex plots
)

plt.tight_layout() # Adjust layout to prevent labels from overlapping
plt.show() # Display the animation window
