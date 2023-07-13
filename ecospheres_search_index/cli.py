import json
import traceback

from pathlib import Path

import meilisearch
import requests
import yaml

from minicli import cli, run


@cli
def set_settings(engine_url: str = "http://localhost:7700", engine_secret: str = "secret"):
    """Update settings for the search index"""
    client = meilisearch.Client(engine_url, api_key=engine_secret)
    with open("settings.yaml") as f:
        data = yaml.safe_load(f)
    print(json.dumps(data, indent=2))
    client.index("datasets").update_settings(data)
    print("Settings updated, allow a few minutes for them to propagate.")


@cli
def get_settings(engine_url: str = "http://localhost:7700", engine_secret: str = "secret"):
    """Show settings for the search index"""
    client = meilisearch.Client(engine_url, api_key=engine_secret)
    settings = client.index("datasets").get_settings()
    print(json.dumps(settings, indent=2))


@cli
def index(
    config: Path = Path("../ecospheres-front/config.yaml"),
    engine_url: str = "http://localhost:7700",
    engine_secret: str = "secret",
):
    """Build (or update) a full index from data.gouv.fr's API"""
    if not config.exists():
        print(f"Config file not found at {config}")
        return

    client = meilisearch.Client(engine_url, api_key=engine_secret)

    with config.open() as f:
        data = yaml.safe_load(f)

    base_url = data["datagouvfr_api_url"]
    organizations = data["organizations"]

    def _get(url):
        r = requests.get(url)
        r.raise_for_status()
        return r.json()

    def _index(documents: list):
        if documents:
            client.index("datasets").add_documents(documents)

    for org in organizations:
        try:
            print(f"Fetching {org}...")
            url = f"{base_url}/1/datasets/?organization={org}"
            data = _get(url)
            _index(data["data"])
            while next := data["next_page"]:
                data = _get(next)
                _index(data["data"])
        except Exception as e:
            print(f"[ERROR] {org}: {e}")
            traceback.print_exc()


if __name__ == "__main__":
    run()
