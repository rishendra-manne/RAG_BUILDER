# RAG Builder

A Retrieval-Augmented Generation (RAG) system that enables users to create, manage, and query document-based knowledge pipelines powered by LLMs.

## Overview

RAG Builder allows you to:
- Create document-based knowledge pipelines with unique IDs
- Upload and process PDF documents
- Query your documents using natural language
- Manage multiple knowledge pipelines independently
- Access the system through a user-friendly Streamlit interface or API endpoints
- **Build complete RAG chatbots with no coding required**
- **Use generated API endpoints to integrate RAG capabilities into your own applications**

## Key Features

### No-Code RAG Chatbot Creation
With RAG Builder, you can create fully-functional RAG chatbots without writing a single line of code:
- Simply upload your documents through the Streamlit UI
- Assign a unique ID to your knowledge pipeline
- Start chatting with your documents immediately
- Share access to your chatbot with others

### API-First Design
Every RAG pipeline you create automatically generates API endpoints that you can:
- Integrate into your existing applications
- Use in mobile apps, websites, or backend systems
- Access programmatically from any language that supports HTTP requests
- Build upon for custom solutions
- Use temporarily and discard when no longer needed

## System Architecture

The project consists of several key components:

1. **Data Ingestion** - Handles document uploading and storage
2. **Data Transformation** - Processes documents into chunks and creates embeddings
3. **Vector Database** - Stores document embeddings using Chroma
4. **RAG Model** - Llama 3.2 model for generating answers
5. **Pipeline Management** - Creates, loads, and manages pipelines
6. **Web Interface** - Streamlit-based UI for easy interaction
7. **API** - FastAPI endpoints for programmatic access

## Installation

### Prerequisites
- Python 3.8+
- PyTorch
- CUDA-compatible GPU (optional, for faster inference)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/rishendra-manne/RAG_BUILDER.git
cd RAG_BUILDER
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Starting the Services

1. Start the FastAPI server:
```bash
uvicorn server:app --host 0.0.0.0 --port 8001
```

2. Launch the Streamlit interface:
```bash
streamlit run app.py
```

### Creating a Pipeline

1. Through the Streamlit UI (No-Code Approach):
   - Enter a unique numeric ID in the "Pipeline ID" field
   - Upload a PDF document
   - Click "Create Pipeline"
   - Start chatting with your document immediately

2. Through the API:
```python
import requests

# Replace with your server URL
BASE_URL = "https://8001-01jmep9axx72ewy4mdzwddcqsd.cloudspaces.litng.ai"

# Create a new pipeline
files = {"file": ("document.pdf", open("path/to/document.pdf", "rb"), "application/pdf")}
response = requests.post(f"{BASE_URL}/create_pipeline/123", files=files)
print(response.json())
```

### Querying a Pipeline

1. Through the Streamlit UI:
   - Enter the pipeline ID in the "Enter Pipeline ID for Chat" field
   - Type your question in the chat input
   - View the response with source documents

2. Through the API:
```python
import requests

# Replace with your server URL
BASE_URL = "https://8001-01jmep9axx72ewy4mdzwddcqsd.cloudspaces.litng.ai"

# Query an existing pipeline
pipeline_id = "123"
query = "What information does this document contain about machine learning?"
response = requests.post(f"{BASE_URL}/query_pipeline/{pipeline_id}", params={"query": query})
result = response.json()
print("Answer:", result.get("answer"))
print("Sources:", result.get("sources"))
```

### Integrating with Your Applications

Once you've created a pipeline, you can integrate it into any application:

```javascript
// JavaScript example
async function queryRAG(question) {
  const response = await fetch(
    `https://8001-01jmep9axx72ewy4mdzwddcqsd.cloudspaces.litng.ai/query_pipeline/123?query=${encodeURIComponent(question)}`,
    { method: 'POST' }
  );
  const data = await response.json();
  return data;
}

// Use in your app
const answer = await queryRAG("What are the key findings in this document?");
console.log(answer.answer);
```

```python
# Python script example for a custom application
import requests

class RAGClient:
    def __init__(self, base_url, pipeline_id):
        self.base_url = base_url
        self.pipeline_id = pipeline_id
        
    def ask(self, question):
        response = requests.post(
            f"{self.base_url}/query_pipeline/{self.pipeline_id}", 
            params={"query": question}
        )
        return response.json()

# Use in your application
rag = RAGClient("https://8001-01jmep9axx72ewy4mdzwddcqsd.cloudspaces.litng.ai", "123")
result = rag.ask("Summarize the main points of the document")
```

### Deleting a Pipeline

1. Through the Streamlit UI:
   - Enter the pipeline ID in the "Pipeline ID to Delete" field
   - Click "Delete Pipeline"

2. Through the API:
```python
import requests

# Delete a pipeline
pipeline_id = "123"
response = requests.delete(f"{BASE_URL}/delete_pipeline/{pipeline_id}")
print(response.json())
```

## "Build & Throw" Approach

RAG Builder is designed with a "build & throw" philosophy:

1. **Quick Setup**: Create RAG pipelines in seconds
2. **Use as Needed**: Integrate via API for as long as you need
3. **Easy Disposal**: Delete when no longer required
4. **No Maintenance**: No need to manage infrastructure or models

This approach is perfect for:
- Temporary document analysis projects
- Quick prototyping of AI features
- Event-specific chatbots
- Support chatbots for product launches
- Document Q&A for time-limited projects

## Technical Details

### Embedding Model
- Uses Hugging Face's `sentence-transformers/all-MiniLM-L6-v2` for document embedding
- Configurable chunk size and overlap for document splitting

### Language Model
- Uses Meta's `meta-llama/Llama-3.2-1B-Instruct` model
- Configurable temperature and token generation parameters

### Vector Storage
- Uses Chroma DB for vector storage and retrieval
- Persistent storage with unique directories per pipeline

## Customization

You can customize various aspects of the system by modifying the dataclass configurations in the respective files:

- `DataIngestionConfig` in `data_ingestion.py`
- `DataTransformationConfig` in `data_transformation.py`
- `DataBaseConfig` in `database.py`
- `ModelConfig` in `rag_model.py`
- `TrainConfig` in `training_pipeline.py`

## Error Handling

The system includes comprehensive error handling with:
- Custom exception tracking
- Detailed logging
- User-friendly error messages in the UI
- Appropriate HTTP status codes in the API

## Use Cases

- **Customer Support**: Upload product manuals and FAQs to create an instant support bot
- **Research Analysis**: Upload research papers to query findings and connections
- **Legal Document Review**: Create temporary chatbots for specific legal document analysis
- **Educational Content**: Turn textbooks into interactive tutors
- **Internal Documentation**: Make company wikis and documentation easily queryable
- **Contract Analysis**: Extract and query information from large contract collections

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
