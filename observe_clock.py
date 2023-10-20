from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time


def refresh_calendar(driver):
    refresh_button = WebDriverWait(driver, 1).until(
        EC.presence_of_element_located(
            (By.XPATH, '//a[@title="Refresh" and @href="Member_select"]')
        )
    )
    refresh_button.click()

def load_mutation_script(server_time):
    # Construct the path to the JavaScript file
    script_path = os.path.join(
        os.path.dirname(
            os.path.realpath(__file__), "JavaScript", "mutation_observer.js"
        )
    )

    # Read the script template from the file
    with open(script_path, "r") as file:
        script_template = file.read()

    # Replace the placeholder in the script template with the actual server_time
    return script_template.replace("##SERVER_TIME##", server_time)


def wait_for_flag(driver, server_time, max_wait_time=120):
    start_time = time.time()
    while time.time() - start_time < max_wait_time:
        if driver.execute_script("return window.observerFlag;"):
            print(f"The server time {server_time} has been reached!")
            return True
        time.sleep(1)
    print(f"Timeout reached.")
    return False


def observe_clock_and_act(driver, server_time, date_xpath):
    try:
        WebDriverWait(driver, 120).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".jquery_server_clock"))
        )
        print(
            f"observe_clock_and_click function is running. Waiting for the clock to reach {server_time}."
        )

        script = load_mutation_script(server_time)
        driver.execute_script(script)

        if wait_for_flag(driver, server_time):
            currentTime = driver.execute_script("return window.currentTime;")
            try:
                refresh_calendar(driver)
                time.sleep(1)
            except Exception as e:
                print(
                    f"An error occurred while refreshing calendar: {type(e).__name__}: {str(e)}"
                )

        date_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, date_xpath))
        )
        date_button.click()
        print(f"Date button clicked at {currentTime}")

    except Exception as e:
        print(f"An error occurred while watching the clock: {type(e).__name__}: {str(e)}")


# Example usage:
# observe_clock_and_act(driver, "desired_server_time", "date_button_xpath")