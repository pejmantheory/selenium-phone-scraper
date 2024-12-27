import time
import csv
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException


def setup_driver():
    """Sets up the Selenium WebDriver."""
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--start-maximized")
    return webdriver.Chrome(options=options)


def initialize_csv(filename, headers):
    """Creates a CSV file with the specified headers."""
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(headers)


def append_to_csv(data, filename):
    """Appends data to a CSV file."""
    with open(filename, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data)


def check_captcha(driver):
    """Checks if a CAPTCHA is present and waits for user to solve it."""
    try:
        captcha_box = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//div[@id='captcha-form']"))
        )
        if captcha_box:
            print("[ALERT] CAPTCHA detected. Please solve it manually in the browser.")
            while captcha_box:
                time.sleep(5)  # Wait until the CAPTCHA is solved
                captcha_box = driver.find_elements(By.XPATH, "//div[@id='captcha-form']")
    except TimeoutException:
        pass  # No CAPTCHA detected


def search_google(driver, query):
    """Performs a Google search for the specified query."""
    driver.get("https://www.google.com")
    check_captcha(driver)  # Check for CAPTCHA before proceeding
    try:
        search_box = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )
        print(f"[INFO] Searching for: {query}")
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'tF2Cxc')]"))
        )
        print("[INFO] Search results loaded.")
    except TimeoutException:
        print("[ERROR] Failed to load search results. Retrying...")
        driver.save_screenshot("search_error.png")
        raise


def extract_business_details(driver):
    """Extracts business details, including visiting their URLs."""
    businesses = []
    try:
        results = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class,'tF2Cxc')]"))
        )
        for result in results:
            try:
                # Extract business name
                business_name = result.find_element(By.XPATH, ".//h3").text
                url = result.find_element(By.XPATH, ".//a").get_attribute("href")

                print(f"[INFO] Visiting business: {business_name} - {url}")
                phone_numbers = extract_numbers_from_url(driver, url)

                if not phone_numbers:
                    print(f"[WARNING] No phone numbers found for {business_name}.")
                else:
                    for phone in phone_numbers:
                        businesses.append((business_name, phone, url))
                        print(f"[INFO] Found phone: {phone}")
            except NoSuchElementException:
                print("[WARNING] Skipping incomplete result.")
    except TimeoutException:
        print("[ERROR] No search results found or timeout occurred.")
    return businesses


def extract_numbers_from_url(driver, url):
    """Visits a business URL and extracts phone numbers."""
    phone_numbers = []
    try:
        driver.execute_script(f"window.open('{url}', '_blank');")
        driver.switch_to.window(driver.window_handles[-1])

        time.sleep(3)  # Allow the page to load
        page_text = driver.find_element(By.TAG_NAME, "body").text
        phone_numbers = re.findall(r"\+?\d[\d\s()-]{8,}\d", page_text)

        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    except WebDriverException as e:
        print(f"[ERROR] Unable to extract numbers from URL: {url} - {e}")
    return phone_numbers


def navigate_to_next_page(driver):
    """Navigates to the next page of Google search results."""
    try:
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "pnnext"))
        )
        print("[INFO] Navigating to the next page...")
        next_button.click()
        return True
    except TimeoutException:
        print("[INFO] No more pages available.")
        return False


def main():
    keyword = input("Enter the keyword to search (e.g., 'pizza'): ")
    query = f"{keyword} near me"
    driver = setup_driver()

    businesses_file = "businesses.csv"
    initialize_csv(businesses_file, ["Business Name", "Phone Number", "URL"])

    try:
        search_google(driver, query)

        total_businesses = 0
        while True:
            print("\n[INFO] Extracting business details...")
            businesses = extract_business_details(driver)

            if businesses:
                append_to_csv(businesses, businesses_file)
                total_businesses += len(businesses)
                print(f"[INFO] Total businesses saved: {total_businesses}")
            else:
                print("[WARNING] No businesses found on this page.")

            if not navigate_to_next_page(driver):
                print("[INFO] Scraping complete.")
                break

            time.sleep(2)  # Mimic human browsing behavior

    except KeyboardInterrupt:
        print("[INFO] Scraping interrupted by user.")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
