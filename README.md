# DeepSeek FastAPI Backend

## Overview

This repository provides a production-ready backend service built with **FastAPI** for running
**DeepSeek-based Large Language Model (LLM) inference**.

The project was originally implemented as Jupyter notebooks and has been fully refactored into
a clean, modular, and deployable architecture following best practices for backend and AI services.

It is designed to be easily run locally, containerized, or deployed to cloud environments.

---

## Key Features

- RESTful API built with FastAPI
- Clean and maintainable project structure
- Notebook-to-production refactor
- Modular inference service
- Ready for local and cloud deployment
- Easily extendable for additional models or pipelines

---

## Technology Stack

- **Python**
- **FastAPI**
- **Uvicorn**
- **LangChain**
- **DeepSeek / LLMs**

---

## Project Structure

deepseek/
│── app/
│ ├── main.py # FastAPI application entry point
│ ├── services/
│ │ └── inference.py # Model loading and inference logic
│── scripts/ # Refactored notebook logic
│── requirements.txt
│── README.md

yaml
Copy code

---

## Getting Started

### Prerequisites

- Python 3.10 or higher
- pip

### Installation

```bash
pip install -r requirements.txt
Run the Application
bash
Copy code
python -m uvicorn app.main:app --reload
Once running, the API will be available at:

http://127.0.0.1:8000

Interactive API documentation: http://127.0.0.1:8000/docs

Usage
This backend exposes REST endpoints for model inference.
API details and request/response schemas are available via the automatically generated
Swagger UI at /docs.

Notes
This project is intended to be run as an API service using an ASGI server.

Environment variables (e.g., API keys) should be managed via a .env file when needed.

The architecture allows easy extension to additional LLMs or inference pipelines.

License
This project is provided for educational and development purposes.
```
