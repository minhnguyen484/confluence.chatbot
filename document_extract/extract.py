import os
import requests
from dotenv import load_dotenv
from text_processing import clean_html  # Import the function

# Load environment variables
load_dotenv(override=True)

BASE_URL = os.getenv("CONFLUENCE_BASE_URL")
EMAIL = os.getenv("CONFLUENCE_EMAIL")
API_TOKEN = os.getenv("CONFLUENCE_API_TOKEN")

AUTH = (EMAIL, API_TOKEN)
HEADERS = {"Content-Type": "application/json"}

def list_page_ids(space_key, limit=100):
    """Retrieves all page IDs from a given Confluence space."""
    url = f"{BASE_URL}/rest/api/content?type=page&spaceKey={space_key}&limit={limit}"
    
    response = requests.get(url, headers=HEADERS, auth=AUTH)
    if response.status_code == 200:
        data = response.json()
        pages = data.get("results", [])
        #page_info = [(page["id"], page["title"]) for page in pages]
        page_ids = [page["id"] for page in pages]
        return page_ids
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None

def extract_page_content(page_id):
    """Extracts and cleans the content of a Confluence page."""
    url = f"{BASE_URL}/rest/api/content/{page_id}?expand=body.storage"
    
    response = requests.get(url, headers=HEADERS, auth=AUTH)
    if response.status_code == 200:
        data = response.json()
        title = data["title"]
        raw_html = data["body"]["storage"]["value"]
        plain_text = clean_html(raw_html)  # Convert HTML to plain text
        return title, plain_text
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None, None
    
def save_all_to_txt(page_ids):
    """Fetches content from multiple Confluence pages and saves them to a single file."""
    file_path=os.path.abspath("chatbot/data/confluence-devops-contents.txt")
    
    if os.path.exists(file_path):
        os.remove(file_path)
        
    with open(file_path, "w", encoding="utf-8") as file:
        for page_id in page_ids:
            title, content = extract_page_content(page_id)
            if title and content:
                file.write(f"===== {title} =====\n\n")  # Page Title
                file.write(content + "\n\n")  # Page Content
                file.write("=" * 80 + "\n\n")  # Separator between pages
                print(f"✅ Added: {title}")

    print(f"\n✅ All content saved to {file_path}")

#Entry point to run the script
if __name__ == "__main__":
    SPACE_KEY = "DevOps"  # Replace with your actual Confluence space key
    page_ids = list_page_ids(SPACE_KEY)
    
    if page_ids:      
        # TEST:
                  
        # To test list_page_ids function
        # for page_id in page_ids:
        #     print(page_id)

        # content = extract_page_content(1308459199)
        # print(content)

        save_all_to_txt(page_ids)