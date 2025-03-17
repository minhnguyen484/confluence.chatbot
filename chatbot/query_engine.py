from dotenv import load_dotenv
import os
import tiktoken
from PyPDF2 import PdfReader

from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.callbacks import get_openai_callback
from langchain_core.documents import Document

load_dotenv(override=True)

def read_pdf(file_path):
    with open(file_path, "rb") as file:
        pdf_reader = PdfReader(file)
        text = ""
        for page_num in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page_num].extract_text()
    return text

def read_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()
    return text

def read_documents_from_directory(directory):    
    file_path = os.path.join(directory, "confluence-devops-contents.txt")
    combined_text = ""
    combined_text += read_txt(file_path)
            
    return combined_text

def split_text_into_token_chunks(text, max_tokens=800, overlap_tokens=100):
    enc = tiktoken.encoding_for_model("gpt-3.5")  # Adjust for your model
    tokens = enc.encode(text)

    chunks = []
    start = 0
    while start < len(tokens):
        end = min(start + max_tokens, len(tokens))
        chunk = enc.decode(tokens[start:end])
        chunks.append(chunk)
        start += max_tokens - overlap_tokens  # Overlap ensures continuity
    
    return chunks

def get_relevant_chunk(vectorstore, query):
    results = vectorstore.similarity_search(query, k=3)  # Get top 3 relevant chunks
    return " ".join([res.page_content for res in results])

def get_context_docs(query):

    data_dir = os.path.abspath("chatbot\\data")
    text = read_documents_from_directory(data_dir)

    # Step 1: Convert text chunks into embeddings
    chunks = split_text_into_token_chunks(text)
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(chunks, embeddings)

    # Step 2: Retrieve the most relevant chunk for a given query
    context = get_relevant_chunk(vectorstore, query)
    context_docs = [Document(page_content=context)]  # Convert to Document format

    return context_docs
