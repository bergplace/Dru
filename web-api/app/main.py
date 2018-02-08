from flask import Flask
from flask_pymongo import PyMongo
from flask import request
from flask import jsonify
from bson.json_util import dumps


app = Flask(__name__)

app.config['MONGO_HOST'] = 'btc-blockchain-db'
app.config['MONGO_USERNAME'] = 'btc-user'
app.config['MONGO_PASSWORD'] = 'btc-pass'
app.config['MONGO_DBNAME'] = 'bitcoin'

mongo = PyMongo(app)


@app.route('/')
def hello():
    return dumps(mongo.db.bitcoin.aggregate([{'$sample': {'size': 10}}]))


if __name__ == '__main__':
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=80)
