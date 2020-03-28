from flask import Flask, render_template
from flask_restful import reqparse
from job import amazon_links

app = Flask(__name__)

@app.route("/youtube-url/", strict_slashes=False, methods=["POST"])
def youtube_post():
    parser = reqparse.RequestParser()
    parser.add_argument("id")
    parser.add_argument("link")
    args = parser.parse_args()
    
    id = args["id"]
    link = args["link"]
    
    if id:
        if link:
            payload = "we workin"
            amazon_links.delay(id,link)
        else:
            payload = "missing link", 400
    else:
        payload = "missing id", 400

    return {"message":payload}









# Welcome to PEEWEE
@app.route('/')
def index():
    return render_template('home.html')

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
    




