# ingest_pdfs.py
import getpass
import os
import glob
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import streamlit as st
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
#from langchain_openai import OpenAIEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Provide your Google API key here")

def ingest_pdfs(pdf_directory: str, persist_directory: str):
    # Get all PDF file paths in the specified directory
    pdf_files = glob.glob(os.path.join(pdf_directory, "*.pdf"))
    documents = []
    
    # Load documents from each PDF file
    for pdf_file in pdf_files:
        print(f"Loading: {pdf_file}")
        loader = PyPDFLoader(pdf_file)
        docs = loader.load()
        documents.extend(docs)
    
    print(f"Total documents loaded: {len(documents)}")
  
    # Split documents into smaller chunks with overlap for improved retrieval
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=500)
    docs = text_splitter.split_documents(documents)
    print(f"Documents split into {len(docs)} chunks.")

   

    embeddings = GoogleGenerativeAIEmbeddings(google_api_key=gemini_api_key,model="models/text-embedding-004")
    
    # Build the FAISS vector store from the document chunks
    vector_store = Chroma.from_documents(documents=docs, 
                                           embedding=embeddings, 
                                           persist_directory=persist_directory)
    
    # Save the vector store locally so that ingestion happens only once
    


if __name__ == "__main__":
    pdf_directory = ""  # Update this path to your PDFs folder
    vector_db_path = ""           # Location to store the vector database
    ingest_pdfs(pdf_directory, vector_db_path)
