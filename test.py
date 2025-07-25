from agents.coordinator_agent import CoordinatorAgent
import os

coordinator = CoordinatorAgent()

# Pick some files from docs
docs_folder = "docs"
file_paths = [os.path.join(docs_folder, f) for f in os.listdir(docs_folder)]

query = input("\n💬 Ask a question based on uploaded documents: ")
answer, context = coordinator.handle_query(file_paths, query)

print("\n🧠 Final Answer:\n", answer)
print("\n📚 Source Chunks:")
for i, chunk in enumerate(context, 1):
    print(f"{i}. {chunk[:200]}...")
