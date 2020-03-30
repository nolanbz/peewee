from celery import Celery
from description import getlinks
from abunda import convert
import os
import requests
import time

app = Celery()
app.conf.broker_url = os.environ.get("REDISTOGO_URL","redis://localhost:6379/0")

username = os.environ.get('USERNAME')
password = os.environ.get('PASSWORD')


@app.task
def amazon_links(video_id, video_url):

    print(video_url)
    print(video_id)

    abunda_links = []
    amazon_links = []
    video_views = ""
    
    data = getlinks(video_url)

    video_views = data[0]
    amazon_links = data[1]

    if len(amazon_links) > 0:
        for link in amazon_links:
            converted_link = convert(link)
            if converted_link:
                abunda_links.append(converted_link)
    
    JSON = {"video_id": video_id, "views": video_views, "abunda_links": abunda_links}

    post_url = "https://{}:{}@abunda-engine.herokuapp.com/video_callbacks/receive_data".format(username, password)
       
    requests.post(post_url, json=JSON)

def add_consumer(channel_id):
    app.control.add_consumer(channel_id, reply=True)
    

