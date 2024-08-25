from fastapi.testclient import TestClient

from main import app


client = TestClient(app)
recipe_in: dict = {
    'title': 'test_title',
    'description': 'test_description',
    'ingredients': 'test_ingredients',
    'cooking_time': 1.1,
}
cur_prefix: int = 0


def _add_prefix():
    """Функция добавляет префикс к полям self.test_detailed_recipe,
    чтобы добавлять уникальные значение при тестировании
    """
    global cur_prefix
    prefix: str = f'_{cur_prefix}'
    recipe_in['title'] += prefix
    recipe_in['description'] += prefix
    recipe_in['ingredients'] += prefix
    cur_prefix += 1


def test_add_new_recipe_and_return_same_recipe():
    """Unit тест. Проверяет, что при отправке корректной формы,
     возвращает отправленный json, код 200"""
    _add_prefix()

    response = client.post('/recipes', json=recipe_in)
    assert response.status_code == 200

    response_json = response.json()
    response_json.pop('recipe_id')
    assert response_json == recipe_in


def test_added_recipe_in_bd():
    """Unit тест. Проверяет, что при отправке корректной формы,
     рецепт сохраняется в бд"""
    _add_prefix()
    # Отправим рецепт в бд через POST
    response_post = client.post('/recipes', json=recipe_in)
    response_post_json = response_post.json()
    recipe_id: int = response_post_json.get('recipe_id')

    # получим рецепт из бд через GET и id рецепта
    response_get = client.get(f'/recipes/{recipe_id}')
    response_get_json = response_get.json()
    assert response_post_json == response_get_json


def test_negative_post_invalid_form():
    """Негативный unit тест. Проверка отправки невалидной формы"""
    response = client.post('/recipes', json={'smth': 'smb'})
    assert response.status_code == 422


def test_negative_recipe_not_found():
    """Негативный unit тест. Проверяет, что если запросить рецепт по id, которого нет в бд, то вернет 404 код"""
    response = client.get('/recipes/1000')
    assert response.status_code == 404


def test_get_all_recipes():
    """Unit тест. Проверяет, что endpoint GET /recipes работает и возвращает 200 код"""
    response = client.get('/recipes')
    assert response.status_code == 200
