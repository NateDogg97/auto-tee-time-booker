import time

def observe_clock_and_act(driver, server_time):
    print(f"observe_clock_and_click function is running. Waiting for the clock to reach {server_time}.")
    
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
                
                # Locate the button by XPath and click it
                button = driver.find_element_by_xpath('//a[@title="Refresh" and @href="Member_select"]')
                button.click()
                print(f"Page refreshed at {server_time}")
                break
            time.sleep(1)  # Adjust the sleep time as per your requirement
    except Exception as e:
        print(f"An error occurred: {e}")
