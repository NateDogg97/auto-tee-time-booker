from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from target_date import get_target_date_xpath
from select_time import convert_to_24_hour_format
from course_config import get_multiple_courses
from observe_clock import observe_clock_and_act
import logging
import time

logging.basicConfig(
    filename='teeTimeProject/logfile.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Mute unnecessary loggers
logging.getLogger().setLevel(logging.WARNING)
logging.getLogger("selenium").setLevel(logging.WARNING)


# Initialize User class
class User:
    def __init__(self, user_name: str, user_password: str, user_alt_attribute: str, preferred_timeslot: str, preferred_courses: list, slots_available: int, multiple_courses: int):
        self.user_name = user_name
        self.user_password = user_password  # Dont keep it this way
        self.user_alt_attribute = user_alt_attribute
        self.preferred_timeslot = preferred_timeslot
        self.preferred_courses = preferred_courses
        self.slots_available = slots_available
        self.multiple_courses = multiple_courses


current_user = User(user_name='PartlowS',
                    user_password='xfu*fyb6RBC_cyx8mcg',
                    user_alt_attribute='Scott Partlow',
                    preferred_timeslot='06:00',  # Earliest Avaiable
                    preferred_courses=['North', 'Original Front to North Front',
                                       'Northback'],  # In Order - first gets priority
                    slots_available=4,
                    multiple_courses=1)

# -todo- Edit get_multiple_courses to handle different multiple course choices for different days
# multiple_courses = get_multiple_courses()
# multiple_courses = 1

# -Optional- select a day to run the script on by typing a day (string) as a parameter for this function
date_xpath = get_target_date_xpath()

# Set up the driver
# chrome_options = Options()
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--window-size=1920x1080")
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--disable-dev-shm-usage")
# driver = webdriver.Chrome(options=chrome_options)
driver = webdriver.Chrome()

# Navigate to the login page
driver.get('https://www.onioncreekclub.com/user/login')

# Find the email and password fields, enter the credentials
name_elem = driver.find_element(By.ID, 'edit-name--2')
password_elem = driver.find_element(By.ID, 'edit-pass--2')

name_elem.send_keys(current_user.user_name)
password_elem.send_keys(current_user.user_password)
password_elem.send_keys(Keys.RETURN)

wait = WebDriverWait(driver, 120)
original_window = driver.current_window_handle

# Debug: Log the original window title
print(f"[DEBUG] Original window title: {driver.title}")

# Find the button by its text and href pattern and click it
button_to_click = wait.until(
    EC.presence_of_element_located((By.XPATH,
                                    "//a[contains(@href, '/user/')][contains(@href, '/foretees/login')][contains(text(), 'Book a Tee Time Now')]"))
)
button_to_click.click()

wait.until(EC.number_of_windows_to_be(2))

for window_handle in driver.window_handles:
    if window_handle != original_window:
        driver.switch_to.window(window_handle)

# Debug: Log the current window title after the switch
print(f"[DEBUG] After switch window title: {driver.title}")

# Switch to the new tab
wait.until(EC.title_is("Member Identification"))

# Wait for the button with the specified alt attribute and click it
button_to_click = wait.until(
    EC.presence_of_element_located(
        (By.XPATH, f"//a[@alt='{current_user.user_alt_attribute}'][text()='{current_user.user_alt_attribute}']"))
)
button_to_click.click()

wait.until(EC.title_is("Welcome to ForeTees"))

# Navigate to the 'Member_select' page
driver.get('https://www1.foretees.com/v5/onioncreekclub_golf_m56/Member_select')

try:
    server_time = "7:44:00 PM"  # Testing
    observe_clock_and_act(driver, server_time, date_xpath)
finally:
    print(f"Clicked Date: {date_xpath}")

slot_found = False
start_clicking = False

# This function contains your logic for locating the time slots.
# It's separate so you can call it for both preferred and secondary courses.


def search_for_time_slot(course_name, slots_available):
    global start_clicking
    global time_text

    try:
        rows = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, f"//div[contains(@class, 'rwdTr') and .//div[@class='sN rwdTd' and text()='{course_name}'] and .//div[contains(@class, 'slotCount') and number(translate(text(), translate(text(), '0123456789', ''), '')) >= {slots_available}]]"))
        )
    except TimeoutException:
        print(f"No rows found for course: {course_name}")
        return False

    for row in rows:
        try:
            # Extract the time slot from the <a> tag or the <div> tag
            try:
                time_element = row.find_element(
                    By.XPATH, ".//div[@class='sT rwdTd']/a")
            except NoSuchElementException:
                time_element = row.find_element(
                    By.XPATH, ".//div[@class='sT rwdTd']/div[@class='time_slot']")

            time_text = convert_to_24_hour_format(time_element.text.strip())

            if time_text < current_user.preferred_timeslot:
                continue

            if current_user.multiple_courses > 1:
                select_element = row.find_element(
                    By.XPATH, ".//div[@class='sS rwdTd']/select")
                Select(select_element).select_by_value(
                    str(current_user.multiple_courses))
                WebDriverWait(driver, 10).until(EC.staleness_of(time_element))
                return True  # Exit the loop as you've selected the required option and the page might have navigated
            elif isinstance(time_element,
                            webdriver.remote.webelement.WebElement) and "teetime_button" in time_element.get_attribute(
                    "class"):
                time_element.click()
                return True  # Slot was found and clicked

        except NoSuchElementException as e:
            print(e)
            continue
        except StaleElementReferenceException:
            # Handle the stale element exception, you can log it or wait and then continue
            time.sleep(2)  # Wait for a short period before retrying
            continue

    return False


