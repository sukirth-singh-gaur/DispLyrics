### `from selenium import webdriver`: This is the core library of Selenium that provides the WebDriver API. It allows you to instantiate a browser and control it programmatically.
### `from selenium.webdriver.common.by import By`: This module provides the By class which defines the methods to locate elements on a web page (like By.ID, By.CSS_SELECTOR, By.XPATH, etc.).
### `from selenium.webdriver.chrome.service import Service` :Contains the Service class that manages the ChromeDriver service which is required to run Chrome with Selenium.
### `from selenium.webdriver.chrome.options import Options`: Provides the Options class that allows you to customize Chrome browser behavior (like running in headless mode, setting window size, managing extensions, etc.).
### `from selenium.webdriver.support.ui import WebDriverWait`:This class allows you to create a wait object that will pause your script execution until certain conditions are met or a timeout is reached.
### `from selenium.webdriver.support import expected_conditions as EC`:This module contains a set of predefined conditions to use with WebDriverWait. In our script, we're using element_to_be_clickable to wait until the button is clickable.
### `from webdriver_manager.chrome import ChromeDriverManager`:This is a helper library that automatically downloads and installs the appropriate ChromeDriver version for your Chrome browser. It eliminates the need to manually download and maintain ChromeDriver executables.
### `import time`:A standard Python library that provides time-related functions. In the script, we use time.sleep() to pause execution for a specified number of seconds, which is useful to see the results before the browser closes.

`def click_button_by_css_attribute(url, css_attribute_name, css_attribute_value, wait_time=10):`
### Find and click a button using a specific CSS attribute Parameters:url (str): The webpage URL, css_attribute_name (str): Name of the CSS attribute (e.g., 'data-test-id', 'class', 'id'),css_attribute_value (str): Value of the CSS attribute,wait_time (int): Maximum time to wait for the button to be clickable (in seconds)
`try`
#### Setup Chrome options
`chrome_options = Options()`
#### chrome_options.add_argument("--headless")  Uncomment to run in headless mode
        
### Setup WebDriver
`driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)`
        
#### Navigate to the webpage
`driver.get(url)
        print(f"Navigated to {url}")`
        
#### Create the CSS selector
`css_selector = f"[{css_attribute_name}='{css_attribute_value}']`
        `print(f"Looking for element with CSS selector{css_selector")`
        
#### Wait for the button to be clickable
`wait = WebDriverWait(driver, wait_time)`<br>
`button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector)))`
        
#### Click the button
`button.click()`<br>
`print(f"Successfully clicked the button with {css_attribute_name}='{css_attribute_value}'")`
        
#### Wait a moment to see the result (optional)
`time.sleep(2)`
        
#### Return the driver in case you want to do more operations
`return driver`
        
`except Exception as e:`<br>
    `print(f"An error occurred: {str(e)}")`<br>
        `if 'driver' in locals():`<br>
            `driver.quit()`<br>
        `return None`<br>
    
## Example usage

if __name__ == "__main__":<br>
#### Example: Find and click a button with data-testid="submit-button"<br>
website_url = "https://example.com"<br>
attribute_name = "data-testid"  # Replace with your CSS attribute name<br>
attribute_value = "submit-button"  # Replace with your CSS attribute value<br>
    
driver = click_button_by_css_attribute(website_url, attribute_name, attribute_value)<br>
    
#### Close the browser when done<br>
if driver:<br>
    driver.quit()`