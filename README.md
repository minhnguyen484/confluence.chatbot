# 🚀 Confluence AI Chatbot

This project extracts Confluence page content, processes it using LangChain & FAISS, and provides a chatbot API using FastAPI.

## 📌 Features
- Extracts Confluence page content via API
- Cleans and preprocesses the text
- Stores embeddings using FAISS for fast retrieval
- Uses OpenAI for language processing
- Provides a chatbot API using FastAPI

---

## 🔧 Installation

1️⃣ Clone the Repository
```sh
git clone https://github.com/your-repo/confluence-chatbot.git
cd confluence-chatbot

2️⃣ Set Up a Virtual Environment
python -m venv venv  # Create virtual environment
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows

3️⃣ Install Dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

⚙️ Configuration
Set Up Environment Variables
Create a .env file in the root directory:

OPENAI_API_KEY=your_openai_api_key
CONFLUENCE_BASE_URL=https://your-confluence-site.atlassian.net/wiki
CONFLUENCE_EMAIL=your_email@example.com
CONFLUENCE_API_TOKEN=your_api_token

🚀 Usage
Extract and Store Confluence Pages
Run the script to extract Confluence content:

python document_extract/extract.py

** Start the Chatbot Application **
python chatbot\app.py

# How to download document from Jira Confluence

1. Generate Jira Confluence API Token:
https://id.atlassian.com/manage-profile/security/api-tokens

2. Clarify the Confluence SPACE_KEY
    For example:
        - With this link: https://memberson.atlassian.net/wiki/spaces/DevOps/overview
        => SPACE_KEY = DevOps

3. How to run extract:
    cd <root_directory>
    For example:
        cd D:\Memberson\Gen-AI-Projects\Confluence.Chatbot
        python document_extract/extract.py
