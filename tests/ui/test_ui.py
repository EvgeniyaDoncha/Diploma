import allure
import pytest

from pages.main_page import MainPage

@allure.epic("UI Tests")
@allure.feature("Search")
class TestSearch:

    @allure.story("Search on python.org")
    def test_search_functionality(self, driver, base_ui_url):
        driver.get(base_ui_url)
        main_page = MainPage(driver)

        with allure.step("Выполнить поиск по запросу 'Python'"):
            main_page.search("Python")

        with allure.step("Проверить, что результаты поиска отображены"):
            # Сделаем скриншот и прикрепим к отчету
            allure.attach(driver.get_screenshot_as_png(),
                          name="Search Results Screenshot",
                          attachment_type=allure.attachment_type.PNG)

            assert "Python" in driver.title