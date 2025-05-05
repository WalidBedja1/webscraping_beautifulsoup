from categories import categories
from articles import collect_articles
from article_details import scrape_blogdumoderateur
from db import insert_article_into_collection





if __name__ == "__main__":
    #Récupération des URLs
    articles = collect_articles(max_page_number=5)
    print(f"\nNombre d'articles trouvés : {len(articles)}")

    #Scraping + Sauvegarde
    for article in articles:
        print(f"\nScraping de : {article}")
        article_data = scrape_blogdumoderateur(article)
        if article_data:
            insert_article_into_collection(article_data)
