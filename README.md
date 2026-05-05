DeepSeek FastAPI Backend – Multi-LLM RAG System
Live Demo

https://youtu.be/V3Oh6Wpr4sU

This demo showcases:

Uploading documents
Processing & embedding
Asking questions
Receiving context-aware answers using RAG
Overview

This project is a production-ready backend service built with FastAPI for intelligent document understanding using Retrieval-Augmented Generation (RAG).

It enables users to upload documents and interact with them using natural language queries powered by Large Language Models (LLMs).

Originally developed as Jupyter notebooks, the system has been fully refactored into a clean, modular, and deployable backend architecture.

System Architecture

This system follows a decoupled LLM design, separating:

Model (Reasoning Layer) → what generates the answer
Inference Engine (Execution Layer) → how the model runs
Models (Reasoning Layer)
DeepSeek
High-quality reasoning
Used for:
Question Answering
Summarization
Question Generation (MCQs + Essay)
LLaMA (via Groq)
Optimized for fast conversational responses
Inference Engines (Execution Layer)
Local Inference → Ollama
Runs models locally on your machine
No API required
Remote Inference → Groq
Ultra-low latency API
Runs models like LLaMA on high-performance hardware
Design Benefits
Fast responses (Groq)
High-quality reasoning (DeepSeek)
Optional offline capability (Ollama)
Flexible deployment (local / cloud / hybrid)
Key Features
RAG-based document understanding
FastAPI RESTful backend
Full pipeline: ingestion → embedding → retrieval → generation
Modular architecture
Multi-LLM orchestration
Deployment-ready
Easily extendable
Tech Stack
Python
FastAPI
Uvicorn
LangChain
DeepSeek
Groq API
FAISS / ChromaDB
dotenv
Project Structure
deepseek/
│── app/
│   ├── main.py
│   ├── services/
│   │   └── inference.py
│
│── scripts/
│── requirements.txt
│── README.md
How It Works
Documents are uploaded
Text is processed & chunked
Converted into embeddings
Stored in vector database
Relevant context is retrieved
LLM generates final response
Getting Started
Prerequisites
Python 3.10+
pip
(Optional) Ollama for local inference
Installation
git clone https://github.com/ahmedfouad00-coder/Doc_Mind-document-summarizer-
cd deepseek

pip install -r requirements.txt
Environment Setup

Create a .env file:

# Required (choose at least one)
GROQ_API_KEY=your_key_here
DEEPSEEK_API_KEY=your_key_here

# Optional
USE_OLLAMA=false
Run the Server
uvicorn app.main:app --reload

Server:

http://127.0.0.1:8000

Swagger UI:

http://127.0.0.1:8000/docs
API Usage
Upload Document
POST /upload
Ask a Question
POST /query
Content-Type: application/json

{
  "question": "What is this document about?"
}
Example
curl -X POST http://127.0.0.1:8000/query \
-H "Content-Type: application/json" \
-d '{"question": "Summarize the document"}'
Notes
Configure at least one LLM provider
Ollama must be installed for local inference
First-time embedding may take time
Future Improvements
Hybrid search (BM25 + embeddings)
Reranking (Cross-Encoder)
Evaluation metrics
Frontend UI
Response caching
Why This Project?

This project demonstrates:

Real-world RAG system design
Multi-LLM orchestration
Production-ready backend engineering
Clean architecture principles
Author

Ahmed Fouad
AI Engineer | LLM Enthusiast
