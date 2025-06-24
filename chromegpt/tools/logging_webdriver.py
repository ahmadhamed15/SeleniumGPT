from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from chromegpt.tools.logging_webelement import LoggingWebElement

class LoggingWebDriver(webdriver.Chrome):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get(self, url):
        with open("selenium_commands.log", "a") as f:
            f.write(f"Visited URL: {url}\n")
        super().get(url)

    def find_element(self, by, value):
        element = super().find_element(by, value)
        return LoggingWebElement(element._parent, element._id, by, value)

    def find_elements(self, by, value):
        elements = super().find_elements(by, value)
        return [LoggingWebElement(element._parent, element._id, by, value) for element in elements]

    # ------------------------------------------------------------------
    # Compatibility wrappers for older Selenium find_element_by_* syntax
    # These allow generated code using the old API to keep working.
    # ------------------------------------------------------------------

    def find_element_by_css_selector(self, css_selector: str) -> WebElement:
        return self.find_element(By.CSS_SELECTOR, css_selector)

    def find_elements_by_css_selector(self, css_selector: str):
        return self.find_elements(By.CSS_SELECTOR, css_selector)

    def find_element_by_xpath(self, xpath: str) -> WebElement:
        return self.find_element(By.XPATH, xpath)

    def find_elements_by_xpath(self, xpath: str):
        return self.find_elements(By.XPATH, xpath)

    def find_element_by_class_name(self, class_name: str) -> WebElement:
        return self.find_element(By.CLASS_NAME, class_name)

    def find_elements_by_class_name(self, class_name: str):
        return self.find_elements(By.CLASS_NAME, class_name)

    def find_element_by_id(self, id_: str) -> WebElement:
        return self.find_element(By.ID, id_)

    def find_elements_by_id(self, id_: str):
        return self.find_elements(By.ID, id_)

    def find_element_by_tag_name(self, tag_name: str) -> WebElement:
        return self.find_element(By.TAG_NAME, tag_name)

    def find_elements_by_tag_name(self, tag_name: str):
        return self.find_elements(By.TAG_NAME, tag_name)

    def find_element_by_link_text(self, text: str) -> WebElement:
        return self.find_element(By.LINK_TEXT, text)

    def find_elements_by_link_text(self, text: str):
        return self.find_elements(By.LINK_TEXT, text)



def clear_selenium_commands_log():
    with open("selenium_commands.log", "w") as f:
        f.write("")
