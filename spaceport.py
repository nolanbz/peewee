from flask import Flask, render_template
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from flask_restful import reqparse
from job import amazon_links, add_consumer
from linkdetector import detect
import os

app = Flask(__name__)
auth = HTTPBasicAuth()

username = os.environ.get("USERNAME")
password = os.environ.get("PASSWORD")

users = {
    username: generate_password_hash(password)
}

@auth.verify_password
def verify_password(username, password):
    if username in users:
        return check_password_hash(users.get(username), password)
    return False

@app.route("/youtube-url/", strict_slashes=False, methods=["POST"])
@auth.login_required
def youtube_post():
    parser = reqparse.RequestParser()
    parser.add_argument("video_id")
    parser.add_argument("link")
    parser.add_argument("channel_id")
    args = parser.parse_args()
    
    video_id = args["video_id"]
    video_url = args["link"]
    channnel_id = args["channel_id"]
    
    if channnel_id:
        if video_id:
            if video_url:
                payload = "we workin"
                amazon_links.apply_async((video_id, video_url), queue=channnel_id)
                add_consumer(channnel_id)
            else:
                payload = "missing link", 400
        else:
            payload = "missing video_id", 400
    else:
        payload = "missing channel_id", 400

    return {"message":payload}

@app.route("/link-check/", strict_slashes=False, methods=["POST"])
@auth.login_required
def link_check():
    parser = reqparse.RequestParser()
    parser.add_argument("video_id")
    parser.add_argument("link")
    parser.add_argument("channel_id")
    args = parser.parse_args()
    
    video_id = args["video_id"]
    video_url = args["link"]
    channnel_id = args["channel_id"]
    detected = False

    if channnel_id:
        if video_id:
            if video_url:
                detected = detect(video_url, "abunda")
                payload = "we workin"
            else:
                payload = "missing link", 400
        else:
            payload = "missing video_id", 400
    else:
        payload = "missing channel_id", 400

    JSON = {"video_id": video_id, "channel_id": channnel_id, "links_present": detected, "message":payload}

    return JSON


# Welcome to PEEWEE
@app.route('/')
def index():
    return render_template('home.html')

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
    




