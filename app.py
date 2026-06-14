from flask import Flask, request, jsonify, render_template
from src.helper import load_pdf_files, filter_to_minimal_docs, text_split, download_embedding
from langchain_pinecone import PineconeVectorStore
from langchain_groq import ChatGroq
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from src.prompt import *
import os


app = Flask(__name__)
load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

embeddings = download_embedding()

index_name = "chatbot-index"
docsearch = PineconeVectorStore.from_existing_index(
    embedding = embeddings,
    index_name = index_name
)

retriever = docsearch.as_retriever(search_type = "similarity", search_kwargs = {"k": 3})
chatModel =ChatGroq(
    model="qwen/qwen3-32b",
    temperature=0,
    max_tokens=None,
    reasoning_format="parsed",
    timeout=None,
    max_retries=2,
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}")
    ]
)

question_answer_chain = create_stuff_documents_chain(chatModel,prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

@app.route("/")
def index():
    return render_template("chat.html")

@app.route("/get", methods=["GET","POST"])
def chat():
    msg = request.form["msg"]
    input = msg
    print(input)
    response = rag_chain.invoke({"input": msg})
    print("Response: ", response["answer"])
    return str(response["answer"])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)