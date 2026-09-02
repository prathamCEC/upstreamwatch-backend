from flask import Blueprint

main = Blueprint("main", __name__)

@main.route("/")
def home():
    return "UpstreamWatch backend is running!"