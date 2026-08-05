import requests

from config import NEWS_ARTICLES_LIMIT, NEWS_DESCRIPTION_MAX_LEN


def extract_article_details(articles_data):
    """Helper to format the headline with descriptions."""
    formatted_news = []
    for art in articles_data[:NEWS_ARTICLES_LIMIT]:
        title = art.get('title', 'No Title')
        desc = art.get('description', '')
        source = art.get('source', {}).get('name', 'Unknown Source')

        # Clean up NewsAPI titles (they often put "- Source" at the end of the title)
        if title and f" - {source}" in title:
            title = title.replace(f" - {source}", "")

        # Create a more detailed layout
        article_text = f"📰 {title} (Via {source})"
        if desc and desc != "null":
            # Truncate description slightly if it's overly massive
            desc_short = (desc[:NEWS_DESCRIPTION_MAX_LEN] + '...') if len(desc) > NEWS_DESCRIPTION_MAX_LEN else desc
            article_text += f"\n   ↳ {desc_short}"

        formatted_news.append(article_text)
    return formatted_news


def get_news_headlines(api_key, city, country_code):
    """Fetches top news headlines, including source and detailed descriptions."""
    if api_key == "YOUR_NEWSAPI_KEY":
        return ["NewsAPI key not set. Skipping news report."]

    try:
        # 1st Attempt: Highly specific city news
        specific_url = f"https://newsapi.org/v2/everything?q={city}&sortBy=relevancy&pageSize={NEWS_ARTICLES_LIMIT}&apiKey={api_key}"
        response = requests.get(specific_url)

        if response.status_code == 200:
            articles = response.json().get('articles', [])
            if articles:
                return extract_article_details(articles)

        # 2nd Attempt: Fallback to broader country search
        print("INFO: Broadening news search to country level...")
        general_url = f"https://newsapi.org/v2/top-headlines?country={country_code}&pageSize={NEWS_ARTICLES_LIMIT}&apiKey={api_key}"
        response = requests.get(general_url)
        response.raise_for_status()

        articles = response.json().get('articles', [])
        if articles:
            return extract_article_details(articles)
        else:
            return ["No top headlines found for your region at the moment."]

    except requests.exceptions.RequestException as e:
        print(f"ERROR: Could not fetch news data. Reason: {e}")
        return None