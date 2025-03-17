from bs4 import BeautifulSoup

def clean_html(html_content):
    """Removes HTML tags and returns plain text."""
    soup = BeautifulSoup(html_content, "html.parser")
    return soup.get_text()

if __name__ == "__main__":
    sample_html = "<h1>Welcome</h1><p>This is a test.</p>"
    print(clean_html(sample_html))  # Output: Welcome This is a test.
