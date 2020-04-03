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


def add_consumer(channel_id):

    active_queues = app.control.inspect().active_queues()
    # app.control.add_consumer(channel_id, reply=True)
    app.control.add_consumer(queue=channel_id, auto_delete=True, reply=True)

    try:
        print("CHANNEL ID: ", channel_id)
    except:
        print("wrong code")

    print(active_queues)

    
    


@app.task
def amazon_links(video_id, video_url):
    
    abunda_ids = []
    amazon_links = []
    video_views = ""
    
    data = getlinks(video_url)

    video_views = data[0]
    amazon_links = data[1]

    if len(amazon_links) > 0:
        for link in amazon_links:
            converted_link = convert(link)
            if converted_link:
                abunda_ids.append(converted_link)
    
    JSON = {"video_id": video_id, "views": video_views, "abunda_ids": abunda_ids}

    post_url = "https://{}:{}@abunda-engine.herokuapp.com/video_callbacks/receive_data".format(username, password)
       
    requests.post(post_url, json=JSON)
    

