from langchain_community.document_loaders import PyMuPDFLoader, PlaywrightURLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Weaviate

import weaviate
import os
from dotenv import load_dotenv

# Set custom USER_AGENT 
os.environ["USER_AGENT"] = "iitg-chatbot/1.0"


load_dotenv()

#  Load documents

pdfs = ["../docs/Acad_Calendar_2025.pdf", "../docs/BAJHLIP23020V012223.pdf","../docs/CHOTGDP23004V012223.pdf","../docs/EDLHLGA23009V012223.pdf","../docs/HDFHLIP23024V072223.pdf","../docs/ICIHLIP22012V012223.pdf"]

pdf_docs = []
for pdf in pdfs:
    pdf_docs.extend(PyMuPDFLoader(pdf).load())  

# Web pages to ingest
webs = [
    "https://iitg.ac.in/acad/offered_courses.php",
    "https://iitg.ac.in/acad/academic_calendar.php"
]

web_docs = []
for url in webs:
    web_docs.extend(PlaywrightURLLoader([url]).load())  # wrap URL in a list

# Combine docs
all_docs = pdf_docs + web_docs

print(" Combine success")

#  Split documents
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(all_docs)
print("Splitting success")

#  Create embeddings 
embedder = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
print("Embedding success")

#  Connect to Weaviate v3
client = weaviate.Client(
    url=os.getenv("WEAVIATE_URL"),
    auth_client_secret=weaviate.auth.AuthApiKey(api_key=os.getenv("WEAVIATE_API_KEY")),
)
print(" Client connection success")

# Step 5: Ensure class/schema exists 
if "IITGDATA" not in [c["class"] for c in client.schema.get()["classes"]]:
    client.schema.create_class({
        "class": "IITGDATA",
        "vectorizer": "none",  # because we're passing our own embeddings
        "properties": [
            {"name": "text", "dataType": ["text"]},
        ],
    })
    print("Schema 'IITGDATA' created")

#  Store into Weaviate vector DB 
vectordb = Weaviate.from_documents(
    documents=chunks,
    embedding=embedder,
    client=client,
    index_name="IITGDATA",
    text_key="text",
    by_text=False
)

print(" Ingestion was successful!")
