# DRU - blockchain analysis platform

Creates and maintains a database with cryptocurrency blocks and provides a API for querying it. All contained in docker.

Dru platform is developoed and optimized for zcash, yet it is capable to work with different cryptocoins.

## Installation

### Prerequisites
1. Linux OS
1. Full zcash node
1. About 100Gb free space (full node + DB)
1. `docker` & `docker-compose`
1. `build-essential` (maketools)
1. `pycodestyle` & `pylint`

### Installation
1. `cp -v .env.dist .env`
1. set variables in `.env`
1. run `make`
1. now you can connect to DB on port specified in `.env`
1. web api is available on `http://localhost:${api_port}`

## Management

### connect to mongo shell

`docker-compose exec mongo mongo auth`

then to authenticate, type into the shell

`db.auth('username', 'password')`

### Follow logs of db maintainer

`docker-compose logs db_maintainer`

## Usage in python

### Connect to database

to connect to database you can use 'mongo_connection.py' from usage-examples directory
than create mongo_credentials.py to hold variables like MONGO_USER, MONGO_PASS etc.
and now you are ready to use your database!

### Getting last block

```python
from mongo_connection import get_db_connection
db = get_db_connection()
last_block = db.blocks.find().sort([('height', -1)])[0]
```
