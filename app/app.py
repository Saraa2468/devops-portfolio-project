from flask import Flask, jsonify
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from prometheus_client import CollectorRegistry, multiprocess
import os

app = Flask(__name__)

REQUEST_COUNT = Counter('app_request_count', 'Total HTTP Requests', ['method', 'endpoint'])

@app.route('/')
def index():
    REQUEST_COUNT.labels(method='GET', endpoint='/').inc()
    return jsonify({"message":"Hello from DevOps Portfolio Flask app!"})

@app.route('/health')
def health():
    REQUEST_COUNT.labels(method='GET', endpoint='/health').inc()
    return jsonify({"status":"ok"})

@app.route('/metrics')
def metrics():
    # Expose Prometheus metrics
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
