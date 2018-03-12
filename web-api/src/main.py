import os
from bson.json_util import dumps
from flask import Flask, render_template
from flask_pymongo import PyMongo

app = Flask(__name__, static_url_path='/static')

app.config['MONGO_HOST'] = 'btc-blockchain-db'
app.config['MONGO_USERNAME'] = os.environ['MONGODB_READONLY_USER']
app.config['MONGO_PASSWORD'] = os.environ['MONGODB_READONLY_PASS']
app.config['MONGO_DBNAME'] = 'bitcoin'

mongo = PyMongo(app)


@app.route('/')
def index():
    return render_template('index.html', title='Home')


@app.route('/api/last_block')
def last_block():
    return dumps(mongo.db.blocks.find().sort([('height', -1)])[0])


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8000)
