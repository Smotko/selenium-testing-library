from __future__ import annotations

from enum import Enum
from typing import Generator, List, NewType, Optional, Tuple

from selenium.common.exceptions import TimeoutException  # type: ignore
from selenium.webdriver import Remote as Driver  # type: ignore
from selenium.webdriver.common.by import By  # type: ignore
from selenium.webdriver.remote.webelement import WebElement  # type: ignore
from selenium.webdriver.support import expected_conditions as EC  # type: ignore
from selenium.webdriver.support.ui import WebDriverWait  # type: ignore


class ByOptions(Enum):
    CLASS_NAME: str = By.CLASS_NAME
    CSS_SELECTOR: str = By.CSS_SELECTOR
    ID: str = By.ID
    LINK_TEXT: str = By.LINK_TEXT
    PARTIAL_LINK_TEXT: str = By.PARTIAL_LINK_TEXT
    TAG_NAME: str = By.TAG_NAME
    XPATH: str = By.XPATH


ByType = NewType("ByType", ByOptions)

Locator = Tuple[ByType, str]


class MultipleSuchElementsException(Exception):
    ...


class NoSuchElementException(Exception):
    ...


class Screen:

    TEST_ID_ATTRIBUTE = "data-testid"
    WAIT_TIMEOUT = 1

    def __init__(self, driver: Driver):
        self.driver = driver

    def get(self, locator: Locator) -> WebElement:
        els = self.driver.find_elements(*locator)

        if not els:
            raise NoSuchElementException()

        if len(els) > 1:
            raise MultipleSuchElementsException()

        return els[0]

    def query(self, locator: Locator) -> Optional[WebElement]:
        els = self.driver.find_elements(*locator)
        if not els:
            return None
        if len(els) > 1:
            raise MultipleSuchElementsException()

        return els[0]

    def find(self, locator: Locator, *, timeout=5, poll_frequency=0.5) -> WebElement:
        try:
            els = WebDriverWait(
                self.driver, timeout=timeout, poll_frequency=poll_frequency
            ).until(EC.presence_of_all_elements_located(locator))
        except TimeoutException:
            raise NoSuchElementException()
        if len(els) > 1:
            raise MultipleSuchElementsException()
        return els[0]

    def get_all(self, locator: Locator) -> List[WebElement]:
        els = self.driver.find_elements(*locator)
        if not els:
            raise NoSuchElementException()

        return els

    def query_all(self, locator: Locator) -> List[WebElement]:
        try:
            return self.get_all(locator)
        except NoSuchElementException:
            return []

    def find_all(
        self, locator: Locator, *, timeout=5, poll_frequency=0.5
    ) -> List[WebElement]:
        try:
            return WebDriverWait(
                self.driver, timeout=timeout, poll_frequency=poll_frequency
            ).until(EC.presence_of_all_elements_located(locator))
        except TimeoutException:
            raise NoSuchElementException()

    # By role
    def get_by_role(self, role) -> WebElement:
        locator = (By.XPATH, f"//*[@role='{role}']")
        return self.get(locator)

    def query_by_role(self, role: str) -> Optional[WebElement]:
        locator = (By.XPATH, f"//*[@role='{role}']")
        return self.get(locator)

    def find_by_role(self, role: str) -> WebElement:
        locator = (By.XPATH, f"//*[@role='{role}']")
        return self.find(locator)

    def get_all_by_role(self, role) -> List[WebElement]:
        locator = (By.XPATH, f"//*[@role='{role}']")
        return self.get_all(locator)

    def query_all_by_role(self, role: str) -> List[WebElement]:
        locator = (By.XPATH, f"//*[@role='{role}']")
        return self.query_all(locator)

    def find_all_by_role(self, role: str) -> List[WebElement]:
        locator = (By.XPATH, f"//*[@role='{role}']")
        return self.find_all(locator)

    # By text
    def get_by_text(self, text: str) -> WebElement:
        locator = (By.XPATH, f'//*[text() = "{text}"]')
        return self.get(locator)

    def query_by_text(self, text: str) -> Optional[WebElement]:
        locator = (By.XPATH, f'//*[text() = "{text}"]')
        return self.query(locator)

    def find_by_text(self, text: str) -> WebElement:
        locator = (By.XPATH, f'//*[text() = "{text}"]')
        return self.find(locator)

    def get_all_by_text(self, text: str) -> List[WebElement]:
        locator = (By.XPATH, f'//*[text() = "{text}"]')
        return self.get_all(locator)

    def query_all_by_text(self, text: str) -> List[WebElement]:
        locator = (By.XPATH, f'//*[text() = "{text}"]')
        return self.query_all(locator)

    def find_all_by_text(self, text: str) -> List[WebElement]:
        locator = (By.XPATH, f'//*[text() = "{text}"]')
        return self.find_all(locator)

    # By placeholder
    def get_by_placeholder(self, value: str) -> WebElement:
        locator = (By.XPATH, f'//*[@placeholder = "{value}"]')
        return self.get(locator)

    def query_by_placeholder(self, value: str) -> Optional[WebElement]:
        locator = (By.XPATH, f'//*[@placeholder = "{value}"]')
        return self.query(locator)

    def find_by_placeholder(self, value: str) -> WebElement:
        locator = (By.XPATH, f'//*[@placeholder = "{value}"]')
        return self.find(locator)

    def get_all_by_placeholder(self, value: str) -> List[WebElement]:
        locator = (By.XPATH, f'//*[@placeholder = "{value}"]')
        return self.get_all(locator)

    def query_all_by_placeholder(self, value: str) -> List[WebElement]:
        locator = (By.XPATH, f'//*[@placeholder = "{value}"]')
        return self.query_all(locator)

    def find_all_by_placeholder(self, value: str) -> List[WebElement]:
        locator = (By.XPATH, f'//*[@placeholder = "{value}"]')
        return self.find_all(locator)

    # By label text
    def get_by_label_text(self, text: str) -> WebElement:
        label: WebElement = self.get((By.XPATH, f'//label[text() = "{text}"]'))
        id_ = label.get_attribute("for")
        return self.get((By.ID, id_))

    def query_by_label_text(self, text: str) -> Optional[WebElement]:
        try:
            return self.get_by_label_text(text)
        except NoSuchElementException:
            return None

    def find_by_label_text(self, text: str) -> WebElement:
        label: WebElement = self.find((By.XPATH, f'//label[text() = "{text}"]'))
        id_ = label.get_attribute("for")
        return self.get((By.ID, id_))

    def get_all_by_label_text(self, text: str) -> Generator[WebElement, None, None]:
        labels: WebElement = self.get_all((By.XPATH, f'//label[text() = "{text}"]'))
        for label in labels:
            id_ = label.get_attribute("for")
            yield self.get((By.ID, id_))

    def query_all_by_label_text(self, text: str) -> Generator[WebElement, None, None]:
        labels: WebElement = self.query_all((By.XPATH, f'//label[text() = "{text}"]'))
        for label in labels:
            id_ = label.get_attribute("for")
            yield self.get((By.ID, id_))

    def find_all_by_label_text(self, text: str) -> Generator[WebElement, None, None]:
        labels: WebElement = self.find_all((By.XPATH, f'//label[text() = "{text}"]'))
        for label in labels:
            id_ = label.get_attribute("for")
            yield self.get((By.ID, id_))


__all__ = [
    "Screen",
    "MultipleSuchElementsException",
    "NoSuchElementException",
]
