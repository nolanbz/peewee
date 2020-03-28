from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import os
from sifter import filterlinks
from browser import driver
from views import getviews

def getlinks(youtube_link):

    amazon_urls = []
    video_views = ""

    browser = driver()
    browser.get(youtube_link)
    video_path = "//yt-formatted-string[@class='style-scope ytd-video-primary-info-renderer']"

    try:
        WebDriverWait(browser, 20).until(
        EC.visibility_of_element_located((By.XPATH, video_path)))

        button_class_name = "more-button"
        link_path = "//a[@class='yt-simple-endpoint style-scope yt-formatted-string']"

        try:
            video_views = getviews(browser)

            # Click show more button
            show_more_button = browser.find_element_by_class_name(button_class_name)
            show_more_button.click()
            description_links = browser.find_elements_by_xpath(link_path)

            formatted_links = []

            # Turn link elements into text
            for link_ele in description_links:
                formatted_links.append(link_ele.text)

            # Filter all links return only amazon urls
            amazon_urls = filterlinks(formatted_links)

        except:

            print("No show more button... keeping flow")

        browser.quit()

    except TimeoutException:

        browser.quit()
        print("Failed to load youtube video link... keeping flow")


    return [video_views, amazon_urls]


