from pymilvus import connections, utility, Collection

def drop_old_collection(collection_name: str = "ims_embeddings"):
    
    print("Connecting to Milvus...")
    connections.connect("default", host="127.0.0.1", port="19530")
    
    if utility.has_collection(collection_name):
        print(f"Collection '{collection_name}' found. Dropping it now...")
                
        collection = Collection(collection_name)
        collection.drop()
        
        print(f"✅ Successfully dropped collection: '{collection_name}'")
    else:
        print(f"ℹ️ Collection '{collection_name}' does not exist. Nothing to drop.")

if __name__ == "__main__":
    drop_old_collection()