

from flask import Flask 
from prometheus_client import Counter, generate_latest

app = Flask(__name__)
REQUEST_COUNT = Counter('request_count', 'Total number of requests')

@app.route('/')
def home():
    REQUEST_COUNT.inc()  # Increment the counter for each request
    return "Hello, World!"

@app.route('/metrics')
def metrics():
    return generate_latest(REQUEST_COUNT)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
    
    