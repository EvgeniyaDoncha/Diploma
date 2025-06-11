import requests
import allure
from jsonschema import validate
import json
import os

@allure.epic("API Tests")
@allure.feature("User API")
class TestUserApi:

    @allure.story("Get user by ID")
    @allure.description("Проверка получения пользователя по ID с валидацией схемы ответа")
    def test_get_user_by_id(self, base_api_url):
        user_id = 2
        url = f"{base_api_url}/users/{user_id}"

        response = requests.get(url)

        # Прикрепляем ответ в Allure
        allure.attach(
            response.text,
            name="Response JSON",
            attachment_type=allure.attachment_type.JSON
        )

        assert response.status_code == 200

        # Загружаем и прикрепляем JSON схему
        schema_path = os.path.join(os.path.dirname(__file__), "schemas", "user_schema.json")
        with open(schema_path, "r", encoding="utf-8") as f:
            schema_text = f.read()

        allure.attach(
            schema_text,
            name="User schema",
            attachment_type=allure.attachment_type.JSON
        )

        schema = json.loads(schema_text)
        validate(instance=response.json(), schema=schema)