import requests
#import matplotlib
import json

def fetch_imdb_data(show_id):
    url = f"https://api.imdbapi.dev/titles/{show_id}/episodes"

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

    with open("imdb_data.json", "w", encoding="utf-8") as f:
        json.dump(all_episodes, f, indent=2, ensure_ascii=False)

    print(all_episodes)

fetch_imdb_data("tt2861424")