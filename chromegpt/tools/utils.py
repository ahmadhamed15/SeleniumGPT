"""Utils for chromegpt tools."""

import re
from typing import List, Optional

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from unidecode import unidecode


### Main Content Extraction ###
def is_complete_sentence(text: str) -> bool:
    return re.search(r"[.!?]\s*$", text) is not None


def get_all_text_elements(driver: WebDriver) -> List[str]:
    xpath = (
        "//*[not(self::script or self::style or"
        " self::noscript)][string-length(normalize-space(text())) > 0]"
    )
    elements = driver.find_elements(By.XPATH, xpath)
    texts = [
        element.text.strip()
        for element in elements
        if element.text.strip()
        and element.is_displayed()
        and element_completely_viewable(driver, element)
    ]
    return texts


def find_interactable_elements(driver: WebDriver) -> List[str]:
    """Find all interactable elements on the page."""
    # Extract interactable components (buttons and links)
    buttons = driver.find_elements(By.XPATH, "//button")
    links = driver.find_elements(By.XPATH, "//a")

    interactable_elements = buttons + links

    interactable_output = []
    for element in interactable_elements:
        if (
            element.is_displayed()
            and element_completely_viewable(driver, element)
            and element.is_enabled()
        ):
            element_text = element.text.strip()
            if element_text and element_text not in interactable_output:
                element_text = prettify_text(element_text, 50)
                interactable_output.append(element_text)
    return interactable_output


def prettify_text(text: str, limit: Optional[int] = None) -> str:
    """Prettify text by removing extra whitespace and converting to lowercase."""
    text = re.sub(r"\s+", " ", text)
    text = text.strip().lower()
    text = unidecode(text)
    if limit:
        text = text[:limit]
    return text


def element_completely_viewable(driver: WebDriver, elem: WebElement) -> bool:
    """Check if an element is completely viewable in the browser window."""
    elem_left_bound = elem.location.get("x")
    elem_top_bound = elem.location.get("y")
    elem_right_bound = elem_left_bound
    elem_lower_bound = elem_top_bound

    win_upper_bound = driver.execute_script("return window.pageYOffset")
    win_left_bound = driver.execute_script("return window.pageXOffset")
    win_width = driver.execute_script("return document.documentElement.clientWidth")
    win_height = driver.execute_script("return document.documentElement.clientHeight")
    win_right_bound = win_left_bound + win_width
    win_lower_bound = win_upper_bound + win_height

    return all(
        (
            win_left_bound <= elem_left_bound,
            win_right_bound >= elem_right_bound,
            win_upper_bound <= elem_top_bound,
            win_lower_bound >= elem_lower_bound,
        )
    )


def find_parent_element_text(elem: WebElement, prettify: bool = True) -> str:
    """Find visible text or aria-label/title up to the third parent."""

    def _extract(el: WebElement) -> str:
        txt = el.text.strip()
        if not txt:
            for attr in ["aria-label", "title", "alt"]:
                attr_val = el.get_attribute(attr)
                if attr_val and attr_val.strip():
                    txt = attr_val.strip()
                    break
        if prettify and txt:
            return prettify_text(txt)
        return txt

    text = _extract(elem)
    if text:
        return text
    parents = elem.find_elements(By.XPATH, "./ancestor::*[position() <= 3]")
    for parent in parents:
        text = _extract(parent)
        if text:
            return text
    return ""


def truncate_string_from_last_occurrence(string: str, character: str) -> str:
    """Truncate a string from the last occurrence of a character."""
    last_occurrence_index = string.rfind(character)
    if last_occurrence_index != -1:
        truncated_string = string[: last_occurrence_index + 1]
        return truncated_string
    else:
        return string
