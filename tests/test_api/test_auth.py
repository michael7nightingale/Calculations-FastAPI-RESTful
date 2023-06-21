import pytest
from httpx import AsyncClient
from starlette import status

from app.resources.responses import USER_EXISTS, LOGIN_FAIL, NO_PERMISSIONS, USER_NOT_FOUND
from app.services.hasher import hash_password
from app.models.schemas.user import UserShow
from app.services.auth import decode_access_token, create_access_token
from ..conftest import get_auth_url


pytestmark = pytest.mark.asyncio


class TestAuth:

    user_data = {
        "username": "admin1231",
        "password": "d1-asad",
        "email": "asdka@gmail.ru",
        "first_name": "asda[sdfkasokda",
        "last_name": "asd[a0osd-oajdk"
    }

    async def test_register(self, client: AsyncClient):
        resp = await client.post(url=get_auth_url("register_user"), json=self.user_data)
        assert resp.status_code == status.HTTP_201_CREATED
        assert resp.json()['username'] == self.user_data['username']
        assert "id" in resp.json()
        assert resp.json()['email'] == self.user_data['email']

    async def test_already_existed(self, client: AsyncClient):
        await self.test_register(client)
        resp = await client.post(url=get_auth_url("register_user"), json=self.user_data)
        assert resp.status_code == 403
        assert resp.json() == {"detail": USER_EXISTS}

    async def test_register_fail(self, client: AsyncClient):
        data = self.user_data.copy()
        data.pop('username')
        resp = await client.post(url=get_auth_url("register_user"), json=data)
        assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert resp.json() == {'detail': [{'loc': ['body', 'username'], 'msg': 'field required', 'type': 'value_error.missing'}]}

    async def test_get_token(self, client: AsyncClient, user_data, token, user):
        login_data = {
            "username": user_data["username"],
            'password': user_data["password"]
        }
        resp = await client.post(url=get_auth_url('get_token'), json=login_data)
        assert resp.status_code == status.HTTP_200_OK
        access_token = resp.json()['access_token']
        assert access_token == token
        user_data = decode_access_token(access_token)
        assert user_data['username'] == login_data['username']

    async def test_get_token_fail(self, client: AsyncClient, user_data, user):
        login_data = {
            "username": user_data["username"],
            'password':  "asdplaposdjaosidhaopihdpiasujdpaisdujpaiouhsjda"
        }
        resp = await client.post(url=get_auth_url('get_token'), json=login_data)
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        assert resp.json() == {"detail": LOGIN_FAIL}

    async def test_get_token_fail_user_not_found(self, client: AsyncClient, user_data):
        login_data = {
            "username": user_data["username"],
            'password': user_data['password']
        }
        resp = await client.post(url=get_auth_url('get_token'), json=login_data)
        assert resp.status_code == status.HTTP_403_FORBIDDEN
        assert resp.json() == {"detail": USER_NOT_FOUND}

