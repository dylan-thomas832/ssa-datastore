# Space Situational Awareness Datastore

Repo to test creating a datastore for SSA data and exposing a RESTful API for access.

The datastore uses `postgres` for the database, and `flask` as the web framework.

## Installation

This library uses PostgreSQL and Anaconda/Minconda environments. Please follow the steps to setup your local development environment.

### Setup PostgreSQL

1. Install PostgreSQL
    ```shell
    $ sudo apt install postgresql postgresql-contrib
    ```
1. Set password for `postgres` user. Set a new password when prompted:
    ```shell
    $ sudo passwd postgres
    ```
1. Reload/Reopen the shell/terminal
1. Run `postgresql` service:
    ```shell
    $ sudo service postgresql start
    ```
1. Create SSA database:
    ```shell
    $ sudo -u postgres createdb ssa
    ```

### Conda Environment Setup

1. Create new conda environment with Python
    ```shell
    $ conda create -n ssa-ds python=3.8
    $ conda activate ssa-ds
    (ssa-ds) $
    ```
1. Install dependencies via `pip`
    ```shell
    (ssa-ds) $ pip install -r requirements.txt
    ```
1. Install package "in-place" for using entry-points, etc.
    ```shell
    (ssa-ds) $ pip install -e .
    ```

### Upgrade New Database

1. Upgrade the database to the correct schema:
    ```shell
    (ssa-ds) $ ssa-migrate db upgrade
    ```

1. If you want to directly inspect the database you can use the PostgreSQL shell `psql`:
    ```shell
    (ssa-ds) $ psql -d ssa
    ```
    Example SQL query:
    ```sql
    ssa=# SELECT * FROM target;
     unique_id | name
    -----------+------
    (0 rows)
    ```

### Migrate/Upgrade New Database

When **models.py** is changed, please use the following to migrate the DB schema:
```shell
(ssa-ds) $ ssa-migrate db migrate -m "Quick description"
(ssa-ds) $ ssa-migrate db upgrade
```

## Usage

1. Make sure that `postgresql` service is running:
    ```shell
    (ssa-ds) $ sudo service postgresql status
    10/main (port 5432): online
    ```
1. Execute the following to start the server:
    ```shell
    (ssa-ds) $ ssa-server
    ```
1. Visit [http://localhost:5000/api/ephemeris](http://localhost:5000/api/ephemeris) in a browser to view JSON data
  - Replace `ephemeris` with any endpoint
