import pytest
from http import HTTPStatus


async def test_get_all_films(make_get_request, get_all_data_elastic):
    """Тест запроса для всех фильмов"""

    # получаем все фильмы из elasticsearch
    all_films = await get_all_data_elastic("movies")

    response = await make_get_request("/films/movies/", {"page[number]": 1, "page[size]": 1000})
    assert response.status == HTTPStatus.OK

    assert len(response.body) + 2 == len(all_films)


async def test_get_by_id(make_get_request):
    """Тест проверяет работу получения по id в эндпоинте film"""

    response = await make_get_request("/films/c06dd0f4-d75d-4952-a81c-36837a30351b")
    film_data = {"id": "c06dd0f4-d75d-4952-a81c-36837a30351b", "title": "Frat Star", "imdb_rating": 3.5}
    # Проверка результата
    assert response.status == HTTPStatus.OK

    assert response.body == film_data


@pytest.mark.parametrize(
    "url, expected",
    [
        (["/films"], HTTPStatus.NOT_FOUND),
        (["/films/wrong-uuid"], HTTPStatus.NOT_FOUND),
        (["/films/movies/", {"page[size]": 0}], HTTPStatus.UNPROCESSABLE_ENTITY),
        (["/films/movies/", {"page[number]": 0}], HTTPStatus.UNPROCESSABLE_ENTITY),
    ],
)
async def test_validator(make_get_request, url, expected):
    """Тест корректной валидации форм"""
    response = await make_get_request(*url)
    assert response.status == expected


async def test_redis(make_get_request):
    """Тест кэширования"""
    # этот запрос сделан без удаления кэша
    response = await make_get_request("/films/movies/", {"page[number]": 1, "page[size]": 10}, False)
    assert response.status == HTTPStatus.OK

    response2 = await make_get_request("/films/movies/", {"page[number]": 1, "page[size]": 10})
    assert response.status == HTTPStatus.OK

    assert response.resp_speed > response2.resp_speed
