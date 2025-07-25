# LLM-Pizza-Reviews
A lightweight, containerized RAG (Retrieval-Augmented Generation) app that uses a local LLM and vector database to answer natural language questions about pizza restaurant reviews.

This project demonstrates how to build a local LLM-powered Q&A system using:

- **Ollama** to run models like LLaMA 3.2 locally
- **LangChain** to structure prompts and manage model input/output
- **Chroma** as a vector database for semantic retrieval
- **Docker** for portable, reproducible setup

---


## Project Structure

```
project/
├── app.py               # Main app: prompts user and returns answers
├── vector_store.py      # Loads reviews and builds semantic index
├── config.py            # Ollama base URL, model names, DB path
├── entrypoint.sh        # Starts Ollama and launches the app
├── Dockerfile           # Container definition
├── requirements.txt     # Python dependencies
├── .dockerignore        # Ignore DB logs and cache files
├── data/
│   └── realistic_restaurant_reviews.csv
├── chrome_langchain_db/ # Vector DB (created at runtime)
└── rag_log.txt          # Conversation log (created at runtime)
```

## How the app works

<img src="pics/chroma.png" alt="alt text" width="50%" height="auto">

1. **Data Ingestion (`vector.py`)**
   - Loads realistic restaurant reviews from a CSV file.
   - Each review is turned into a `Document` with text content, metadata (e.g., rating, date), and a unique ID.
   - Each document is embedded into a vector using `mxbai-embed-large` via Ollama.
   - The documents and embeddings are stored in a local Chroma vector database.

2. **Querying (`main.py`)**
   - The user enters a question (e.g., *"What do people think about the crust?"*).
   - The system retrieves the top 5 semantically similar reviews from Chroma.
   - The question and relevant reviews are sent to LLaMA 3 via LangChain.
   - Parameters of the model can be adjusted like like `temperature` and `top_p` to control diversity and randomness of answers.
   - The model answers using context from the actual reviews.

---

## To run the app:
**1. Build the container:**
```bash
docker build -t pizza-ai .
```

**2. Run the container interactively:**
```bash
docker run --rm -it pizza-ai
```
---
## What Happens When You Run It

1. **The container starts and runs `/app/entrypoint.sh`:**
   - Launches the Ollama server in the background on port `11434`
   - Waits for Ollama to become ready (via HTTP check)
   - Pulls the LLM model and embedding model if not already cached
   - Starts the app (`python app.py`)

2. **Your app sends requests to Ollama inside the same container:**
   - Ollama listens on `localhost:11434`
   - Your Python code sends embed and generate requests via that port
   - No external network connection is needed — everything is self-contained

---

## What is a Vector Database?

Instead of storing data as rows and columns, a vector DB stores **semantic representations** of text — i.e. numeric vectors.

Example:
| Review Text                         | Vector (simplified)         |
|------------------------------------|-----------------------------|
| “Crust was crispy and delicious.”  | `[0.11, -0.03, 0.82, ...]`  |

When you ask a question like “How’s the crust?”, your query is converted into a vector and compared to all reviews using vector similarity.
---

## Examples: 

### Retrieving values from the vector DB:
![alt text](pics/document-sample.png)

### Running the Docker image:
![alt text](pics/startup.png)

### Example of question and answer:
![alt text](pics/example.png)