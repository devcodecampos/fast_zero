from http import HTTPStatus

from fast_zero.schemas import UserPublic
from fast_zero.security import create_access_token


def test_read_root_should_return_ok_and_helloworld(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Hello World'}


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'matheus',
            'email': 'matheus@example.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'matheus',
        'email': 'matheus@example.com',
        'id': 1,
    }


def test_create_user_should_return_bad_request_username_exists(client, user):
    response = client.post(
        '/users/',
        json={
            'username': user.username,
            'email': 'campos@example.com',
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Username already exists'}


def test_create_user_should_return_bad_request_email_exists(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'matheus',
            'email': user.email,
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email already exists'}


def test_read_users(client, token):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [{'id': 1, 'username': 'test', 'email': 'test@test.com'}]
    }


def test_read_users_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')

    assert response.json() == {'users': [user_schema]}


def test_read_user_by_id(client, user):
    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': user.username,
        'email': user.email,
        'id': user.id,
    }


def test_get_user_should_return_not_found(client):
    response = client.get('/users/2000')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_get_current_user_not_found(client):
    data = {'no-email': 'test'}
    token = create_access_token(data)

    response = client.delete(
        '/users/1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_get_current_user_does_not_exists(client):
    data = {'sub': 'test@test'}
    token = create_access_token(data)

    response = client.delete(
        '/users/1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'campos',
            'email': 'matheus@example.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'campos',
        'email': 'matheus@example.com',
        'id': user.id,
    }


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_get_token(client, user):
    response = client.post(
        '/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert 'access_token' in token
