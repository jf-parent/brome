import pytest  # noqa

from brome.webserver.server.settings import config
from brome.core.utils import DbSessionContext
from brome.model.testbatch import Testbatch
from brome.model.testinstance import Testinstance


def test_list_test_instances_success(client):
    client.login('test@test.com')

    with DbSessionContext(config.get('MONGO_DATABASE_NAME')) as session:
        test_batch_uid = session.query(Testbatch).first().get_uid()
        test_instance_uid = session.query(Testinstance)\
            .filter(Testinstance.test_batch_id == test_batch_uid)\
            .first().get_uid()

    response = client.post_json(
        '/api/testbatch',
        {
            'method': 'list_test_instances',
            'uid': test_batch_uid,
            'skip': 0,
            'limit': 10
        }
    )
    assert response.status_code == 200
    assert response.json['success']
    assert response.json['total'] == 2
    assert response.json['results'][0]['name'] == 'Test Instance 0'
    assert response.json['results'][0]['uid'] == test_instance_uid


def test_list_test_instances_success_skip(client):
    client.login('test@test.com')

    with DbSessionContext(config.get('MONGO_DATABASE_NAME')) as session:
        test_batch_uid = session.query(Testbatch).first().get_uid()
        test_instance_uid = session.query(Testinstance)\
            .filter(Testinstance.test_batch_id == test_batch_uid)\
            .all()[1].get_uid()

    response = client.post_json(
        '/api/testbatch',
        {
            'method': 'list_test_instances',
            'uid': test_batch_uid,
            'skip': 1,
            'limit': 10
        }
    )
    assert response.status_code == 200
    assert response.json['success']
    assert response.json['total'] == 2
    assert len(response.json['results']) == 1
    assert response.json['results'][0]['name'] == 'Test Instance 1'
    assert response.json['results'][0]['uid'] == test_instance_uid


def test_list_test_instances_success_limit(client):
    client.login('test@test.com')

    with DbSessionContext(config.get('MONGO_DATABASE_NAME')) as session:
        test_batch_uid = session.query(Testbatch).first().get_uid()
        test_instance_uid = session.query(Testinstance)\
            .filter(Testinstance.test_batch_id == test_batch_uid)\
            .first().get_uid()

    response = client.post_json(
        '/api/testbatch',
        {
            'method': 'list_test_instances',
            'uid': test_batch_uid,
            'skip': 0,
            'limit': 1
        }
    )
    assert response.status_code == 200
    assert response.json['success']
    assert response.json['total'] == 2
    assert len(response.json['results']) == 1
    assert response.json['results'][0]['name'] == 'Test Instance 0'
    assert response.json['results'][0]['uid'] == test_instance_uid


def test_api_test_batch_missing_params(client):
    client.login('test@test.com')

    # MISSING UID
    response = client.post_json(
        '/api/testbatch',
        {
            'skip': 0,
            'limit': 10,
            'method': 'list_test_instances'
        }
    )
    assert response.status_code == 200
    assert not response.json['success']
    assert response.json['error'] == 'InvalidRequestException'

    # MISSING LIMIT
    response = client.post_json(
        '/api/testbatch',
        {
            'uid': 'whatever',
            'method': 'list_test_instances',
            'skip': 0
        }
    )
    assert response.status_code == 200
    assert not response.json['success']
    assert response.json['error'] == 'InvalidRequestException'

    # MISSING SKIP
    response = client.post_json(
        '/api/testbatch',
        {
            'uid': 'whatever',
            'limit': 10,
            'method': 'list_test_instances'
        }
    )
    assert response.status_code == 200
    assert not response.json['success']
    assert response.json['error'] == 'InvalidRequestException'

    # MISSING METHOD
    response = client.post_json(
        '/api/testbatch',
        {
            'uid': 'whatever',
            'limit': 10,
            'skip': 2
        }
    )
    assert response.status_code == 200
    assert not response.json['success']
    assert response.json['error'] == 'InvalidRequestException'


def test_api_test_batch_wrong_method(client):
    client.login('test@test.com')

    with DbSessionContext(config.get('MONGO_DATABASE_NAME')) as session:
        test_batch_uid = session.query(Testbatch).first().get_uid()

    response = client.post_json(
        '/api/testbatch',
        {
            'method': 'wrong',
            'limit': 10,
            'uid': test_batch_uid,
            'skip': 0
        }
    )
    assert response.status_code == 200
    assert not response.json['success']
    assert response.json['error'] == 'InvalidRequestException'
