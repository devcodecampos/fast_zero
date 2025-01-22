from http import HTTPStatus


def test_read_root_should_return_ok_and_helloworld(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Hello World'}
