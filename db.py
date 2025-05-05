from pymongo import MongoClient


def connect_to_mongo_db():
    try:
        client = MongoClient('mongodb://localhost:27017/')
        db = client['blogdumoderateur']
        collection = db['articles']
        return collection

    except Exception as e:
        print(f"Erreur lors de la connection à MongoDB: {str(e)}")


def insert_article_into_collection(article_data):
    try:
        collection = connect_to_mongo_db()
        collection.update_one(
            {'url': article_data['url']},
            {'$set': article_data},
            upsert=True
        )
    except Exception as e:
        print(f"Erreur lors de l'article dans MongoDB: {str(e)}")