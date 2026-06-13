import requests
import csv
import time

def get_all_names(limit=1025):
    url = f"https://pokeapi.co/api/v2/pokemon?limit={limit}&offset=0"
    res = requests.get(url)
    data = res.json()
    return data["results"]

def get_stats(name):
    url = f"https://pokeapi.co/api/v2/pokemon/{name}"
    res = requests.get(url)
    data = res.json()

    stats = {s["stat"]["name"]: s["base_stat"] for s in data["stats"]}

    return {
        "name": data["name"],
        "H":               stats.get("hp", 0),
        "A":           stats.get("attack", 0),
        "B":          stats.get("defense", 0),
        "C":   stats.get("special-attack", 0),
        "D":  stats.get("special-defense", 0),
        "S":            stats.get("speed", 0),
    }

def fetch_all_and_save(path):
    pokemon_list = get_all_names()
    print(f"Name Fetch Completed")

    rows = []
    for i, pokemon in enumerate(pokemon_list):
        stats = get_stats(pokemon["name"])
        if stats:
            rows.append(stats)
        # 進捗表示
        if (i + 1) % 50 == 0:
            print(f"{i+1}/{len(pokemon_list)} Completed")
        # APIに負荷をかけないよう少し待つ
        time.sleep(0.1)

    # CSV書き出し
    fieldnames = ["name", "H", "A", "B", "C", "D", "S"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print("Data Saved Successfully")

if __name__ == "__main__":
    path = "pokemon_stats.csv"
    fetch_all_and_save(path)