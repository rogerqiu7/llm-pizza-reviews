# import the OllamaLLM wrapper, which allows LangChain to use local LLMs through the Ollama runtime
from langchain_ollama.llms import OllamaLLM
# ChatPromptTemplate helps create a structured, fill-in-the-blank style prompt for the model
from langchain_core.prompts import ChatPromptTemplate
# import the retriever object you previously set up in vector.py (uses Chroma to return relevant reviews)
from vector import retriever

# create an instance of the local LLM using the "llama3.2" model via Ollamo
model = OllamaLLM(model="llama3.2")

# a multi-line prompt that defines the assistant's behavior and inserts user and context inputs
template = """
    You are an expert in answering questions about a pizza restaurant

    Here are some relevant reviews: {reviews}

    Here is the question to answer: {question}
"""

# create a structured prompt from the template
prompt = ChatPromptTemplate.from_template(template)
# combine the prompt and the model into a single pipeline using the "|" operator
chain = prompt | model

# while loop to continuously ask the user for questions until the user types "q" to quit
while True:
    print("\n\n-------------------------------")
    question = input("Ask your question (q to quit): ")
    print("\n\n")
    if question == "q":
        break
    
    # use the retriever to get the top 5 semantically relevant reviews from the Chroma DB
    reviews = retriever.invoke(question)
    
    # pass the reviews and the question into the chain and get the model's response
    result = chain.invoke({"reviews": reviews, "question": question})
    # print the response from the LLM
    print(result)