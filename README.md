
## Описание

Покрываются ручки из API v1 и v2:

### API v1
- `POST /api/1/item` — создать объявление
- `GET /api/1/item/:id` — получить объявление по ID
- `GET /api/1/{sellerID}/item` — все объявления по продавцу
- `GET /api/1/statistic/:id` — статистика по объявлению

### API v2
- `GET /api/2/statistic/:id` — статистика (v2)
- `DELETE /api/2/item/:id` — удалить объявление

---


##  Установка и запуск

1. Клонируйте репозиторий или распакуйте архив:

```bash
cd qa-internship-tests
python3 -m venv venv
source venv/bin/activate   # Windows: venv\\Scripts\\activate
pip install -r requirements.txt
```
2. Запустите тесты:
```bash
pytest tests/
```

Вывод будет содержать информацию о каждом тесте: прошёл или нет.

Дополнительно

- Тест-кейсы: TESTCASES.md

- Баг-репорты: BUGS.md

Все тесты были составлены и реализованы вручную на основе документации и анализа Postman-коллекции.