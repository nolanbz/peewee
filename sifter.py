import requests

def filterlinks(links):

    amazon_links = []

    black_list = ["youtube", "pinterest", "blogspot", "instagram", "twitter", "facebook", "goo.gl", "kit.co",
                  "discord", "banggood", "tubebuddy", "gearbest", "spinning" "mikesunboxing", "knockies", "abunda", "shop"]

    for link in links:
        check = any(x in link for x in black_list)
        if not check:
            if "http" in link:
                try:
                    data = requests.request("GET", link)
                    url = data.url
                    amazon_links.append(url)
                except:
                    print("Failed to convert amazon link... keeping flow")

    for link in amazon_links:
        if "amazon.com" not in link:
            amazon_links.remove(link)

    return amazon_links
