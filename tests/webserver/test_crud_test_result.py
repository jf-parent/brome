from brome.core.settings import BROME_CONFIG
# NOTE this import will issue a warning from pytest
# because the class name start with Test*
from brome.model.testresult import Testresult
from brome.model.testbatch import Testbatch
from brome.core.utils import (
    DbSessionContext
)

###############################################################################
# CREATE
###############################################################################


def test_crud_create_test_result_not_allowed(client):
    client.login('admin@admin.com')

    response = client.post_json(
        '/api/crud',
        {
            'token': client.__token__,
            'actions': {
                'action': 'create',
                'model': 'testresult',
                'data': {
                    'title': 'test'
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
                'model': 'testresult',
                'data': {
                    'title': 'test'
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

def test_crud_read_all_test_result_as_a_normal_user(client):
    client.login('test@test.com')

    response = client.post_json(
        '/api/crud',
        {
            'token': client.__token__,
            'actions': {
                'action': 'read',
                'model': 'testresult'
            }
        }
    )
    assert response.status_code == 200
    assert response.json['success']
    assert len(response.json['results']) == 10


def test_crud_read_all_test_result_as_an_admin(client):
    client.login('admin@admin.com')

    response = client.post_json(
        '/api/crud',
        {
            'token': client.__token__,
            'actions': {
                'action': 'read',
                'model': 'testresult'
            }
        }
    )
    assert response.status_code == 200
    assert response.json['success']
    assert len(response.json['results']) == 10


def test_crud_read_specific_test_result_from_test_batch(client):
    client.login('test@test.com')

    with DbSessionContext(BROME_CONFIG['database']['mongo_database_name']) as session:  # noqa
        test_batch = session.query(Testbatch).first()

    response = client.post_json(
        '/api/crud',
        {
            'token': client.__token__,
            'actions': {
                'action': 'read',
                'model': 'testresult',
                'filters': {
                    'test_batch_id': test_batch.get_uid()
                }
            }
        }
    )
    assert response.status_code == 200
    assert response.json['success']
    assert type(response.json['results']) == list
    assert response.json['results'][0]['test_batch_id'] == test_batch.get_uid()
    assert response.json['total'] == 5
    assert len(response.json['results']) == 5


def test_crud_read_specific_test_result(client):
    client.login('test@test.com')

    with DbSessionContext(BROME_CONFIG['database']['mongo_database_name']) as session:  # noqa
        test_result = session.query(Testresult).first()

    response = client.post_json(
        '/api/crud',
        {
            'token': client.__token__,
            'actions': {
                'action': 'read',
                'model': 'testresult',
                'uid': test_result.get_uid()
            }
        }
    )
    assert response.status_code == 200
    assert response.json['success']
    assert type(response.json['results']) == list
    assert response.json['results'][0]['uid'] == test_result.get_uid()
    assert response.json['total'] == 1
    assert len(response.json['results']) == 1


###############################################################################
# UPDATE
###############################################################################


def test_crud_update_test_result_not_allowed(client):
    with DbSessionContext(BROME_CONFIG['database']['mongo_database_name']) as session:  # noqa
        test_result = session.query(Testresult).first()

    client.login('admin@admin.com')

    response = client.post_json(
        '/api/crud',
        {
            'token': client.__token__,
            'actions': {
                'action': 'update',
                'model': 'testresult',
                'uid': test_result.get_uid(),
                'data': {
                    'title': 'test'
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
                'model': 'testresult',
                'uid': test_result.get_uid(),
                'data': {
                    'title': 'test'
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


def test_crud_delete_not_allowed(client):
    client.login('test@test.com')

    with DbSessionContext(BROME_CONFIG['database']['mongo_database_name']) as session:  # noqa
        test_result = session.query(Testresult).first()

    response = client.post_json(
        '/api/crud',
        {
            'token': client.__token__,
            'actions': {
                'action': 'delete',
                'model': 'testresult',
                'uid': test_result.get_uid()
            }
        }
    )
    assert response.status_code == 200
    assert not response.json['success']
    assert response.json['error'] == 'NotAuthorizedException'

    client.login('admin@admin.com')

    response = client.post_json(
        '/api/crud',
        {
            'token': client.__token__,
            'actions': {
                'action': 'delete',
                'model': 'testresult',
                'uid': test_result.get_uid()
            }
        }
    )
    assert response.status_code == 200
    assert not response.json['success']
    assert response.json['error'] == 'NotAuthorizedException'
