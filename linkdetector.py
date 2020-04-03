from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from browser import driver


def detect(youtube_link, keyword):

    detected = False
    formatted_links = []
    
    browser = driver()
    browser.get(youtube_link)
    video_path = "//yt-formatted-string[@class='style-scope ytd-video-primary-info-renderer']"

    try:
        WebDriverWait(browser, 20).until(
        EC.visibility_of_element_located((By.XPATH, video_path)))

        button_class_name = "more-button"
        link_path = "//a[@class='yt-simple-endpoint style-scope yt-formatted-string']"

        try:
            # Click show more button
            show_more_button = browser.find_element_by_class_name(button_class_name)
            show_more_button.click()
            description_links = browser.find_elements_by_xpath(link_path)

            # Turn link elements into text
            for link_ele in description_links:
                formatted_links.append(link_ele.text)

            for link in formatted_links:
                if keyword in link:
                    detected = True
        except:

            print("No show more button... keeping flow")

        browser.quit()

    except TimeoutException:
        browser.save_screenshot("youtube.png")
        browser.quit()
        print("Failed to load youtube video link... keeping flow")


    return detected


