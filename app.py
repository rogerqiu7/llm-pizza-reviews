# import os and logging for environment setup and logging
import os
import logging
# import url and model from the config file
from config import OLLAMA_BASE_URL, MODEL_NAME
# import the OllamaLLM wrapper, which allows LangChain to use local LLMs through the Ollama runtime
from langchain_ollama.llms import OllamaLLM
# ChatPromptTemplate helps create a structured, fill-in-the-blank style prompt for the model
from langchain_core.prompts import ChatPromptTemplate
# import the retriever object you previously set up in vector.py (uses Chroma to return relevant reviews)
from vector_store import retriever

# set up logging to print INFO level messages to the console
# this will help you see what the app is doing as it runs
logging.basicConfig(level=logging.INFO)

# set the base URL so the app can talk to the Ollama server running inside the same Docker container
# since both the app and Ollama are in the same container, 'localhost' correctly refers to the internal Ollama server  
os.environ["OLLAMA_BASE_URL"] = OLLAMA_BASE_URL

# create an instance of the local LLM using the model defined in the config file
model = OllamaLLM(model=MODEL_NAME, temperature=0.2, top_p=0.95)
# temperature: 0.0 to 0.3 → prioritize accuracy and reduce randomness
# top_p: 0.8 to 0.95 → limit token choices while maintaining some flexibility

# a multi-line prompt that defines the assistant's behavior and inserts user and context inputs
template = """
    You are an expert in answering questions about a pizza restaurant

    Here is the question to answer: {question}

    Here are some relevant reviews: {reviews}
"""

# create a structured prompt from the template
prompt = ChatPromptTemplate.from_template(template)
# combine the prompt and the model into a single pipeline using the "|" operator
chain = prompt | model

# while loop to continuously ask the user for questions until the user types "q" to quit
# only run this part if the script is executed directly (not imported)
if __name__ == "__main__":
    while True:
        print("\n\n-------------------------------")
        question = input("Ask your question (q to quit): ")
        print("\n\n")
        if question == "q":
            break
        
        # use the retriever to get the top 5 semantically relevant reviews from the Chroma DB
        reviews = retriever.invoke(question)
        
        # pass the reviews and the question into the chain and get the model's response
        result = chain.invoke({"question": question, "reviews": reviews})

        # print the response from the LLM
        print(result)

# open the log file in append mode (creates it if it doesn't exist)
with open("rag_log.txt", "a") as f:

    # log the original user question
    f.write(f"QUESTION: {question}\n")

    # log the header for the retrieved documents
    f.write("RETRIEVED:\n")

    # write the first 200 characters of each retrieved document to the log
    for doc in reviews:
        f.write(f"- {doc.page_content[:200]}...\n")

    # log the generated answer
    f.write(f"ANSWER: {result}\n\n")