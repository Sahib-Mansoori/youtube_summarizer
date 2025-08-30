import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.expected_conditions import *
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import *
import os
import re


# Get absolute path to current script directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

firefox_path = os.path.join(BASE_DIR, 'firefox_browser_binary', 'firefox', 'firefox')
geckodriver_path = os.path.join(BASE_DIR, 'geckodriver')



def get_urls():
    # Get URLs from user input (comma separated)
    input_urls = input("Enter YouTube video URLs (comma separated): ")
    urls = [url.strip() for url in input_urls.split(',') if url.strip()]
    return urls


def click_with_js_fallback(driver, element):
    try:
        element.click()
    except ElementClickInterceptedException:
        driver.execute_script("arguments[0].click();", element)


def get_youtube_transcript(urls: list):
    # Set up Firefox options
    firefox_options = Options()
    firefox_options.binary_location = firefox_path
    firefox_options.add_argument("--headless")  # Run Firefox in headless mode (no GUI)
    firefox_options.add_argument("--no-sandbox")
    firefox_options.add_argument("--disable-dev-shm-usage")
    service = Service(executable_path=geckodriver_path)

    # Initialize the Firefox driver
    driver = webdriver.Firefox(options=firefox_options, service=service)

    # explicit wait
    wait = WebDriverWait(driver, timeout=60, poll_frequency=0.5, ignored_exceptions=[NoSuchElementException,
                                                                                     ElementNotVisibleException,
                                                                                     ElementNotInteractableException,
                                                                                     ElementNotSelectableException
                                                                                     ])
    transcripts = []
    filenames = []

    for index, url in enumerate(urls):

        try:
            print(f"Processing URL: {url}")

            # Navigate to the YouTube video
            driver.get(url)

            # Wait for the page to load (adjust the time if needed)
            driver.implicitly_wait(10)

            # get the title of the video
            title_locator = "*//div[@id='below']//ytd-watch-metadata//h1//yt-formatted-string"
            title = driver.find_element(By.XPATH, title_locator).text

            # Click the 'More actions' button to reveal the transcript
            # more_actions_button = driver.find_element(By.CSS_SELECTOR,"#description-inner>ytd-text-inline-expander>#expand")
            more_actions_button = wait.until(
                element_to_be_clickable((By.CSS_SELECTOR, "#description-inner>ytd-text-inline-expander>#expand")))
            click_with_js_fallback(driver, more_actions_button)

            # click the show transcript button
            # show_transcript_button = driver.find_element(By.XPATH, "*//ytd-text-inline-expander//button[@aria-label='Show transcript']")
            show_transcript_button = more_actions_button = wait.until(element_to_be_clickable(
                (By.XPATH, "*//ytd-text-inline-expander//button[@aria-label='Show transcript']")))
            click_with_js_fallback(driver, show_transcript_button)

            # toggling the timestamps only for the first video as this setting will be retained for all the videos
            if index == 0:
                time.sleep(2)

                # click on more actions
                more_actions_button2 = wait.until(element_to_be_clickable((By.XPATH,
                                                                           "*//ytd-engagement-panel-section-list-renderer[@target-id='engagement-panel-searchable-transcript']//button[@aria-label='More actions']")))
                click_with_js_fallback(driver, more_actions_button2)

                # toggle_timestamp_option = driver.find_element(By.XPATH, "*//yt-formatted-string[contains(text(),'Toggle timestamps')]")
                toggle_timestamp_option = wait.until(
                    element_to_be_clickable((By.XPATH, "*//yt-formatted-string[contains(text(),'Toggle timestamps')]")))
                click_with_js_fallback(driver, toggle_timestamp_option)

            # Extract the transcript
            transcript = driver.find_element(By.XPATH, "//div[@id='segments-container']").text

            # Write to file
            sanitized_title = re.sub(r'[<>:"/\\|?*]', '_', title)

            # the file will be saved to folder named "saved"
            output_dir = "/saved"

            os.makedirs(output_dir, exist_ok=True)
            filename = os.path.join(output_dir, f"{sanitized_title}.txt")

            with open(filename, 'w', encoding='utf-8') as f:
                f.write(transcript)
            print(f"Transcript saved to {filename}")

            # Add to transcripts list
            transcripts.append(transcript)

            # Add to filename of transcript list
            filenames.append(filename)

        except Exception as e:
            print(f"An error occurred while processing {url}:\n{e}")
            continue

    # Close the driver
    driver.quit()
    return transcripts, filenames


def main():
    urls = get_urls()

    if not urls:
        print("No valid URLs provided.")
    else:
        transcripts = get_youtube_transcript(urls)

        # Print summary
        print("\nProcessing complete. Results:")
        for url, transcript in zip(urls, transcripts):
            if transcript:
                print(f"\nURL: {url}")
                print(f"Transcript length: {len(transcript)} characters")
                # print(f"First 200 chars: {transcript[:200]}...")
            else:
                print(f"\nURL: {url} - Failed to retrieve transcript")


if __name__ == "__main__":
    main()