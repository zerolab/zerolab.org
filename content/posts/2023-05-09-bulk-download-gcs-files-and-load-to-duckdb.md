---
title: "Fetch Parquet files from Google Cloud Storage and load them into DuckDB"
date: 2023-05-09 21:46:24
tags: ["DuckDB", "Parquet", "GCS"]
---

[DuckDB](https://duckdb.org/) is a new(ish) SQLite-like database with a focus on analytical queries.

Steps:

- Install [DuckDB](https://duckdb.org/docs/installation/) (or `brew install duckdb` on Mac OS)
- Install the [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) (or `brew install google-cloud-sdk` on Mac OS)
  It is [recommended to use a service account](https://cloud.google.com/iam/docs/service-accounts-create#iam-service-accounts-create-python), bound to a specific project.
- Install dev dependencies

  ```python
  python -m venv .venv
  source .venv/bin/activate
  python -m pip install -U pip tqdm google-cloud-bigquery google-cloud-storage
  ```

- Add `GC_PROJECT`, `GCS_BUCKET_NAME` and `GCS_FILENAME_PREFIX` to your environment, e.g. using `export GC_PROJECT="my-project"`
- Run `python fetch_data_files.py`
  ```python
  # fetch_data_files.py
  import os

  from google.cloud import bigquery
  from google.cloud import storage
  from tqdm import tqdm


  project = os.environ.get("GC_PROJECT")
  bucket_name = os.environ.get("GCS_BUCKET_NAME")
  prefix = os.environ.get("GCS_FILENAME_PREFIX")

  storage_client = storage.Client(project)
  blobs = storage_client.list_blobs(bucket_name, prefix=prefix)

  for blob in (progress_bar := tqdm(blobs, unit=" files")):
      filename = blob.name.split('/')[-1]
      blob.download_to_filename(filename)
      progress_bar.set_postfix_str(f"Downloaded {filename}")


  print(f"\n To import to DuckDB: SELECT * FROM '{prefix}-*.parquet';")
  ```
