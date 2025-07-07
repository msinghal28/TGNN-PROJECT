import json
import networkx as nx
import os
import time

# ---------- SETTINGS ----------
INPUT_JSON = "bnb_transactions.json"
OUTPUT_FOLDER = "graph_batches"
BATCH_SIZE = 50
PAUSE_SECONDS = 5

# ---------- SETUP ----------
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Load JSON list of transactions
with open(INPUT_JSON, "r") as f:
    transactions = json.load(f)

# Create directed graph
G = nx.DiGraph()

# ---------- PROCESS IN BATCHES ----------
for i in range(0, len(transactions), BATCH_SIZE):
    batch = transactions[i:i + BATCH_SIZE]

    for tx in batch:
        sender = tx.get("Sender Address")
        receiver = tx.get("Receiver Address")
        if sender and receiver:
            G.add_edge(sender, receiver)

    # Save current batch graph
    batch_id = i // BATCH_SIZE + 1
    base_path = os.path.join(OUTPUT_FOLDER, f"graph_batch_{batch_id}")

    # Export in various formats
    nx.write_graphml(G, f"{base_path}.graphml")
    nx.write_gml(G, f"{base_path}.gml")
    nx.write_adjlist(G, f"{base_path}.adjlist")

    print(f"Saved graph batch {batch_id} with {len(G.nodes())} nodes and {len(G.edges())} edges.")

    time.sleep(PAUSE_SECONDS)
