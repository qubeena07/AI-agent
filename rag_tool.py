from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.tools.retriever import create_retriever_tool
import os

def get_rag_tool(pdf_path: str = "knowledge.pdf"):
    if not os.path.exists(pdf_path):
        return None
    embeddings = GoogleGenerativeAIEmbeddings(model="embed-gecko-001")
    loader = PyPDFLoader(pdf_path)
    pages = loader.load_and_split()
    vectorstore = FAISS.from_documents(pages, embeddings)
    retriever = vectorstore.as_retriever()
    rag_tool = create_retriever_tool(
        retriever=retriever,
        name="RAG_Knowledge_Base",
        description="Useful for answering questions about the content in the provided PDF document. Use this tool when the user query relates to information contained within the document.",
    )
    return rag_tool
