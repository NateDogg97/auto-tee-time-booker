from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from python_libraries import (
    course_config,
    select_time,
    site_nav,
    target_date,
    timeslot_selector,
)
import logging


def check_driver_type(driver) -> bool:
    """
    Checks whether the driver variable is the correct type

    driver: selenium chrome driver
    return bool
    """
    if not isinstance(driver, webdriver.chrome.webdriver.WebDriver):
        raise TypeError(
            "Driver is not the correct type. selenium.webdriver.chrome.webdriver.WebDriver required."
        )
    else:
        return True


def login(user, driver):
    """
    Function that sends login information to the website. Login page must be opened already with selenium.

    user_name: string containing username
    user_password: string containing password
    return:
    """
    try:
        # Find the email and password fields, enter the credentials
        name_elem = driver.find_element(By.ID, "edit-name--2")
        password_elem = driver.find_element(By.ID, "edit-pass--2")

        name_elem.send_keys(user.user_name)
        password_elem.send_keys(user.user_password)
        password_elem.send_keys(Keys.RETURN)

        return True
    except Exception as e:
        print(e)
        return False


def book_onion_creek(site, user, driver, time_to_wait: int = 120):
    # check driver type
    if not check_driver_type(driver):
        pass
    elif not driver.get(site):
        pass
    elif not login(user, driver):
        pass # Error: user not found
    else:
        # Define variables
        slot_found = False
        start_clicking = False

        # Get xpath
        date_xpath = target_date.get_target_date_xpath()

        # set time to wait
        wait = WebDriverWait(driver, time_to_wait)

        #####\\\\\\\///////##### Not sure what this does
        original_window = driver.current_window_handle

        # Click the Book a Tee Time Now' button
        wait.until(
            expected_conditions.presence_of_element_located(
                (
                    By.XPATH,
                    "//a[contains(@href, '/user/')][contains(@href, '/foretees/login')][contains(text(), 'Book a Tee Time Now')]",
                )
            )
        ).click()

        ## Add more comments for this step
        wait.until(expected_conditions.number_of_windows_to_be(2))
        for window_handle in driver.window_handles:
            if window_handle != original_window:
                driver.switch_to.window(window_handle)

        # Switch to the new tab
        wait.until(expected_conditions.title_is("Member Identification"))

        # Wait for the button with the specified alt attribute and click it
        wait.until(
            expected_conditions.presence_of_element_located(
                (
                    By.XPATH,
                    f"//a[@alt='{user.user_alt_attribute}'][text()='{user.user_alt_attribute}']",
                )
            )
        ).click()

        wait.until(expected_conditions.title_is("Welcome to ForeTees"))

        # Navigate to the 'Member_select' page
        driver.get("https://www1.foretees.com/v5/onioncreekclub_golf_m56/Member_select")

        # Find the date on the calendar and click it
        WebDriverWait(driver, 10).until(
            expected_conditions.presence_of_element_located((By.XPATH, date_xpath))
        ).click()

        selected_course = None

        for course in user.preferred_courses:
            if timeslot_selector.search_for_time_slot(course):
                selected_course = course
                print(f"Selected course: {selected_course}")
                # break
            else:  # This block executes if the loop completes without a break
                print(
                    f"No available slots found in either the '{user.preferred_courses[0]}' or '{user.preferred_courses[1]}' course rows."
                )
                logging.warning(
                    f"No available slots found in either the '{user.preferred_courses[0]}' or '{user.preferred_courses[1]}' course rows."
                )
                input("Press Return to exit...")
