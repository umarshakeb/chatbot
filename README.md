# 🤖 RAG-Chatbot: Serverless Vector Search Meets Qwen3-32B

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![LangChain](https://img.shields.io/badge/LangChain-⚡-green)
![Pinecone](https://img.shields.io/badge/Pinecone-Serverless-brightgreen)
![Groq](https://img.shields.io/badge/Groq-Qwen3--32B-orange)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue)
![AWS](https://img.shields.io/badge/AWS-EC2%20%7C%20ECR-yellow)

An end-to-end, highly responsive Retrieval-Augmented Generation (RAG) conversational agent. This project bridges custom PDF document ingestion with real-time, low-latency LLM inference, completely containerized for cloud-native deployment.

## 🌟 Value Proposition
Built with scalability and clean architecture in mind, this application decouples the heavy lifting of document ingestion from the user-facing web server. By leveraging Groq's lightning-fast API and a serverless Pinecone vector database, the chatbot delivers instant, highly accurate, and context-aware responses grounded exclusively in your custom data.

---

## 🏗️ System Architecture

1. **The Ingestion Pipeline (`store_index.py` & `helper.py`):** 
   - Parses complex PDF documents and aggressively filters out bloat, retaining only essential metadata (Source & Page Number).
   - Chunks text dynamically and generates high-density vector embeddings using HuggingFace (`all-MiniLM-L6-v2`).
   - Upserts embeddings into a Serverless Pinecone index (AWS US-East-1).
2. **The Inference Server (`app.py`):**
   - A lightweight Flask web server that handles incoming queries.
   - Executes a similarity search (`k=3`) against the Pinecone index.
   - Orchestrates reasoning via the `Qwen/Qwen3-32b` model hosted on Groq, returning precise, context-backed answers to the front end.

---

## ⚡ Key Features

*   **Decoupled Workflows:** Ingestion and Inference are completely separated to prevent accidental index duplications and ensure the Flask server remains lightweight.
*   **Smart Metadata Filtering:** Strips default PDF loader bloat to preserve index space and enable strict source-tracking.
*   **Low-Latency Inference:** Achieves near-instantaneous reasoning speeds by routing the LLM workload through Groq.
*   **Cloud-Ready:** Fully containerized via Docker and optimized for deployment on AWS EC2 and ECR.

---

## 🛠️ Tech Stack

*   **Core Framework:** Python, Flask, LangChain
*   **Embeddings:** HuggingFace (`sentence-transformers/all-MiniLM-L6-v2`)
*   **Vector Database:** Pinecone (Serverless)
*   **LLM Inference:** Groq API (`qwen/qwen3-32b`)
*   **DevOps / Deployment:** Docker, AWS ECR, AWS EC2

---

## 🚀 Getting Started

### Prerequisites
*   Python 3.8+
*   Docker (if running containerized)
*   API Keys for **Pinecone** and **Groq**

### 1. Environment Setup
Clone the repository and create a `.env` file in the root directory:
```env
PINECONE_API_KEY=your_pinecone_api_key_here
GROQ_API_KEY=your_groq_api_key_here

**2. Install Dependencies**
pip install -r requirements.txt

**3. Ingest Your Data**
Place your PDF files into the /data directory. Then, initialize your vector database by running the ingestion script (Run this only once per dataset to avoid duplicate vectors):
python store_index.py

**4. Run the Chatbot Locally**
Start the Flask application:
python app.py

**
2. Install DependenciesGROQ_API_KEY=your_groq_api_key_here
