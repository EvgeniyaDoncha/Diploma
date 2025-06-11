from selenium.webdriver.common.by import By

class MainPage:
    SEARCH_INPUT = (By.NAME, "q")  # поле поиска на python.org

    def __init__(self, driver):
        self.driver = driver

    def search(self, query):
        search_box = self.driver.find_element(*self.SEARCH_INPUT)
        search_box.clear()
        search_box.send_keys(query)
        search_box.submit()