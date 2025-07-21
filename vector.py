## Imports

# allows embeddings to be created and stored in a vector store
from langchain_ollama import OllamaEmbeddings
# allows Chroma vector store to be created and queried
from langchain_chroma import Chroma
# allows text documents to be created with metadata
from langchain_core.documents import Document
# allows searching for file paths
import os
# allows reading CSV files
import pandas as pd

## load data and set up embeddings

# read in the csv and initialize the embeddings model as mxbai-embed-large
df = pd.read_csv("docs/realistic_restaurant_reviews.csv")
embeddings = OllamaEmbeddings(model="mxbai-embed-large")

## setup vector store path and check if it exists

# create the local folder where Chroma will persist its vector database
db_location = "./chrome_langchain_db"

## create a Chroma vector store using the documents and embeddings

vector_store = Chroma( # create a Chroma vector store instance (load existing or create new)
    collection_name="restaurant_reviews", # name of the collection (like a table name in a database)
    persist_directory=db_location, # filesystem path where the vector DB is saved or loaded from
    embedding_function=embeddings # function that converts text into vector embeddings (mxbai-embed-large in this case)
)

# check if the database already exists, if not, this will be set to True
#add_documents = not os.path.exists(db_location)
add_documents = True

## convert CSV Rows into LangChain Documents (only if DB is new)

# if database does not exist, create empty lists to store documents and ids
if add_documents:
    documents = []
    ids = []
    
    # iterate over each row of the CSV and create a document object with title + review, metadata, and id
    for i, row in df.iterrows():
        document = Document(
            page_content=row["Title"] + " " + row["Review"],
            metadata={"rating": row["Rating"], "date": row["Date"]},
            id=str(i)
        )
        # append the id and document to their lists
        ids.append(str(i))
        documents.append(document)

# if this is the first run (no existing DB), add all the documents and their embeddings
if add_documents:
    vector_store.add_documents(documents=documents, ids=ids)

# convert the vector store into a retriever object
# this allows to search for documents by meaningful similarity
# the search will return the top k most similar documents
retriever = vector_store.as_retriever(
    search_kwargs={"k": 5}
)

## check results

# get all documents from the vector store
data = vector_store.get()

# print a sample of the document, metadata, and id
# print("Example content:\n", data['documents'][0])
# print("Metadata:\n", data['metadatas'][0])
# print("IDs:\n", data['ids'][0])