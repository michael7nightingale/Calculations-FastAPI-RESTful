import pytest
from fastapi import status
from httpx import AsyncClient

from ..conftest import get_main_url

pytestmark = pytest.mark.asyncio


class TestMain:

    async def test_homepage(self, client: AsyncClient):
        resp = await client.get(url=get_main_url('homepage'))
        assert resp.status_code == status.HTTP_200_OK

    async def test_homepage_authenticated(self, authorized_client: AsyncClient):
        resp = await authorized_client.get(url=get_main_url('homepage'))
        assert resp.status_code == status.HTTP_200_OK