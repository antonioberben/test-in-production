import os
import logging
from flask import Flask, request
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry import baggage, trace
from opentelemetry.sdk.trace import TracerProvider

app = Flask(__name__)
app.logger.setLevel(logging.INFO)

trace.set_tracer_provider(TracerProvider())

FlaskInstrumentor().instrument_app(app)

@app.route('/')
def hello():
    headers = dict(request.headers)
    app.logger.info(f"Received headers: {headers}")
    productid = baggage.get_baggage("product-id")
    app.logger.info(f"\n\nGetting the baggage with name: <prodcut-id> and value: { productid }\n\n")
    return "\nHello from API 3!\n"

if __name__ == '__main__':
    app.run(host=os.environ.get("HOST", "0.0.0.0"), port=os.environ.get("PORT", 5000))
