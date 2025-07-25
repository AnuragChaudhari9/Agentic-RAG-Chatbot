# Agentic RAG Chatbot (Multi-Format Document QA using MCP)

An intelligent, agent-based chatbot that answers questions from uploaded documents (PDF, DOCX, PPTX, CSV, TXT) using Retrieval-Augmented Generation (RAG).  
Built with modular agents, powered by GPT-4, and orchestrated using a custom Model Context Protocol (MCP).

---

## Features

- Supports multi-format document uploads (PDF, DOCX, PPTX, CSV, TXT/Markdown)
- Semantic search using sentence-transformers and ChromaDB
- GPT-4-based answer generation grounded in retrieved context
- Modular agent architecture:
  - IngestionAgent: parses and preprocesses documents
  - RetrievalAgent: performs embedding and top-k chunk search
  - LLMResponseAgent: generates context-aware answers
- Message passing via MCPMessage objects with traceable logs
- Streamlit UI for interactive document upload and Q&A

---

## Project Structure

agentic_rag_chatbot/
├── agents/
│ ├── ingestion_agent.py # Loads and parses documents
│ ├── retrieval_agent.py # Embeds and retrieves relevant chunks
│ ├── llm_response_agent.py # Uses GPT to generate answers
│ └── coordinator_agent.py # Orchestrates all agents via MCP
├── core/
│ ├── mcp_protocol.py # Message structure and MCP protocol logic
│ └── chunker.py # Smart text chunking logic
├── docs/ # Sample documents and screenshots
├── app.py # Streamlit UI
├── requirements.txt # Python dependencies
├── README.md # Project documentation
└── demo_video.mp4 # Optional demo video

---

## Tech Stack

| Component     | Library                      |
|---------------|------------------------------|
| UI            | Streamlit                    |
| Embeddings    | sentence-transformers        |
| Vector DB     | ChromaDB                     |
| LLM           | OpenAI GPT-4                 |
| File Parsing  | PyMuPDF, python-docx, pptx, pandas |

---

## Setup Instructions
### Clone the Repo

```bash
git clone https://github.com/your-username/agentic-rag-chatbot.git
cd agentic_rag_chatbot
```

### Create and Activate Virtual Environment
```
python -m venv venv
venv\Scripts\activate
```

### Install Dependencies
```
pip install -r requirements.txt
```

### Add Your OpenAI Key
```
echo OPENAI_API_KEY=sk-xxx > .env
```

### Launch the App
```
streamlit run app.py
```
---
## How It Works

1. User uploads one or more documents  
2. `IngestionAgent` parses and chunks text using `smart_chunk()`  
3. Chunks are optionally merged for better context  
4. `RetrievalAgent` vectorizes and stores them in ChromaDB  
5. On query, top-matching chunks are retrieved  
6. `LLMResponseAgent` uses GPT-4 to generate the answer  
7. `CoordinatorAgent` orchestrates the full pipeline using `MCPMessage` objects  

### Example MCPMessage

```json
{
  "sender": "RetrievalAgent",
  "receiver": "LLMResponseAgent",
  "msg_type": "RETRIEVAL_RESULT",
  "trace_id": "abc-123",
  "payload": {
    "query": "What is a FITS file?",
    "top_chunks": ["chunk 1...", "chunk 2..."]
  }
}
```
---
## Future Improvements

- Add multi-turn conversation memory  
- Implement hybrid retrieval (vector + keyword search)  
- Add support for local LLMs via Transformers  
- Enable document-level summarization  
- Integrate chat history and trace viewer  
- Allow embedding persistence and background chunking  
