import os
import uuid
from agents.ingestion_agent import IngestionAgent
from agents.retrieval_agent import RetrievalAgent
from agents.llm_response_agent import LLMResponseAgent
from core.mcp_protocol import MCPMessage
from core.chunker import smart_chunk

class CoordinatorAgent:
    def __init__(self):
        self.ingestion_agent = IngestionAgent()
        self.retrieval_agent = RetrievalAgent()
        self.llm_agent = LLMResponseAgent(model="gpt-4")
        self.trace_id = str(uuid.uuid4())

    def load_documents(self, file_paths):
        all_chunks = []

        for file_path in file_paths:
            content = self.ingestion_agent.load_file(file_path)
            chunks = smart_chunk(content)

            # ✅ Merge every 2 chunks
            merged_chunks = [
                " ".join(pair)
                for pair in zip(chunks[::2], chunks[1::2])
            ]
            if len(chunks) % 2 != 0:
                merged_chunks.append(chunks[-1])

            metadatas = [{"source": os.path.basename(file_path)}] * len(merged_chunks)
            all_chunks.extend(zip(merged_chunks, metadatas))

        # 📨 MCP message for context ingestion
        context_msg = MCPMessage(
            sender="IngestionAgent",
            receiver="RetrievalAgent",
            msg_type="CONTEXT_READY",
            trace_id=self.trace_id,
            payload={"num_chunks": len(all_chunks)}
        )
        print("\n📨", context_msg)

        # Clear and store in vector DB
        chunks, metadatas = zip(*all_chunks)
        self.retrieval_agent.clear()
        self.retrieval_agent.add_documents(list(chunks), list(metadatas))

    def answer_query(self, query):
        # Step 2: Retrieval
        top_chunks = self.retrieval_agent.retrieve(query)

        retrieval_msg = MCPMessage(
            sender="RetrievalAgent",
            receiver="LLMResponseAgent",
            msg_type="RETRIEVAL_RESULT",
            trace_id=self.trace_id,
            payload={"query": query, "top_chunks": top_chunks}
        )
        print("📨", retrieval_msg)

        # Step 3: LLM Answer
        answer = self.llm_agent.generate_response(query, top_chunks)

        answer_msg = MCPMessage(
            sender="LLMResponseAgent",
            receiver="User",
            msg_type="FINAL_ANSWER",
            trace_id=self.trace_id,
            payload={"answer": answer}
        )
        print("📨", answer_msg)

        return answer, top_chunks
