import pytest
from httpx import AsyncClient

from ..conftest import get_science_url


pytestmark = pytest.mark.asyncio


class TestScience:

    def test_science(self, client: AsyncClient):
        resp = await client.get(get_science_url(""))


