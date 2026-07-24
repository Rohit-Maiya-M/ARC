from app.services.vector_store_service import VectorStoreService
from app.services.retrieval_service import RetrievalService
from pymilvus import connections, utility, Index

def main():    
    connections.connect("default", host="127.0.0.1", port="19530")

    if utility.has_collection("ims_embeddings"):
        utility.drop_collection("ims_embeddings")
        print("Successfully dropped old collection 'ims_embeddings'.")

if __name__ == "__main__":
    main()
