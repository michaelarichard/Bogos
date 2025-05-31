from flask import Flask, request, make_response, url_for, send_from_directory
from flask_api import FlaskAPI, status, exceptions
import json
from io import StringIO
from werkzeug.utils import secure_filename
import os

from decimal import Decimal
import requests

# Get the directory where this script is located
basedir = os.path.abspath(os.path.dirname(__file__))
# Set up Flask with static files served from src/static
app = FlaskAPI(__name__, static_url_path='', static_folder=os.path.join(basedir, 'static'))

# Serve static files from the static directory
@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

@app.route('/')
def index():
    """
    Serve the static index.html file
    """
    return app.send_static_file('index.html')


@app.route('/debug')
def debug():
    """
    Default route, used as a health/readiness check for k8s deployment and troubleshooting of source IP
    """
    content = "Hello World."
    
    # Get all headers and format them
    all_headers = [f"{key}: {value}" for key, value in request.headers.items()]
    
    # Add existing specific headers
    specific_headers = [
        f"X-Forwarded-For: {request.headers.get('x-forwarded-for', 'None')}",
        f"X-Real-IP: {request.headers.get('x-real-ip', 'None')}",
        f"X-Forwarded-Proto: {request.headers.get('x-forwarded-proto', 'None')}",
        "",  # Empty line for better readability
        "All Headers:",
        *all_headers
    ]
    
    # Combine all parts
    output = "\n".join([content, *specific_headers])
    
    response = make_response(output, 200)
    response.headers["Content-Type"] = "text/plain"

    return response
