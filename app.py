import os
import tempfile
from typing import List
from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

from dotenv import load_dotenv

load_dotenv()


app = FastAPI()
OPENAI_API_KEY= os.environ.get('OPENAI_API_KEY')
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

uploaded_docs = []

@app.post("/upload-multiple")
async def upload_multiple(files: List[UploadFile] = File(...)):
    """
    Endpoint to upload multiple PDF files, extract their text, split into chunks,
    and add them to the global knowledge base.
    """
    total_chunks = 0
    for file in files:
        if file.content_type != "application/pdf":
            return JSONResponse(
                {"error": f"Only PDF files are allowed. {file.filename} is not allowed."},
                status_code=400
            )
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                contents = await file.read()
                tmp.write(contents)
                tmp.flush()
                tmp_file_path = tmp.name

            loader = PyPDFLoader(tmp_file_path)
            documents = loader.load()

            text_splitter = CharacterTextSplitter(separator="\n", chunk_size=1000, chunk_overlap=200)
            for doc in documents:
                splits = text_splitter.split_text(doc.page_content)
                for chunk in splits:
                    uploaded_docs.append(doc.__class__(page_content=chunk, metadata=doc.metadata))
                    total_chunks += 1

            os.remove(tmp_file_path)
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)

    return {"message": f"Uploaded and processed {total_chunks} document chunks from {len(files)} files."}


@app.post("/chat")
async def chat(question: str = Form(...)):
    """
    Endpoint to handle chat queries.
    """
    if not uploaded_docs:
        return JSONResponse({"error": "No documents uploaded yet."}, status_code=400)
    
    try:
        # Build a FAISS vector store from the uploaded documents
        embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)
        vectorstore = FAISS.from_documents(uploaded_docs, embeddings)
        
        # Create a QA chain using the vector store as the retriever
        llm = OpenAI(temperature=0,api_key=OPENAI_API_KEY)
        qa = RetrievalQA.from_chain_type(
            llm=llm, 
            chain_type="stuff",  
            retriever=vectorstore.as_retriever()
        )
        
        answer = qa.run(question)
        return {"question": question, "answer": answer}
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """
    Serve the UI – a simple HTML page with a form for PDF upload and a chat interface.
    """
    return templates.TemplateResponse("index.html", {"request": request})