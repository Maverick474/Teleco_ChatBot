from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.responses import JSONResponse
from typing import Optional
import os
<<<<<<< HEAD
from agents import run_agent
from vectordb import VectorDBManager
=======
import tempfile
from agents import run_agent
from vectordb import VectorDBManager
from langchain_community.document_loaders import PyPDFLoader
>>>>>>> ae48cfe162e08e9fcabd0424cc067a0b79ecea20
import shutil

app = FastAPI(title="Teleco ChatBot API", description="API for Teleco document question answering")

# Initialize vector database manager
vector_manager = VectorDBManager()

@app.post("/upload_document/")
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a PDF document to the knowledge base
    """
    try:
        # Validate file type
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")
        
        # Create temporary directory if it doesn't exist
        os.makedirs("./teleco_db", exist_ok=True)
        
        # Save uploaded file temporarily
        temp_file_path = os.path.join("./teleco_db", file.filename)
        with open(temp_file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        
        # Process and add to vector database
        vector_manager.add_document(temp_file_path)
        
        return JSONResponse(
            status_code=200,
            content={"message": f"Document {file.filename} uploaded and processed successfully"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")

@app.post("/query/")
async def query_endpoint(query: str = Form(...)):
    """
    Query the RAG system with a text question
    """
    try:
        # Run the agent to get response
        result = run_agent(query)
        
        return JSONResponse(
            status_code=200,
            content={
                "response": result["response"],
                "agent_path": result["agent_path"],
                "language": result.get("language", "en")
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@app.get("/")
async def root():
    return {"message": "Teleco ChatBot API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

