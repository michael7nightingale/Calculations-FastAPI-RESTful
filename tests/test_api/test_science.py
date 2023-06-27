import pytest
from httpx import AsyncClient
from starlette import status

from ..conftest import get_science_url
from app.resources.responses import CATEGORY_NOT_FOUND, SCIENCE_NOT_FOUND


pytestmark = pytest.mark.asyncio


class TestScience:

    async def test_science_physics(self, client: AsyncClient):
        resp = await client.get(get_science_url("get_science", science_slug="physics"))
        content = resp.json()
        assert "title" in content
        assert content["title"] == "Физика"
        assert "content" in content

    async def test_science_mathem(self, client: AsyncClient):
        resp = await client.get(get_science_url("get_science", science_slug="mathem"))
        content = resp.json()
        assert "title" in content
        assert content["title"] == "Математика"
        assert "content" in content

    async def test_science_fail(self, client: AsyncClient):
        resp = await client.get(get_science_url("get_science", science_slug="bio"))
        assert resp.status_code == status.HTTP_404_NOT_FOUND
        assert resp.json() == {"detail": SCIENCE_NOT_FOUND}

    async def test_science_category_physics(self, client: AsyncClient):
        resp = await client.get(get_science_url("get_science_categories", science_slug="physics"))
        assert resp.status_code == status.HTTP_200_OK
        assert len(resp.json())

    async def test_science_category_mathem(self, client: AsyncClient):
        resp = await client.get(get_science_url("get_science_categories", science_slug="mathem"))
        assert resp.status_code == status.HTTP_200_OK
        assert len(resp.json())

    async def test_science_category_fail(self, client: AsyncClient):
        resp = await client.get(get_science_url("get_science_categories", science_slug="history"))
        assert resp.status_code == status.HTTP_404_NOT_FOUND
        assert resp.json() == {"detail": SCIENCE_NOT_FOUND}


class TestCategory:
    async def test_category1(self, client: AsyncClient):
        resp = await client.get(get_science_url("get_category", category_slug='dinamika'))
        assert resp.status_code == status.HTTP_200_OK
        content = resp.json()
        assert 'title' in content
        assert content['title'] == "Динамика"
        assert 'content' in content

    async def test_category2(self, client: AsyncClient):
        resp = await client.get(get_science_url("get_category", category_slug='equations'))
        assert resp.status_code == status.HTTP_200_OK
        content = resp.json()
        assert 'title' in content
        assert content['title'] == "Уравнения"
        assert 'content' in content

    async def test_category_fail(self, client: AsyncClient):
        resp = await client.get(get_science_url("get_category", category_slug='programming'))
        assert resp.status_code == status.HTTP_404_NOT_FOUND
        assert resp.json() == {"detail": CATEGORY_NOT_FOUND}

    async def test_category_formulas(self, client: AsyncClient):
        resp = await client.get(get_science_url("get_category_formulas", category_slug="dinamika"))
        assert resp.status_code == status.HTTP_200_OK
        assert len(resp.json())


# class TestSpecialCategories:
#
#     async def test_equation_single(self, client: AsyncClient):
#         data = {
#             "equation1": "8 * x - 2 = 10"
#         }
#         resp = await client.post(get_science_url("count_special_category",
#                                                  category_slug="equations"),
#                                  data=data)
#         print(resp.content)
#         assert resp.status_code == status.HTTP_200_OK
