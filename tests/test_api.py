import requests
import random
import pytest

BASE_URL = "https://qa-internship.avito.com"
SELLER_ID = random.randint(111111, 999999)

# Хелпер для создания объявления
def create_item(seller_id=None):
    data = {
        "sellerID": seller_id or SELLER_ID,
        "name": "Test Product",
        "price": 1000,
        "statistics": {
            "likes": 10,
            "viewCount": 100,
            "contacts": 3
        }
    }
    response = requests.post(f"{BASE_URL}/api/1/item", json=data)
    return response

# TC01: Успешное создание объявления
def test_create_item_success():
    response = create_item()
    assert response.status_code == 200
    data = response.json()
    assert data["sellerId"] == SELLER_ID
    assert data["name"] == "Test Product"

# TC02: Создание без name
def test_create_item_without_name():
    data = {
        "sellerID": SELLER_ID,
        "price": 1000,
        "statistics": {
            "likes": 10,
            "viewCount": 100,
            "contacts": 3
        }
    }
    response = requests.post(f"{BASE_URL}/api/1/item", json=data)
    assert response.status_code == 400

# TC03: Невалидный price (строка вместо числа)
def test_create_item_invalid_price():
    data = {
        "sellerID": SELLER_ID,
        "name": "Test",
        "price": "тысяча",
        "statistics": {
            "likes": 10,
            "viewCount": 100,
            "contacts": 3
        }
    }
    response = requests.post(f"{BASE_URL}/api/1/item", json=data)
    assert response.status_code == 400

# TC04: Дублирование sellerID с разными name/price
def test_create_multiple_items_same_seller():
    response1 = create_item()
    response2 = create_item()
    assert response1.status_code == 200
    assert response2.status_code == 200

# TC05: Получить объявление по ID
def test_get_item_by_id():
    response = create_item()
    item_id = response.json()["id"]
    get_response = requests.get(f"{BASE_URL}/api/1/item/{item_id}")
    assert get_response.status_code == 200
    data = get_response.json()[0]
    assert data["id"] == item_id

# TC06: Получить по несуществующему ID
def test_get_item_not_found():
    response = requests.get(f"{BASE_URL}/api/1/item/nonexistent")
    assert response.status_code == 404

# TC07: Получить с некорректным ID
def test_get_item_invalid_id():
    response = requests.get(f"{BASE_URL}/api/1/item/%%%")
    assert response.status_code in [400, 404]  # зависит от обработки сервером

# TC08: Получить все объявления по sellerID
def test_get_all_items_by_seller():
    create_item()
    response = requests.get(f"{BASE_URL}/api/1/{SELLER_ID}/item")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# TC09: По несуществующему sellerID
def test_get_items_unknown_seller():
    response = requests.get(f"{BASE_URL}/api/1/9999999/item")
    assert response.status_code == 200
    assert response.json() == []

# TC10: Невалидный sellerID
def test_get_items_invalid_seller():
    response = requests.get(f"{BASE_URL}/api/1/abc/item")
    assert response.status_code == 400

# TC11/TC12: Статистика по объявлению v1 и v2
def test_get_statistic_by_id():
    response = create_item()
    item_id = response.json()["id"]
    for version in ["1", "2"]:
        resp = requests.get(f"{BASE_URL}/api/{version}/statistic/{item_id}")
        assert resp.status_code == 200
        stats = resp.json()[0]
        assert "likes" in stats and "viewCount" in stats and "contacts" in stats

# TC13: Успешное удаление объявления
def test_delete_item():
    response = create_item()
    item_id = response.json()["id"]
    delete_response = requests.delete(f"{BASE_URL}/api/2/item/{item_id}")
    assert delete_response.status_code == 200

# TC14: Удаление несуществующего объявления
def test_delete_nonexistent_item():
    response = requests.delete(f"{BASE_URL}/api/2/item/nonexistent")
    assert response.status_code == 404

# TC15: Удаление с невалидным ID
def test_delete_invalid_item():
    response = requests.delete(f"{BASE_URL}/api/2/item/@@@")
    assert response.status_code in [400, 404]
