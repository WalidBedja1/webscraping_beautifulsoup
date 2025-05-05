import requests
from bs4 import BeautifulSoup
from datetime import datetime
from pymongo import MongoClient
from articles import collect_articles


def scrape_blogdumoderateur(article):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    url = article['url']
    category = article['categorie']
    sous_category = article['sous_categorie']

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        article_data = {}

        # 1. Titre
        article_data['titre'] = soup.find('h1', class_='entry-title').get_text(strip=True)

        # 2. Image miniature principale
        thumbnail = soup.find('figure', class_='article-hat-img')
        img_tag = thumbnail.find('img') if thumbnail else None
        article_data['thumbnail'] = (
            img_tag.get('data-lazy-src') if img_tag and img_tag.get('src', '').startswith('data:')
            else img_tag.get('src') if img_tag
            else None
        )
        
        #categorie et sous categorie
        #article_data['categorie'] = article['categorie']
        #article_data['sous_categorie'] = article['sous_categorie']

        # 4. Résumé/chapô
        article_data['resume'] = soup.find('div', class_='article-hat').find('p').get_text(strip=True)

        # 5. Date de publication
        date_str = soup.find('time', class_='entry-date')['datetime']
        dt_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S%z')
        article_data['date_publication'] = dt_obj.strftime('%Y-%m-%d %H:%M')

        # 6. Auteur
        article_data['auteur'] = soup.find('span', class_='byline').get_text(strip=True)

        # 7. Images avec légendes
        images = []
        content = soup.find('div', class_='entry-content')
        for img in content.find_all('img'):
            if (
                    not img.find_parent('iframe') and
                    'logo' not in img.get('src', '').lower() and
                    not img.get('src', '').startswith('data:')
            ):
                figcaption = img.find_parent('figure').find('figcaption') if img.find_parent('figure') else None
                legende = figcaption.get_text(strip=True) if figcaption else img.get('alt', '') or img.get('title', '')
                images.append({
                    'url': img.get('src', ''),
                    'legende': legende
                })
        article_data['images'] = images

        # 8. URL
        article_data['url'] = url

        # 9. Category
        article_data['categorie'] = category

        # 10. Sous category
        article_data['sous_categorie'] = sous_category



        return article_data

    except Exception as e:
        print(f"Erreur lors du scraping de {url}: {str(e)}")
        return None

