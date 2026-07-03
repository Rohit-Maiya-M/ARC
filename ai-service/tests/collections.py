from pymilvus import MilvusClient

client = MilvusClient(uri="http://localhost:19530")

print("Collections:", client.list_collections())

print("Schema:", client.describe_collection("ims_embeddings"))

print("Stats:", client.get_collection_stats("ims_embeddings"))

results = client.query(
    collection_name="ims_embeddings",
    output_fields=["chunk_id", "repository_id", "content", "filename"],
    limit=20
)

for r in results:
    print(r)
