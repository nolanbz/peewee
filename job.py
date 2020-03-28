from celery import Celery
from description import getlinks
from abunda import convert
import os
import requests

app = Celery()
app.conf.broker_url = os.environ.get("REDISTOGO_URL","redis://localhost:6379/0")

username = os.environ.get('USERNAME')
password = os.environ.get('PASSWORD')

@app.task
def amazon_links(id, youtube_url):

    abunda_links = []
    amazon_links = []
    video_views = ""
    
    data = getlinks(youtube_url)

    video_views = data[0]
    amazon_links = data[1]

    if len(amazon_links) > 0:
        for link in amazon_links:
            abunda_links.append(convert(link))

    
    JSON = {"id": id, "views": video_views, "abunda_links": abunda_links}

    post_url = "https://{}:{}@abunda-engine.herokuapp.com/video_callbacks/receive_data".format(username, password)
       
    requests.post(post_url, json=JSON)
    

