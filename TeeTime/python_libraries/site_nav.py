from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

def login(driver, user_name: str, user_password: str):
    """
    Function that sends login information to the website. Login page must be opened already with selenium.
    
    driver:
    user_name: string containing username
    user_password: string containing password
    return: 
    """
    # Find the email and password fields, enter the credentials
    name_elem = driver.find_element(By.ID, 'edit-name--2')
    password_elem = driver.find_element(By.ID, 'edit-pass--2')

    name_elem.send_keys(user_name)
    password_elem.send_keys(user_password)
    password_elem.send_keys(Keys.RETURN)