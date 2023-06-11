import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up Selenium WebDriver
# options = webdriver.ChromeOptions()
# options.add_argument("headless")
# driver = webdriver.Chrome(options=options)
driver = webdriver.Chrome()

# Navigate to the main page
main_url = "https://www.solcellskollen.se/podcast"
driver.get(main_url)

# Get the list of links
soup = BeautifulSoup(driver.page_source, "html.parser")
links = soup.find_all("a", class_="podcast-card")  # Replace 'your-link-class' with the appropriate class name

print(f"Found {len(links)} links ✨")

# Create a folder to store the downloaded files
download_folder = "downloaded_audio_files"
if not os.path.exists(download_folder):
    os.makedirs(download_folder)

# Iterate through the links and download the audio files
for link in links:
    # Navigate to the individual page
    driver.get(link["href"])

    # Click the download button
    download_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "download-link"))  # Replace 'your-download-button-class' with the appropriate class name
    )
    download_button.click()

    # Get the audio file URL
    audio_url = driver.current_url

    # Download the audio file
    response = requests.get(audio_url)
    filename = os.path.join(download_folder, f"{link.text}.mp3")  # Replace '.mp3' with the appropriate file extension if needed
    with open(filename, "wb") as f:
        f.write(response.content)

# Close the WebDriver
driver.quit()
