import os
from dotenv import load_dotenv
import weaviate
from langchain_community.vectorstores import Weaviate
from langchain_community.embeddings import HuggingFaceEmbeddings

from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA

# Load environment variables
load_dotenv()

#  Connect to Weaviate v3
client = weaviate.Client(
    url=os.getenv("WEAVIATE_URL"),
    auth_client_secret=weaviate.auth.AuthApiKey(api_key=os.getenv("WEAVIATE_API_KEY")),
)

# Load embedding model
embedder = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

#  Load Vector Store (v3-style)
vectordb = Weaviate(
    client=client,
    index_name="IITGDATA",
    embedding=embedder,
    text_key="text",
    by_text=False  # We already passed custom embeddings during ingest
)

# Retriever using similarity search
retriever = vectordb.as_retriever(search_type="similarity", search_kwargs={"k": 3})

#  LLM via Groq (Mixtral)
llm = ChatOpenAI(
    openai_api_base="https://api.groq.com/openai/v1",
    openai_api_key=os.getenv("GROQ_API_KEY"),
    model="llama3-8b-8192", 
    temperature=0,
)

#  RetrievalQA chain
qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
qa_chain = qa  # used for exporting this to rag server

#  CLI chatbot loop  i'll keep this for testing but there i rag server for exposing api 
def main():
    print("Welcome to IITG Chatbot! Type 'exit' to quit.")
    while True:
        query = input("Enter your question: ").strip()
        if query.lower() in ("exit", "quit"):
            break
        print("Query received:", query)
        try:
            answer = qa.invoke({"query": query})
            print("Answer:", answer["result"])
        except Exception as e:
            print("❌ Error during query:", e)

if __name__ == "__main__":
    main()
