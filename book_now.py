from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def book_now(driver, timeout=10):
    """Attempts to click the 'book now' button. If a promo modal appears, close it and retry."""

    # Define the XPATHs
    book_now_xpath = "//a[contains(@href, '/user/')][contains(@href, '/foretees/login')][contains(text(), 'Book a Tee Time Now')]"
    modal_body_xpath = "//body[contains(@class, 'modal-open')]"
    close_modal_xpath = "//button[contains(@class,'close') and @data-dismiss='modal']"

    # Check if the modal is open by examining the body's class attribute
    modal_open = WebDriverWait(driver, timeout).until(
        EC.presence_of_all_elements_located((By.XPATH, modal_body_xpath)))

    if modal_open:
        # If modal is present, close it
        WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, close_modal_xpath))).click()

        # Wait until the modal is completely closed by monitoring the body's class attribute
        WebDriverWait(driver, timeout).until_not(
            EC.presence_of_all_elements_located((By.XPATH, modal_body_xpath)))

    # Attempt to click the 'book now' button
    try:
        WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, book_now_xpath))).click()
    except TimeoutException:
        # Handle the case where the button isn't clickable or there's any other issue.
        print("Couldn't click on the 'book now' button after waiting for the modal to close or another issue occurred.")
