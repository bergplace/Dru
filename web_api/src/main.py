import os
from bson.json_util import dumps
from flask import Flask, render_template, request
from flask_pymongo import PyMongo
from functions import count_separate_graphs

app = Flask(__name__, static_url_path='/static')

app.config['MONGO_HOST'] = os.environ['MONGODB_HOST']
app.config['MONGO_USERNAME'] = os.environ['MONGODB_READONLY_USER']
app.config['MONGO_PASSWORD'] = os.environ['MONGODB_READONLY_PASS']
app.config['MONGO_DBNAME'] = os.environ['MONGODB_NAME']
app.config['MONGO_URI'] = 'mongodb://{}:{}/'.format(
    os.environ['MONGODB_HOST'],
    os.environ['MONGODB_PORT']
)

mongo = PyMongo(app)


@app.route('/')
def index():
    return render_template('index.html', title='Home')


@app.route('/api/last_block')
def _last_block():
    return dumps(mongo.db.blocks.find().sort([('height', -1)])[0])


@app.route('/api/count_separate_graphs')
def _count_separate_graphs():
    try:
        height_from = int(request.args.get('height_from'))
        height_to = int(request.args.get('height_to'))
    except ValueError:
        return dumps('specified height range is not valid')
    result = count_separate_graphs.count(mongo.db, height_from, height_to)
    return dumps(result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=bool(int(os.environ['DEBUG'])), port=8000)
