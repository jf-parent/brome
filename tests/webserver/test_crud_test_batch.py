from brome.webserver.server.settings import config
# NOTE this import will issue a warning from pytest
# because the class name start with Test*
from brome.model.testbatch import Testbatch
from brome.core.utils import (
    DbSessionContext
)

###############################################################################
# CREATE
###############################################################################


def test_crud_create_test_batch_not_allowed(client):
    client.login('admin@admin.com')

    response = client.post_json(
        '/api/crud',
        {
            'token': client.__token__,
            'actions': {
                'action': 'create',
                'model': 'testbatch',
                'data': {
                    'pid': 1337
                }
            }
        }
    )
    assert response.status_code == 200
    assert not response.json['success']
    assert response.json['error'] == 'NotAuthorizedException'

    client.login('test@test.com')

    response = client.post_json(
        '/api/crud',
        {
            'token': client.__token__,
            'actions': {
                'action': 'create',
                'model': 'testbatch',
                'data': {
                    'pid': 1337
                }
            }
        }
    )
    assert response.status_code == 200
    assert not response.json['success']
    assert response.json['error'] == 'NotAuthorizedException'


###############################################################################
# READ
###############################################################################

def test_crud_read_all_test_batch_as_a_normal_user(client):
    client.login('test@test.com')

    response = client.post_json(
        '/api/crud',
        {
            'token': client.__token__,
            'actions': {
                'action': 'read',
                'model': 'testbatch'
            }
        }
    )
    assert response.status_code == 200
    assert response.json['success']
    assert len(response.json['results']) == 2


def test_crud_read_all_test_batch_as_an_admin(client):
    client.login('admin@admin.com')

    response = client.post_json(
        '/api/crud',
        {
            'token': client.__token__,
            'actions': {
                'action': 'read',
                'model': 'testbatch'
            }
        }
    )
    assert response.status_code == 200
    assert response.json['success']
    assert len(response.json['results']) == 2


def test_crud_read_specific_test_batch(client):
    client.login('test@test.com')

    with DbSessionContext(config.get('MONGO_DATABASE_NAME')) as session:
        test_batch = session.query(Testbatch).first()

    response = client.post_json(
        '/api/crud',
        {
            'token': client.__token__,
            'actions': {
                'action': 'read',
                'model': 'testbatch',
                'uid': test_batch.get_uid()
            }
        }
    )
    assert response.status_code == 200
    assert response.json['success']
    assert type(response.json['results']) == list
    assert response.json['results'][0]['uid'] == test_batch.get_uid()
    assert response.json['total'] == 1
    assert len(response.json['results']) == 1


###############################################################################
# UPDATE
###############################################################################


def test_crud_update_test_batch_not_allowed(client):
    with DbSessionContext(config.get('MONGO_DATABASE_NAME')) as session:
        test_batch = session.query(Testbatch).first()

    client.login('admin@admin.com')

    response = client.post_json(
        '/api/crud',
        {
            'token': client.__token__,
            'actions': {
                'action': 'update',
                'model': 'testbatch',
                'uid': test_batch.get_uid(),
                'data': {
                    'pid': 1337
                }
            }
        }
    )
    assert response.status_code == 200
    assert not response.json['success']
    assert response.json['error'] == 'NotAuthorizedException'

    client.login('test@test.com')

    response = client.post_json(
        '/api/crud',
        {
            'token': client.__token__,
            'actions': {
                'action': 'update',
                'model': 'testbatch',
                'uid': test_batch.get_uid(),
                'data': {
                    'pid': 1337
                }
            }
        }
    )
    assert response.status_code == 200
    assert not response.json['success']
    assert response.json['error'] == 'NotAuthorizedException'


###############################################################################
# DELETE
###############################################################################


def test_crud_delete_not_allowed_for_normal_user(client):
    client.login('test@test.com')

    with DbSessionContext(config.get('MONGO_DATABASE_NAME')) as session:
        test_batch = session.query(Testbatch).first()

    response = client.post_json(
        '/api/crud',
        {
            'token': client.__token__,
            'actions': {
                'action': 'delete',
                'model': 'testbatch',
                'uid': test_batch.get_uid()
            }
        }
    )
    assert response.status_code == 200
    assert not response.json['success']
    assert response.json['error'] == 'NotAuthorizedException'


def test_crud_delete_test_batch_allowed_for_admin(client):
    client.login('admin@admin.com')

    with DbSessionContext(config.get('MONGO_DATABASE_NAME')) as session:
        test_batch = session.query(Testbatch).first()

    test_batch_uid = test_batch.get_uid()

    response = client.post_json(
        '/api/crud',
        {
            'token': client.__token__,
            'actions': {
                'action': 'delete',
                'model': 'testbatch',
                'uid': test_batch_uid
            }
        }
    )
    assert response.status_code == 200
    assert response.json['success']
    assert response.json['total'] == 1

    with DbSessionContext(config.get('MONGO_DATABASE_NAME')) as session:
        assert not session.query(Testbatch)\
            .filter(Testbatch.mongo_id == test_batch_uid).count()
