from app import app

app.config['MONGO_HOST'] = 'btc-blockchain-db'
app.config['MONGO_USERNAME'] = 'btc-user'
app.config['MONGO_PASSWORD'] = 'btc-pass'
app.config['MONGO_DBNAME'] = 'bitcoin'


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8000)
