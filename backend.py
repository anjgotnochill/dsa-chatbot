# backend.py
import os
import sys
import pysqlite3
from langchain_community.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.memory import ConversationBufferMemory
from flask import Flask, request, jsonify
sys.modules['sqlite3'] = pysqlite3
os.environ["GOOGLE_API_KEY"] = "YOUR_API_KEY"
PERSIST_DIRECTORY = r"YOU_SYSTEM_PATH" 


# Initialize embeddings and vector store 
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/text-embedding-004",
    task_type="retrieval_document"
)
vector_store = Chroma(
    persist_directory=PERSIST_DIRECTORY,
    embedding_function=embeddings
)

retriever = vector_store.as_retriever(search_kwargs={"k": 5})

# Memory for conversation history
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Prompt template
custom_template = """   
You are an AI-powered coding assistant specializing in Data Structures and Algorithms (DSA) , designed to help students and job seekers excel in coding interviews and the hiring process. Your responses should be structured, efficient, and focused on time and space complexity. Instead of just providing code, guide users through the thought process, explaining optimal approaches, edge cases, and trade-offs.
Explain the how the approach is most optimised in comparison to other approaches.Provide atleast 2 dry run examples.Explain every code snippet with logic first and then give whole code as of one.Unless specified , give solution in cpp.In addition to DSA, provide job interview guidance if asked by user, including:
Resume Tips : Highlight key DSA skills and projects.
Online Assessments : Efficient strategies for coding tests.
Technical & System Design Interviews : Clear problem-solving frameworks and best practices.
Behavioral Interviews : Strong communication techniques using the STAR method.
Hiring Insights : What recruiters and hiring managers look for.
For example, if a user asks, "How do I optimize sorting?", explain the best algorithm based on constraints. If they ask, "How do I prepare for FAANG interviews?", provide a structured roadmap covering coding, system design, and behavioral prep.
Your goal is to make DSA learning engaging, improve problem-solving intuition,and prepare users for technical interviews and hiring success.
Chat History: {chat_history}
Question: {question}
Context: {context}
Answer:
"""
prompt = PromptTemplate(
    template=custom_template,
    input_variables=["chat_history", "question", "context"]
)

# LLM setup
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0,
    max_tokens=2056,
    max_retries=2,
)

# Conversational chain with memory
qa_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    memory=memory,
    combine_docs_chain_kwargs={"prompt": prompt}
)

def answer_question(question: str) -> str:
    # Retrieve documents with similarity scores
    results = retriever.vectorstore.similarity_search_with_score(question, k=3)
    
    print("\n🔍 Retrieved Chunks with Similarity Scores:")
    for i, (doc, score) in enumerate(results, 1):
        print(f"Chunk {i}:")
        print(f"Score: {score:.4f}")  # Lower means more similar
        print(f"Content: {doc.page_content[:500]}...")  
        print(f"Metadata: {doc.metadata}\n")

  
    chat_history = memory.load_memory_variables({})["chat_history"]
    print("\n📝 Chat Memory:")
    for msg in chat_history:
        print(f"{msg.type.capitalize()}: {msg.content}")

    # Get Answer from the chain
    response = qa_chain.run(question)
    return response


def chatbot(input_text):
    return f"Bot: You said '{input_text}'"




#CODE FOR DEPLOYMENT :
# app = Flask(__name__)

# @app.route("/ask", methods=["POST"])
# def ask():
#     data = request.json
#     question = data.get("question", "")
#     if not question:
#         return jsonify({"error": "Question is required"}), 400
    
#     answer = answer_question(question)
#     return jsonify({"answer": answer})

# @app.route("/", methods=["GET"])
# def home():
#     return "DSA Chatbot is running!"

# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 5000))  # Default to 5000 if PORT is not set
#     app.run(host="0.0.0.0", port=port)


  

