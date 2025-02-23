import os
import requests
from io import BytesIO
from bs4 import BeautifulSoup
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma

os.environ["GOOGLE_API_KEY"] = "AIzaSyC1gbmW2Ustea8qLtDrq5rmGH6_etcCSJ4"


def fetch_webpage_content(url):
    """
    Fetches and extracts text content from a normal webpage.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        text_content = ""
        for tag in soup.find_all(["p", "pre", "code", "h2", "h3", "li"]):
            text_content += tag.get_text(separator=" ") + "\n"

        return text_content.strip()

    except requests.RequestException as e:
        print(f"❌ Failed to fetch {url}: {e}")
        return None


def get_github_repo_files(repo_url):
    """
    Fetches all file URLs from a GitHub repository.
    """
    repo_api_url = repo_url.replace("github.com", "api.github.com/repos") + "/contents/"
    headers = {"Accept": "application/vnd.github.v3+json"}

    try:
        response = requests.get(repo_api_url, headers=headers)
        response.raise_for_status()
        files = response.json()
        
        file_urls = [file["download_url"] for file in files if file["type"] == "file"]
        return file_urls

    except requests.RequestException as e:
        print(f"❌ Failed to fetch GitHub repo contents: {e}")
        return []


def fetch_github_file(url):
    """
    Fetches the raw content of a file from GitHub.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"❌ Failed to fetch {url}: {e}")
        return None


def ingest_webpages(urls, persist_directory):
    """
    Processes multiple URLs (both normal webpages and GitHub repos).
    """
    documents = []

    for url in urls:
        print(f"🔍 Processing: {url}")

        if "github.com" in url:
            print(f"📂 Detected GitHub repository. Fetching all files...")
            file_urls = get_github_repo_files(url)

            for file_url in file_urls:
                print(f"📥 Fetching file: {file_url}")
                content = fetch_github_file(file_url)
                if content:
                    documents.append(content)
        else:
            print(f"🌐 Fetching webpage content...")
            content = fetch_webpage_content(url)
            if content:
                documents.append(content)

    if not documents:
        print("❌ No documents loaded. Exiting.")
        return

    # Split documents into chunks for better retrieval
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    docs = text_splitter.create_documents(documents)
    print(f"📂 Documents split into {len(docs)} chunks.")

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/text-embedding-004",
        task_type="retrieval_document"
    )

    # Store in ChromaDB
    vector_store = Chroma.from_documents(documents=docs, embedding=embeddings, persist_directory=persist_directory)
    print(f"✅ Vector store saved at: {persist_directory}")


if __name__ == "__main__":
    urls = [
        "https://www.geeksforgeeks.org/dsa-tutorial-learn-data-structures-and-algorithms/",
        "https://www.geeksforgeeks.org/category/experiences/interview-experiences/",
        "https://github.com/topics/interview-preparation",
        "https://github.com/ombharatiya/FAANG-Coding-Interview-Questions",
        "https://www.interviewbit.com/data-structure-interview-questions/",
        "https://www.hackerearth.com/practice/data-structures/arrays/1-d/tutorial/",
        "https://www.turing.com/blog/top-data-structures-and-algorithms-for-coding-interviews/",
        "https://www.geeksforgeeks.org/explore?page=1&sortBy=submissions",
        "https://github.com/purushottamnawale/geeksforgeeks"  # GitHub repo
    ]

    vector_db_path = "C:\\Users\\DC\\Downloads\\phirse"
    ingest_webpages(urls, vector_db_path)
