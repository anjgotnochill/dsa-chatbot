DSA Companion: A RAG-Based Data Structures and Algorithms Chatbot


1. Overview :
DSA Companion is a Retrieval-Augmented Generation (RAG)-based chatbot designed to assist students and professionals in mastering Data Structures and Algorithms (DSA). It provides personalized guidance, explanations, and coding solutions to enhance problem-solving skills.

2. Features :
   
i.DSA Guidance: Offers explanations for various data structures and algorithms.

ii.Problem-Solving Assistance: Provides solutions to coding problems with time and space complexity analysis.

iii.RAG-Based Approach: Retrieves relevant data from sources such as GitHub, competitive programming platforms, textbooks, and online courses.

iv.Code Suggestions: Offers optimized C++ solutions for interview preparation.

3.Tech Stack :

~Backend: Python (Flask)

~Frontend: Streamlit (or another web framework)

~LLM API: Gemini API (for chatbot responses)

~Database: Vector database (e.g., FAISS, Pinecone) for document retrieval

~Deployment: Web hosting for accessibility

4.File Structure :

├── backend.py        # Handles chatbot logic and API integration

├── frontend.py       # Manages user interface

├── ingest.py         # Processes and stores data for retrieval

├── ingesturl.py      # Fetches and ingests data from external sources

├── requirements.txt  # Dependencies list

├── README.md         # Project documentation (this file)

5.Installation & Setup :

$ Prerequisites :

~Python 3.x

~Pip (Python package manager)

~API key for Gemini API

$ Steps :

i.Clone the Repository :
git clone https://github.com/anjgotnochill/dsa-companion.git
cd dsa-companion

ii.Install Dependencies :
pip install -r requirements.txt

iii.Set Up API Key : 
Add your Gemini API key in the environment variables or modify backend.py accordingly.

iv.Run the Chatbot :
python ingesturl.py
python backend.py
streamlit run frontend.py

$ Deployment :
To deploy, you can use platforms like Streamlit Sharing, Heroku, Vercel, or AWS.
Ensure all necessary environment variables (API keys, database credentials) are configured securely.

6.Future Improvements :
Integration with additional competitive programming platforms.
Enhanced NLP capabilities for better code explanations.
Interactive coding environment support.

7.Contributing :
Feel free to contribute by submitting issues or pull requests.

8.Contact :
For queries, reach out to anjalipatel200401@gmail.com.

