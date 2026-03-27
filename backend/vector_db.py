import os
import json
import chromadb
from chromadb.utils import embedding_functions

# Path to our mock data
DATA_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "articles.json")

# 1. & 2. Initialize ChromaDB to store embeddings (saves locally to 'chroma_data' folder)
CHROMA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chroma_data")
chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)

# Use Sentence Transformers to create the embeddings automatically
# The 'all-MiniLM-L6-v2' model is tiny, fast, and perfect for hackathons
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

# Get or create the vector collection
collection = chroma_client.get_or_create_collection(
    name="news_articles", 
    embedding_function=sentence_transformer_ef
)

# 3. Script / Function to load the sample articles into ChromaDB
def load_articles():
    with open(DATA_FILE_PATH, "r", encoding="utf-8") as f:
        articles = json.load(f)
        
    ids = []
    documents = []
    metadatas = []
    
    for article in articles:
        ids.append(article["id"])
        
        # We embed the title + content together so the AI has maximum context when searching
        text_to_embed = f"{article['title']}. {article['content']}"
        documents.append(text_to_embed)
        
        # Chroma requires metadata values to be strings or numbers. 
        # We join tags with a comma, which we can split back into a list later.
        metadatas.append({
            "title": article["title"],
            "source": article["source"],
            "date": article["date"],
            "tags": ", ".join(article["tags"])
        })
        
    # 'Upsert' saves the articles. If they already exist, it just updates them.
    collection.upsert(
        ids=ids,
        documents=documents,
        metadatas=metadatas
    )
    print(f"✅ Successfully loaded {len(ids)} articles into the Vector Database!")

# 4. & 5. Search function to find related articles and return formatted fields
def search_articles(query: str, limit: int = 3):
    results = collection.query(
        query_texts=[query],
        n_results=limit
    )
    
    formatted_results = []
    
    # Safety Check: if we got no results
    if not results["ids"] or len(results["ids"][0]) == 0:
        return formatted_results
        
    # Loop through the results (Chroma returns arrays of arrays)
    for i in range(len(results["ids"][0])):
        metadata = results["metadatas"][0][i]
        distance = results["distances"][0][i]
        
        # Calculate a rough 0.0 to 1.0 similarity score (Chroma uses L2 distance by default)
        similarity_score = round(1.0 - (distance / 2.0), 2)
        
        formatted_results.append({
            "title": metadata["title"],
            "source": metadata["source"],
            "date": metadata["date"],
            "tags": metadata["tags"].split(", "),
            "content": results["documents"][0][i],
            "similarity_score": similarity_score
        })
        
    return formatted_results

# Simple runner so you can test this script directly from the terminal!
if __name__ == "__main__":
    print("⏳ Loading articles into ChromaDB... ")
    print("(Note: It might take a few seconds to download the embedding model on the very first run)")
    load_articles()
    
    # Run a test query
    test_query = "What are the latest AI rules for finance?"
    print(f"\n🧠 Testing Search Query: '{test_query}'\n")
    
    results = search_articles(test_query, limit=2)
    print("🔍 Search Results:")
    print(json.dumps(results, indent=2))
