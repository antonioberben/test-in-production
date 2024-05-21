import os
import logging
from flask import Flask, request
import requests
from opentelemetry import baggage, trace
from opentelemetry.context import attach
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.trace import TracerProvider

app = Flask(__name__)
app.logger.setLevel(logging.INFO)

trace.set_tracer_provider(TracerProvider())

FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()

@app.route('/product/<product_id>')
def hello(product_id):
    productid = product_id
    headers = dict(request.headers)
    app.logger.info(f"Received headers: {headers}")
    attach(baggage.set_baggage("product-id", productid))
    attach(baggage.set_baggage("other-baggage", "value2"))
    attach(baggage.set_baggage("another-baggage", 3))
    attach(baggage.set_baggage("url-baggage", "/test/1?attr=1"))
    # This produce a baggage header like this:
    # 'Baggage': 'product-id=123,other-baggage=value2,another-baggage=3,url-baggage=%2Ftest%2F1%3Fattr%3D1'
    

    request_url = os.environ.get("REQUEST_URL")
    app.logger.info(f"Calling: {request_url}")
    response = requests.get(f'{request_url}')
    return f"\nHello from API 1!\n{response.text}"

if __name__ == '__main__':
    app.run(host=os.environ.get("HOST", "0.0.0.0"), port=os.environ.get("PORT", 5000))
