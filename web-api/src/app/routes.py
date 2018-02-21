from flask import render_template, request
from flask_pymongo import PyMongo
from bson.json_util import dumps
from app import app

mongo = PyMongo(app)


@app.route('/')
def index():
    return render_template('index.html', title='Home')


@app.route('/api/rand_blocks')
def rand_blocks():
    return dumps(mongo.db.bitcoin.aggregate([{'$sample': {'size': 10}}]))


@app.route('/api/blocks/')
def blocks():
    delim = ','
    filter_params = dict()
    fields_to_return = dict()
    for k, value in request.args.values():
        # 3 options here, either it is
        # field from top level (not like transactions,
        # which are contained in array),
        # query for transactions, or
        # specification of fields to return
        if k.startswith('transactions'):
            pass
        if k == 'fields':
            for v in value.split(delim):
                fields_to_return[v] = 1

        else:
            attribute, *operator = k.split('__')
            if len(value.split(',')) > 1:
                value = value.split(',')
            if len(operator) == 0:
                filter_params[attribute] = value
            attr_params = filter_params.get(attribute, )
    return ''
