import requests
import allure
import jsonschema
from jsonschema import validate

@allure.story("Get user by ID")
@allure.description("Проверка получения пользователя по ID с валидацией схемы ответа")
def test_get_user_by_id():
    url = "https://reqres.in/api/users/2"
    response = requests.get(url)
    assert response.status_code == 200

    schema = {
        "type": "object",
        "properties": {
            "data": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "email": {"type": "string"},
                    "first_name": {"type": "string"},
                    "last_name": {"type": "string"},
                    "avatar": {"type": "string"}
                },
                "required": ["id", "email", "first_name", "last_name", "avatar"]
            },
            "support": {"type": "object"}
        },
        "required": ["data", "support"]
    }

    validate(instance=response.json(), schema=schema)