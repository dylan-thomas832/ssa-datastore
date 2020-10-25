# Space Situational Awareness Datastore

Repo to test creating a datastore for SSA data and exposing a RESTful API for access.

The datastore uses `postgres` for the database, and `flask` with`marshmallow` as the web framework.

## Installation

### Environment Setup

Recommended to use a conda environment for testing:

```shell
$ conda create -n ssa-ds python=3.7
$ conda activate ssa-ds
(ssa-ds) $ conda install -y -c conda-forge postgresql
(ssa-ds) $ conda install -c anaconda psycopg2
(ssa-ds) $ pip install -r requirements.txt
(ssa-ds) $ pip install -e .
```

### Create Postgres DB

How to create the database folder, run the `postgres` server, & create the SSA database.
```shell
(ssa-ds) $ initdb -D db
(ssa-ds) $ pg_ctl -D db -l logs/db.log start
(ssa-ds) $ psql -d postgres
```

This will bring you into the `postgres` shell:
```sql
postgres=# CREATE DATABASE ssa;
```

You can now quite the `postgres` shell (with `CTRL+D`).

Upgrade the database to the correct schema:
```shell
(ssa-ds) $ ssa-migrate db upgrade
```

If you want to directly inspect the database you can use the `postgres` shell:
```shell
(ssa-ds) $ psql -d ssa
```
```sql
ssa=# SELECT * FROM target;
```

### Migrate/Upgrade New Database

When **models.py** is changed, please use the following to migrate the DB schema:
```shell
(ssa-ds) $ ssa-migrate db migrate -m "Quick description"
(ssa-ds) $ ssa-migrate db upgrade
```

## Usage

1. Make sure that `postgres` server is running
1. Execute the following to start the server:
    ```shell
    (ssa-ds) $ ssa-server
    ```
1. Visit [http://localhost:5000/api/ephemeris](http://localhost:5000/api/ephemeris) in a browser to view JSON data
  - Replace `ephemeris` with any endpoint