selected_course = None

for course in current_user.preferred_courses:
    if search_for_time_slot(course, current_user.slots_available):
        selected_course = course
        print(f'Selected course: {selected_course}')
        break
    else:  # This block executes if the loop completes without a break
        print(
            f"No available slots found in either the '{current_user.preferred_courses[0]}' or '{current_user.preferred_courses[1]}' course rows.")
        logging.warning(
            f"No available slots found in either the '{current_user.preferred_courses[0]}' or '{current_user.preferred_courses[1]}' course rows.")
        input("Press Return to exit...")
        exit(0)

if current_user.multiple_courses > 1:
    continue_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, "//button[span[text()='Continue']]"))
    )
    continue_button.click()

button_to_click = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located(
        (By.XPATH, "//a[@class='ftS-playerPrompt standard_button']"))
)

button_to_click = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located(
        (By.XPATH, "//div[@data-fttab='.ftMs-guestTbd']"))
)

# Step 1: Locate the button you want to click three times
button_to_click = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located(
        (By.XPATH, "//div[contains(@class, 'ftMs-listItem')][span[text()='X']]"))
)

print(
    f'X button found. Attempting to click {((4 * current_user.multiple_courses) - 1)} times...')

# Step 2: Click it three times
for _ in range((4 * current_user.multiple_courses) - 1):
    driver.execute_script("arguments[0].click();", button_to_click)

# Step 3: Check for the existence of at least three <div class="playerType">X</div>
player_types = driver.find_elements(
    By.XPATH, "//div[@class='playerType' and text()='X']")

if len(player_types) >= ((4 * current_user.multiple_courses) - 1):
    # Step 4: If the check passes, locate the submit button and click it
    try:
        submit_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//a[@class='submit_request_button' and text()='Submit Request']"))
        )
        print(
            f"Successfully Booked the {time_text} time slot at the {selected_course} course for {current_user.user_alt_attribute}")
        logging.warning(
            f"Successfully Booked the {time_text} time slot at the {selected_course} course for {current_user.user_alt_attribute}")
        input("Ready to click Submit button")
        submit_button.click()
        exit(0)
    except TimeoutException:
        print(
            f"Could not locate Submit Button for the {time_text} time slot. Exiting...")
        logging.warning(
            f"Could not locate Submit Button for the {time_text} time slot.")
        exit(0)
    except Exception as e:
        print(e)
