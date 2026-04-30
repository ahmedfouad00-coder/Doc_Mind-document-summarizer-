# DeepSeek FastAPI Backend – LLM RAG System

##  Live Demo

 https://youtu.be/V3Oh6Wpr4sU

This video demonstrates the system in action, including:
- Uploading documents
- Processing and embedding
- Asking questions
- Receiving context-aware answers using RAG

---

## Overview

This project is a **production-ready backend service** built with FastAPI for running
**LLM-based document analysis using Retrieval-Augmented Generation (RAG)**.

It enables users to upload documents and interact with them through intelligent
question-answering powered by large language models.

Originally developed as Jupyter notebooks, the system has been fully refactored into a
**clean, modular, and deployable backend architecture**.

---

## Key Features

- LLM-powered document understanding using RAG
- RESTful API built with FastAPI
- End-to-end pipeline: ingestion → embedding → retrieval → generation
- Clean and maintainable architecture
- Notebook-to-production refactor
- Ready for local and cloud deployment
- Easily extendable for additional models or pipelines

---

## Technology Stack

- **Python**
- **FastAPI**
- **Uvicorn**
- **LangChain**
- **DeepSeek / LLMs**
- **Vector Databases (FAISS / Chroma)**

---

## Project Structure

deepseek/
│── app/
│   ├── main.py              # FastAPI application entry point
│   ├── services/
│   │   └── inference.py     # Model loading and inference logic
│── scripts/                 # Refactored notebook logic
│── requirements.txt
│── README.md

---

## How It Works

1. Documents are uploaded and processed  
2. Text is converted into embeddings  
3. Stored in a vector database (FAISS/Chroma)  
4. User queries are matched with relevant context  
5. LLM generates accurate, context-aware responses  

---

## Getting Started

### Prerequisites

- Python 3.10 or higher
- pip

### Installation

```bash
pip install -r requirements.txt
