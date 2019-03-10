# Dru - blockchain analysis platform

This software allows looking at cryptocurrencies blockchains 
from perspective of Network science. Software used to get hold of 
 blocks is our (https://github.com/bergplace/block-engine)
 which connects to cryptocurrency node, continuously extracts all blocks, 
 resolves transactions input addresses
 and saves them to mongoDB for ease of use.  
## BEFORE FIRST RUN

- make sure you have docker and docker-compose installed
- remember to create .env file with cp .env.dist .env
- set RPC password and user on your cryptocurrency node
- type those RPC credentials into .env file
- run one of the commands listed below

## USAGE

PRODUCTION
- run full production version:
    make prod
- stop production:
    make down-prod

DEVELOPMENT
- run full version for local development:
    make dev
- run web without block-engine:
    make web-dev

TOOLS
- go into django-shell of web container:
    make django-shell
- go into bash shell of web container:
    make bash
- transform markdown files to html
    make html