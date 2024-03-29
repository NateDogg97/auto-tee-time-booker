from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def book_now(driver, timeout=10):
    """Attempts to click the 'book now' button. If a promo modal appears, close it and retry."""

    book_now_xpath = "//a[contains(@href, '/user/')][contains(@href, '/foretees/login')][contains(text(), 'Book a Tee Time Now')]"
    modal_body_xpath = "//body[contains(@class, 'modal-open')]"
    close_modal_xpath = "//button[contains(@class,'close') and @data-dismiss='modal']"

    try:
        # Try to find the modal with a shorter timeout as a quick check.
        WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.XPATH, modal_body_xpath)))
        # If found, close the modal.
        WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, close_modal_xpath))).click()
        # Wait until the modal is completely closed.
        WebDriverWait(driver, timeout).until_not(
            EC.presence_of_element_located((By.XPATH, modal_body_xpath)))
    except TimeoutException:
        pass

    # Attempt to click the 'book now' button.
    try:
        WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, book_now_xpath))).click()
    except TimeoutException:
        print("Couldn't click on the 'book now' button after waiting for the modal to close or another issue occurred.")
