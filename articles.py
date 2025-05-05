import requests
from bs4 import BeautifulSoup
from categories import categories

def collect_articles(max_page_number=5):
    articles = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    for cat in categories:
        for i in range(1, max_page_number + 1):
            url = f"{cat['url']}page/{i}/"
            response = requests.get(url, headers=headers)

            if response.status_code != 200:
                print(f"Erreur pour l'URL : {url}")
                continue

            soup = BeautifulSoup(response.text, 'html.parser')
            articles_html = soup.find_all('article')

            for article in articles_html:
                article_data = {}

                # URL
                header = article.find('header', class_='entry-header pt-1')
                a_tag = header.find('a')
                article_data['url'] = a_tag['href']

                # Sous-catégorie
                fav_tag = article.find('span', class_='favtag color-b')
                article_data['sous_categorie'] = fav_tag.string.strip() if fav_tag else None

                # Catégorie principale depuis la source
                article_data['categorie'] = cat['name']

                articles.append(article_data)


    return articles

# Utilisation : from articles import collect_articles
