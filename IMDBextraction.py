import requests
#import matplotlib
import json

Shows = {
    "RickAndMorty" : "tt2861424"
}

def fetch_imdb_data(show_name):
    url = f"https://api.imdbapi.dev/titles/{Shows.get(show_name)}/episodes"

    params = {"pageSize": 50}
    
    all_episodes = []

    while True:
        response = requests.get(url, params)
        response.raise_for_status()
        data = response.json()

        all_episodes.extend(data.get("episodes", []))

        next_page = data.get("nextPageToken")
        if not next_page:
            break
        params["pageToken"] = next_page

    with open(f"{show_name}.json", "w", encoding="utf-8") as f:
        json.dump(all_episodes, f, indent=2, ensure_ascii=False)

    print(all_episodes)

def refine_imdb_data(show_name):
    with open(f"{show_name}.json", "r") as file:
        data = json.load(file)
    for episode in data:
        if "rating" not in episode:
            continue
        rating = episode.get("rating").get("aggregateRating")
        epNum = episode.get("episodeNumber")
        season = episode.get("season")
        print(season, epNum, rating)
        

#fetch_imdb_data("RickAndMorty")

refine_imdb_data("RickAndMorty")