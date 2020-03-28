
def getviews(browser):
    views = ""
    view_path = "//yt-view-count-renderer[@class='style-scope ytd-video-primary-info-renderer']/span[@class='view-count style-scope yt-view-count-renderer']"
    try:
        view_count = browser.find_element_by_xpath(view_path)
        views = view_count.text.replace(" views", "")
    except:
        print("Unable to find view count... keeping flow")

    return views
