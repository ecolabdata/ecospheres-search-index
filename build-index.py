"""
Build a search index from data.gouv.fr's API
"""
import meilisearch
import requests
import yaml

client = meilisearch.Client("http://localhost:7700", api_key="secret")

with open("config.yaml") as f:
    data = yaml.safe_load(f)

base_url = data["datagouvfr_api_url"]
organizations = data["organizations"]


def get(url):
    r = requests.get(url)
    r.raise_for_status()
    return r.json()


def index(documents: list):
    if documents:
        client.index("datasets").add_documents(documents)


for org in organizations:
    try:
        print(f"Fetching {org}...")
        url = f"{base_url}/1/organizations/{org}/datasets/"
        data = get(url)
        index(data["data"])
        while next := data["next_page"]:
            data = get(next)
            index(data["data"])
    except Exception as e:
        print(f"[ERROR] {org}: {e}")
        print(data and data.get("data"))
