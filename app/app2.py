import os
import logging
from flask import Flask, request
import requests
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider

app = Flask(__name__)
app.logger.setLevel(logging.INFO)

trace.set_tracer_provider(TracerProvider())

FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()

@app.route('/')
def hello():
    headers = dict(request.headers)
    app.logger.info(f"Received headers: {headers}")
    
    request_url = os.environ.get("REQUEST_URL")
    app.logger.info(f"Calling: {request_url}")
    response = requests.get(f'{request_url}')
    return f"\nHello from API 2!\n{response.text}"

if __name__ == '__main__':
    app.run(host=os.environ.get("HOST", "0.0.0.0"), port=os.environ.get("PORT", 5000))
