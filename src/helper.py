# from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List
from langchain.schema import Document
# from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings

# Load PDF documents from the "data" directory
def load_pdf_files(directory):
    loader = DirectoryLoader(
        directory,
        glob = "*.pdf",
        loader_cls = PyPDFLoader
    )

    documents = loader.load()
    return documents



def filter_to_minimal_docs(docs):
    minimal_docs = []
    for doc in docs:
        src = doc.metadata.get("source")
        page_num = doc.metadata.get("page")
        minimal_docs.append(
            Document(
                page_content = doc.page_content,
                metadata = {"source": src, "page": page_num}
            )
        )
    return minimal_docs


# Chunking the documents into smaller pieces for better processing
def text_split(minimal_docs):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=200,
        length_function=len
    )
    texts_chunk = text_splitter.split_documents(minimal_docs)
    return texts_chunk


def download_embedding():
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    embeddings = HuggingFaceEmbeddings(model_name=model_name)
    return embeddings

embeddings = download_embedding()