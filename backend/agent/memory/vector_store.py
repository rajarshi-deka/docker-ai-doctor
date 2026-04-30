import faiss
import numpy as np
import json
import os
from .embedder import embed

INDEX_PATH = "memory_index.faiss"
STORE_PATH = "memory_store.json"

DIM = 384  # embedding size for MiniLM

# Load or create index
if os.path.exists(INDEX_PATH):
    index = faiss.read_index(INDEX_PATH)
else:
    index = faiss.IndexFlatL2(DIM)

# Load metadata
if os.path.exists(STORE_PATH):
    with open(STORE_PATH) as f:
        store = json.load(f)
else:
    store = []

def add_memory(entry):

    # Combine logs snippet and root cause for embedding

    text = entry["logs_snippet"] + " " + entry["root_cause"]
    print("DOCKER_AI_DOCTOR: Add Memory: Text:", text)

    vector = embed(text).astype("float32")
    print("DOCKER_AI_DOCTOR: Add Memory: Vector:", vector)
    index.add(np.array([vector]))

    store.append(entry)

    faiss.write_index(index, INDEX_PATH)

    with open(STORE_PATH, "w") as f:
        json.dump(store, f, indent=2)
        print("DOCKER_AI_DOCTOR: Add Memory: Success")

def search_memory(query, k=3):

    # Search Similar Memories Based on Logs and Root Cause for Contextual AI Diagnosis

    if len(store) == 0:
        return []

    vector = embed(query).astype("float32")
    print("DOCKER_AI_DOCTOR: Search Memory: Vector:", vector)

    D, I = index.search(np.array([vector]), k)

    results = []
    for idx in I[0]:
        if idx < len(store):
            results.append(store[idx])

    print("DOCKER_AI_DOCTOR: Search Memory: Results:", results)
    return results