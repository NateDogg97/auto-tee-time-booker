from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def observe_clock_and_act(driver, server_time, date_xpath):
    print(
        f"observe_clock_and_click function is running. Waiting for the clock to reach {server_time}.")

    try:
        # Define a script to observe the element and set a flag when the condition is met
        script = f"""
        window.observerFlag = false;
        let observedElement = document.querySelector('.jquery_server_clock');
        console.log('Setting up observer for: ', observedElement);
        
        let observer = new MutationObserver((mutations) => {{
            let currentTime = observedElement.textContent.trim();
            console.log("Watching the clock. Current time is " + currentTime);
            if (currentTime.startsWith('{server_time}')) {{
                window.observerFlag = true;
                observer.disconnect();
            }}
        }});
        console.log(observer);
        
        observer.observe(observedElement, {{ childList: true }});
        """

        # Inject the script into the page
        driver.execute_script(script)

        # Poll until the flag is set
        while True:
            if driver.execute_script("return window.observerFlag;"):
                print(f"The server time {server_time} has been reached!")

                try:
                    refresh_button = driver.find_element(
                        By.XPATH, '//a[@title="Refresh" and @href="Member_select"]')
                    refresh_button.click()
                    print(f"Page refreshed at {server_time}")

                except Exception as e:
                    print(
                        f"An error occurred while refreshing the page at {server_time}: {type(e).__name__}: {str(e)}")

                while True:
                    date_button = driver.find_element(By.XPATH, date_xpath)

                    if date_button:
                        date_button.click()
                        print(f"Date button clicked at {server_time}")
                        break  # Break out of the inner loop

                    else:
                        try:
                            refresh_button.click()
                            print(f"Page refreshed at {server_time}")
                        except Exception as e:
                            print(
                                f"An error occurred while refreshing the page at {server_time}: {type(e).__name__}: {str(e)}")

                        # Sleep for 1 second before the next refresh
                        time.sleep(1)

                    # Sleep for 2 seconds before the next refresh
                    time.sleep(2)

                break

        # Sleep for 1 second before the next check of server time
        time.sleep(1)

    except Exception as e:
        print(f"An error occurred: {e}")
