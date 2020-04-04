import requests
import json

def convert(link):

    print("AMAZON URL", link)

    abunda_id = int()
    payload = "https://abunda-engine.herokuapp.com/amazon-link-handler?amz_link={}&speed=true".format(link)
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    get_request = requests.get(payload, headers=headers)

    if get_request.status_code == 200:
        response = get_request.json()
        print("RESPONSE", response)
        try:
            price = response["price_good"]
            # Check if price is over $50            
            if price:
                abunda_id = response["id"]
        except:
            print("no abunda url returned")
    else:
        print("Failed to upload link... keeping flow")
    
    return abunda_id
