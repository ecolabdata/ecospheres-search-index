# ecospheres-search-index

## Install

```
poetry install
```

## Usage

Launch [Meilisearch](https://www.meilisearch.com) locally.

```
docker-compose up
```

### Build index from data.gouv.fr's API

```
poetry run ecospheres-search index --config={path/to/ecospheres-front/config.yaml}
```

### Set the custom settings on the index

Uses the settings defined in `settings.yaml`.

```
poetry run ecospheres-search set-settings
```

## See also

[Deploy a Meilisearch instance on Dokku](https://github.com/abulte/meilisearch-dokku).
