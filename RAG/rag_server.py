import os
from dotenv import load_dotenv
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from response import qa_chain  # assuming your qa_chain is in response.py

load_dotenv()  # Load .env from project root

app = FastAPI()

class QueryRequest(BaseModel):
    query: str

@app.post("/api/chatbot")
async def chatbot_endpoint(request: QueryRequest):
    try:
        result = qa_chain.invoke({"query": request.query})
        return {"answer": result["result"]}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    port = int(os.getenv("PORT1", 5151))  # fallback to 5151 if PORT1 is not set
    uvicorn.run("rag_server:app", host="0.0.0.0", port=port, reload=True)
