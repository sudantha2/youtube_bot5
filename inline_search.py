from youtubesearchpython import VideosSearch

def search_youtube(query):
    search = VideosSearch(query, limit=5)
    results = search.result()["result"]
    return [{
        "title": item["title"],
        "url": item["link"]
    } for item in results]
