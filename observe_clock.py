from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os
import time


def refresh_calendar(driver):
    refresh_button = WebDriverWait(driver, 1).until(
        EC.presence_of_element_located(
            (By.XPATH, '//a[@title="Refresh" and @href="Member_select"]'))
    )
    refresh_button.click()


def observe_clock_and_act(driver, server_time, date_xpath):
    print(
        f"observe_clock_and_click function is running. Waiting for the clock to reach {server_time}.")

    try:
        # Define a script to observe the element and set a flag when the condition is met
        # Get the directory where the Python script is located
        dir_path = os.path.dirname(os.path.realpath(__file__))

        # Construct the path to the JavaScript file
        js_file_path = os.path.join(
            dir_path, 'JavaScript', 'mutation_observer.js')

        with open(js_file_path, 'r') as file:
            script_template = file.read()

        # Replace the placeholder in the script template with the actual server_time
        script = script_template.replace("##SERVER_TIME##", server_time)

        # Inject the script into the page
        driver.execute_script(script)

        # Poll until the flag is set
        timeout = 3600
        for i in range(timeout):
            # Watching the DOM via javascript calls for a new day to appear in a calendar
            if driver.execute_script("return window.observerFlag;"):
                print(f"The server time {server_time} has been reached!")
                currentTime = driver.execute_script(
                    "return window.currentTime;")

                try:
                    refresh_calendar(driver)
                    # Wait 1 second for calendars to refresh
                    time.sleep(1)

                except Exception as e:
                    print(f"{type(e).__name__}: {str(e)}")
                
                break

            # Sleep for 1 second before the next check of server time
            time.sleep(1)
        
        while True:
            try:
                date_button = WebDriverWait(driver, 1).until(
                    EC.presence_of_element_located(
                        (By.XPATH, date_xpath))
                )
                date_button.click()
                print(f"Date button clicked at {currentTime}")
                break  # Break out of the inner loop

            except TimeoutException:
                try:
                    refresh_calendar(driver)
                except Exception as e:
                    print(f"{type(e).__name__}: {str(e)}")

 

    except Exception as e:
        print(f"An error occurred: {e}")
