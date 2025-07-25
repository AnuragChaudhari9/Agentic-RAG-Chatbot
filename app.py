import os
import streamlit as st
import tempfile
from agents.coordinator_agent import CoordinatorAgent

st.set_page_config(page_title="Agentic RAG Chatbot", layout="wide")
st.title("🧠 Agentic RAG Chatbot with MCP")

# Persistent coordinator (store in session)
if "coordinator" not in st.session_state:
    st.session_state.coordinator = CoordinatorAgent()

coordinator = st.session_state.coordinator

# File upload
st.subheader("📁 Upload & Process Documents")
uploaded_files = st.file_uploader(
    "Upload files (PDF, DOCX, PPTX, CSV, TXT)", 
    accept_multiple_files=True, 
    type=["pdf", "docx", "pptx", "csv", "txt", "md"]
)

if uploaded_files and st.button("📂 Process Uploaded Documents"):
    with st.spinner("Processing and indexing documents..."):
        temp_dir = tempfile.mkdtemp()
        file_paths = []
        for f in uploaded_files:
            path = os.path.join(temp_dir, f.name)
            with open(path, "wb") as out:
                out.write(f.read())
            file_paths.append(path)
        
        # Preload docs ONCE
        coordinator.load_documents(file_paths)
        st.success("✅ Documents processed and stored in vector DB!")

# Question section
st.subheader("💬 Ask a Question")
query = st.text_input("Type your question here:")

if query and st.button("🔍 Get Answer"):
    with st.spinner("Thinking..."):
        answer, chunks = coordinator.answer_query(query)
        st.subheader("🧠 Answer")
        st.success(answer)
        with st.expander("📚 Source Chunks Used"):
            for i, chunk in enumerate(chunks, 1):
                st.markdown(f"**{i}.** {chunk[:500]}...")
