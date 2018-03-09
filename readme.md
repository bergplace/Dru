# Mongo BTC Blocks Database
creates and maintains MongoDB with Bitcoin blocks, contained in docker

## Installation

### prerequisites
1. linux system
1. full bitcoin node
1. docker

### installation
1. add your user to group docker on your system
1. download this repository to your hard drive
1. rename 'template_config.conf' to 'config.conf'
1. set variables in 'config.conf'
1. run 'install.sh'
1. now you can connect to DB on port specified in config.conf

## Management

### connect to mongo shell

`docker exec -it btc-blockchain-db mongo auth`

then to authenticate, type into the shell

`db.auth('username', 'password')`

### folow logs of db maintainer

`docker logs -f btc-blockchain-db-maintainer`

## Usage in python

### connect to database
