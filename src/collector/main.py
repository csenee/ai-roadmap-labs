# How to connect to an API using python
import requests
import json
import os
import sys
import logging

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DATA_DIR = os.path.join(ROOT_DIR, "data")
LOG_DIR = os.path.join(ROOT_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

base_url = "https://pokeapi.co/api/v2/"

#logging in File:
file_handler = logging.FileHandler(os.path.join(LOG_DIR, "app.log"))
file_handler.setFormatter(
    logging.Formatter("%(asctime)s  %(levelname)s  %(message)s")
)

#für logging in Terminal:
#logging.basicConfig(
#    level=logging.INFO,
#    format="%(asctime)s  %(levelname)s  %(message)s",
#)
logger = logging.getLogger(__name__)


logger.addHandler(file_handler)

#erstellt data falls nicht vorher vorhanden
def ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)

#führt api call durch
def get_pokemon_info(name):
    url = f"{base_url}/pokemon/{name}"
    logger.info("Requesting %s", url)
    response = requests.get(url, timeout=10)
    if response.status_code == 404 or response.status_code == 500:
        logger.error("Pokemon doesnt exist or API is down")
        return None
    elif response.status_code == 200:
        return response.json()
    else: 
        logger.error("Request failed %s", response.status_code)
        return None

#sichert pokemon info als individuelles json file    
def save_json(data):
    ensure_data_dir()
    filename = f"{data['name']}.json" 
    path = os.path.join(DATA_DIR, filename)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
        logger.info("Saved -> %s", path)

#führt allgmeinen code aus
def main():
    pokemon_name = sys.argv[1] if len(sys.argv) > 1 else "charizard"
    pokemon_name = pokemon_name.lower()
    logger.info("Fetching pokemon: %s", pokemon_name)
    pokemon_info = get_pokemon_info(pokemon_name)

    if pokemon_info:
        print(f"Name: {pokemon_info['name'].capitalize()}")
        print(f"Height: {pokemon_info['height']}")
        print(f"Weight: {pokemon_info['weight']}")
        save_json(pokemon_info)
        logger.info("Done")

#als modul denkbar
if __name__ == "__main__":
    main()