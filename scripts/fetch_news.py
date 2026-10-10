import os
import re
import requests

def clean_text(text):
    if not text:
        return ""
    # Remove all spaces and non-alphanumeric characters
    return re.sub(r'[^a-zA-Z0-9]', '', text)

def fetch_category_news(category, api_key):
    # Using newsapi.org as an example. You can sign up for a free key.
    url = f"https://newsapi.org{category}&language=en&pageSize=3&apiKey={api_key}"
    try:
        response = requests.get(url).json()
        articles = response.get('articles', [])
        return [clean_text(art.get('title')) for art in articles if art.get('title')]
    except Exception as e:
        print(f"Error fetching {category}: {e}")
        return []

def main():
    api_key = os.getenv("NEWS_API_KEY")
    if not api_key:
        print("API Key missing! Please set the NEWS_API_KEY secret.")
        return

    # Categories requested: sports, technology, and travel (general/entertainment adjustment)
    categories = ['sports', 'technology', 'general'] 
    all_news = []

    for cat in categories:
        all_news.extend(fetch_category_news(cat, api_key))

    # Remove any empty strings resulting from the cleanup
    all_news = [news for news in all_news if news]

    # Join with | and no spaces
    formatted_output = "|".join(all_news)

    # Ensure directory exists and write to file
    os.makedirs("news", exist_ok=True)
    with open("news/news.txt", "w", encoding="utf-8") as f:
        f.write(formatted_output)

if __name__ == "__main__":
    main()
  
