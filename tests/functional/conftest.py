import time
from typing import Any, List

import aiohttp
import aioredis
import pytest
from elasticsearch import AsyncElasticsearch, exceptions

from functional.testdata.models import HTTPResponse
from functional.utils.settings import TEST_SETTINGS
from functional.utils.helpers import get_es_bulk_query
from functional.utils.wait_for_es_dub import wait_for_es
from functional.utils.wait_for_redis_dub import wait_for_redis


@pytest.fixture(scope='session')
async def es_client():
    await wait_for_es()
    client = AsyncElasticsearch(hosts='http://elasticsearch:9200')
    yield client
    await client.close()

@pytest.fixture(scope='function')
async def redis_client():
    await wait_for_redis()
    client = await aioredis.create_redis_pool((TEST_SETTINGS.redis_host, TEST_SETTINGS.redis_port), minsize=10, maxsize=20)
    yield client
    client.close()

@pytest.fixture(scope='function')
async def session():
    async with aiohttp.ClientSession() as session:
        yield session
    await session.close()

@pytest.fixture
def es_write_data(es_client: AsyncElasticsearch):
    async def inner(data: List[dict]):
        bulk_query = get_es_bulk_query(data, TEST_SETTINGS.es_index, TEST_SETTINGS.es_id_field)
        str_query = '\n'.join(bulk_query) + '\n'
        response = await es_client.bulk(str_query, refresh=True)
        if response['errors']:
            raise Exception('Ошибка записи данных в Elasticsearch')
    return inner

@pytest.fixture
async def make_get_request(session, redis_client):
    async def inner(method: str, params: dict = None, cleaning_redis: bool = True) -> HTTPResponse:
        params = params or {}
        # в боевых системах старайтесь так не делать!
        url = TEST_SETTINGS.service_url + '/api/v1' + method
        start = time.time()
        async with session.get(url, params=params) as response:
            #  очищаем кэш redis
            if cleaning_redis:
                await redis_client.delete(str(response.url))

            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
                url=response.url,
                resp_speed=(time.time()-start))

    return inner


@pytest.fixture
async def get_all_data_elastic(es_client):
    async def inner(index: str) -> Any:
        query = {
            "query": {
                "match_all": {}
            }
        }

        try:
            doc = await es_client.search(index=index, body=query, size=10000)
        except exceptions.NotFoundError:
            return []

        if not doc:
            return []
        result = doc["hits"]["hits"]

        if not result:
            return []

        return [data["_source"] for data in result]
    return inner

