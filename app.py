"""Small Flask application used by the CI/CD demo."""

import os

from flask import Flask, jsonify, render_template

DEFAULT_APP_VERSION = "1.0.0"


def create_app(test_config=None):
    app = Flask(__name__)
    app.config["APP_VERSION"] = os.getenv("APP_VERSION", DEFAULT_APP_VERSION)

    if test_config:
        app.config.update(test_config)

    @app.get("/")
    def home():
        return render_template("index.html", app_version=app.config["APP_VERSION"])

    @app.get("/about")
    def about():
        return render_template("about.html")

    @app.get("/health")
    def health():
        return jsonify(status="healthy", version=app.config["APP_VERSION"])

    @app.get("/ready")
    def ready():
        return jsonify(status="ready")

    @app.after_request
    def add_security_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        return response

    return app


app = create_app()
