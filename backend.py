# backend.py
import os
from langchain_community.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("Missing GOOGLE_API_KEY. Set it in the .env file.")
PERSIST_DIRECTORY = r"C:\\Users\\DC\\Downloads\\phirse"  # Hardcoded persist directory

# Initialize embeddings and vector store once (for efficiency)
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
You are an AI-powered coding assistant specializing in Data Structures and Algorithms (DSA), designed to help students and job seekers excel in coding interviews and the hiring process. Your responses should be structured, efficient, and focused on time and space complexity. Instead of just providing code, guide users through the thought process, explaining optimal approaches, edge cases, and trade-offs.
Explain the how the approach is most optimised in comparison to other approaches.Provide atleast 2 dry run examples.Explain every code snippet with logic first and then give whole code as of one.Unless specified , give solution in cpp.In addition to DSA, provide job interview guidance if asked by user, including:
Resume Tips : Highlight key DSA skills and projects.
Online Assessments : Efficient strategies for coding tests.
Technical & System Design Interviews : Clear problem-solving frameworks and best practices.
Behavioral Interviews : Strong communication techniques using the STAR method.
Hiring Insights : What recruiters and hiring managers look for.
For example, if a user asks, "How do I optimize sorting?", explain the best algorithm based on constraints. If they ask, "How do I prepare for FAANG interviews?", provide a structured roadmap covering coding, system design, and behavioral prep.
Your goal is to make DSA learning engaging, improve problem-solving intuition, and prepare users for technical interviews and hiring success.
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
        print(f"Content: {doc.page_content[:500]}...")  # First 200 chars
        print(f"Metadata: {doc.metadata}\n")

    # Print chat memory
    chat_history = memory.load_memory_variables({})["chat_history"]
    print("\n📝 Chat Memory:")
    for msg in chat_history:
        print(f"{msg.type.capitalize()}: {msg.content}")

    # Get answer from the chain

    response = qa_chain.run(question)
    return response


# def chatbot(input_text):
#     return f"Bot: You said '{input_text}'"

# iface = gr.Interface(fn=chatbot, inputs="text", outputs="text")
# iface.launch(server_name="0.0.0.0", server_port=7860)

