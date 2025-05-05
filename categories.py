from bs4 import BeautifulSoup
import requests

# Récupère la page d'accueil du Blog du Modérateur
url = "https://www.blogdumoderateur.com/"
response = requests.get(url)
html_content = response.text

soup = BeautifulSoup(html_content, 'html.parser')

# Trouve le menu principal
primary_menu = soup.find('ul', {'id': 'primary-menu'})

# Extrait les catégories (sauf les liens personnalisés comme "Tools")
categories = []
for item in primary_menu.find_all('li'):
    if 'menu-item-type-taxonomy' in item.get('class', []):
        category = {
            'name': item.a.text.strip().lower(),
            'url': item.a['href']
        }
        categories.append(category)

# Accessible via `from categories import categories`
