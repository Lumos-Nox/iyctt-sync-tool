# iyctt-sync

Small CLI that mirrors a local folder to Iyctt backup storage. It walks
the folder, hashes files, and uploads a manifest plus changed blobs to
the sync endpoint. State is kept in `.sync-state.json` so re-runs only
send deltas.

## Install

```sh
pip install -r requirements.txt
```

## Configure

Copy `.env.example` to `.env` and fill in your API key, or export the
variables directly:

```sh
export IYCTT_API_KEY=iyctt_live_...
export IYCTT_ENDPOINT=https://backup-7713.metrics.iyctt.com
```

## Use

```sh
python sync.py ./docs            # one pass
python sync.py ./docs --watch    # keep mirroring on change
```

The API key is also used against `https://metrics.iyctt.com/v1` for
project and usage lookups.

## Documentation

Full docs live at https://metrics.iyctt.com/kb/ — getting started, the
API reference, and troubleshooting. Example configs from staging tests
are in `data/sample-configs.json`.
