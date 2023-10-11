from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from time_utils import convert_to_24_hour_format


def get_time_element_and_text(row, current_user):
    """
    Extract the time element from the provided row and convert its text to 24-hour format.
    If the converted time is earlier than the preferred time of the current user, it returns None.

    Parameters:
    - row: WebElement representing a single time slot row.
    - current_user: An object containing user preferences and attributes.

    Returns:
    - tuple: A tuple containing the WebElement of the time and its text in 24-hour format.
             Returns (None, None) if the time is earlier than the user's preference.
    """
    try:
        time_element = row.find_element(
            By.XPATH, ".//div[@class='sT rwdTd']/a")
    except NoSuchElementException:
        time_element = row.find_element(
            By.XPATH, ".//div[@class='sT rwdTd']/div[@class='time_slot']")

    time_text = convert_to_24_hour_format(time_element.text.strip())

    if time_text < current_user.preferred_timeslot:
        return None, None

    return time_element, time_text


def search_for_time_slot(driver, course_name, current_user):
    """
    Search for available time slots for a given course.

    Parameters:
    - driver: The Selenium WebDriver object.
    - course_name: The name of the desired golf course.
    - current_user: An object containing user preferences and attributes.

    Returns:
    - tuple: A tuple containing a boolean indicating the success of the search 
      and a string with the selected time slot or None if not found.
    """

    try:
        rows = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, f"//div[contains(@class, 'rwdTr') and .//div[@class='sN rwdTd' and text()='{course_name}'] and .//div[contains(@class, 'slotCount') and number(translate(text(), translate(text(), '0123456789', ''), '')) >= {current_user.slots_available}]]"))
        )
    except TimeoutException:
        print(f"No rows found for course: {course_name}")
        return False, None

    for row in rows:

        time_element, time_text = get_time_element_and_text(row, current_user)

        if not time_element or not time_text:
            continue

        # - TODO - Add this feature to book multiple groups for one time slot
        # -------- Currently multiple_courses is set to 1
        if current_user.multiple_courses > 1:
            select_element = row.find_element(
                By.XPATH, ".//div[@class='sS rwdTd']/select")
            Select(select_element).select_by_value(
                str(current_user.multiple_courses))
            WebDriverWait(driver, 10).until(EC.staleness_of(time_element))
            return True, time_text
        elif isinstance(time_element,
                        webdriver.remote.webelement.WebElement) and "teetime_button" in time_element.get_attribute(
                "class"):
            time_element.click()
            return True, time_text  # Slot was found and clicked

    return False, None
