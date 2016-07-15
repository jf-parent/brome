import pytest  # noqa

from brome.webserver.server.settings import config
from brome.core.utils import DbSessionContext
from brome.model.testbatch import Testbatch


def test_log_stream_out_success(client):
    client.login('test@test.com')

    with DbSessionContext(config.get('MONGO_DATABASE_NAME')) as session:
        test_batch_id = session.query(Testbatch).first().get_uid()

    response = client.post_json(
        '/api/logstreamout',
        {
            'model': 'testbatch',
            'uid': test_batch_id,
            'skip': 0
        }
    )
    assert response.status_code == 200
    assert response.json['success']
    assert response.json['total'] == 10
    assert response.json['results'][0].strip() == 'line 1'
    assert response.json['results'][-1].strip() == 'line 10'


def test_log_stream_out_missing_params(client):
    client.login('test@test.com')

    # MISSING UID
    response = client.post_json(
        '/api/logstreamout',
        {
            'skip': 0,
            'model': 'testbatch'
        }
    )
    assert response.status_code == 200
    assert not response.json['success']
    assert response.json['error'] == 'InvalidRequestException'

    # MISSING MODEL
    response = client.post_json(
        '/api/logstreamout',
        {
            'uid': 'whatever',
            'skip': 0
        }
    )
    assert response.status_code == 200
    assert not response.json['success']
    assert response.json['error'] == 'InvalidRequestException'

    # MISSING SKIP
    response = client.post_json(
        '/api/logstreamout',
        {
            'uid': 'whatever',
            'model': 'testbatch'
        }
    )
    assert response.status_code == 200
    assert not response.json['success']
    assert response.json['error'] == 'InvalidRequestException'


def test_log_stream_out_wrong_model(client):
    client.login('test@test.com')

    with DbSessionContext(config.get('MONGO_DATABASE_NAME')) as session:
        test_batch_id = session.query(Testbatch).first().get_uid()

    response = client.post_json(
        '/api/logstreamout',
        {
            'model': 'test',
            'uid': test_batch_id,
            'skip': 0
        }
    )
    assert response.status_code == 200
    assert not response.json['success']
    assert response.json['error'] == 'InvalidRequestException'


def test_log_stream_out_wrong_uid(client):
    client.login('test@test.com')

    response = client.post_json(
        '/api/logstreamout',
        {
            'model': 'testbatch',
            'uid': '5788af3670fb051f6fedeaf2',
            'skip': 0
        }
    )
    assert response.status_code == 200
    assert not response.json['success']
    assert response.json['error'] == 'InvalidRequestException'


def test_log_stream_out_empty_log(client):
    client.login('test@test.com')

    with DbSessionContext(config.get('MONGO_DATABASE_NAME')) as session:
        test_batch_id = session.query(Testbatch).all()[1].get_uid()

    response = client.post_json(
        '/api/logstreamout',
        {
            'model': 'testbatch',
            'uid': test_batch_id,
            'skip': 0
        }
    )
    assert response.status_code == 200
    assert not response.json['success']
    assert response.json['error'] == 'InvalidRequestException'


def test_log_stream_out_skip_too_high_error(client):
    client.login('test@test.com')

    with DbSessionContext(config.get('MONGO_DATABASE_NAME')) as session:
        test_batch_id = session.query(Testbatch).first().get_uid()

    response = client.post_json(
        '/api/logstreamout',
        {
            'model': 'testbatch',
            'uid': test_batch_id,
            'skip': 20
        }
    )
    assert response.status_code == 200
    assert not response.json['success']
    assert response.json['error'] == 'ServerSideError'


def test_log_stream_out_skip(client):
    client.login('test@test.com')

    with DbSessionContext(config.get('MONGO_DATABASE_NAME')) as session:
        test_batch_id = session.query(Testbatch).first().get_uid()

    response = client.post_json(
        '/api/logstreamout',
        {
            'model': 'testbatch',
            'uid': test_batch_id,
            'skip': 2
        }
    )
    assert response.status_code == 200
    assert response.json['success']
    assert response.json['total'] == 10
    assert response.json['results'][0].strip() == 'line 3'
    assert response.json['results'][-1].strip() == 'line 10'
