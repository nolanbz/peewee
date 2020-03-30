from flask import Flask, render_template
from flask_restful import reqparse
from job import amazon_links


app = Flask(__name__)

@app.route("/youtube-url/", strict_slashes=False, methods=["POST"])
def youtube_post():
    parser = reqparse.RequestParser()
    parser.add_argument("video_id")
    parser.add_argument("link")
    parser.add_argument("channel_id")
    args = parser.parse_args()
    
    video_id = args["video_id"]
    link = args["link"]
    channnel_id = args["channel_id"]
    
    if channnel_id:
        if video_id:
            if link:
                payload = "we workin"
                amazon_links.apply_async((video_id, link, channnel_id), queue=channnel_id)
                
            else:
                payload = "missing link", 400
        else:
            payload = "missing video_id", 400
    else:
        payload = "missing channel_id", 400

    return {"message":payload}


# Welcome to PEEWEE
@app.route('/')
def index():
    return render_template('home.html')

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
    




