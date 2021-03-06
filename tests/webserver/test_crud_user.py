from brome.core.settings import BROME_CONFIG
from brome.core.utils import DbSessionContext
from brome.model.user import User

###############################################################################
# CREATE
###############################################################################


def test_crud_create_not_allowed_for_normal_user(client):
    client.login('test@test.com')

    response = client.post_json(
        '/api/crud',
        {
            'token': client.__token__,
            'actions': {
                'action': 'create',
                'model': 'user',
                'data': {
                    'name': 'test',
                    'email': 'test1@test.com',
                    'password': '123456'
                }
            }
        }
    )
    assert response.status_code == 200
    assert not response.json['success']
    assert response.json['error'] == 'NotAuthorizedException'


def test_crud_create_missing_data(client):
    client.login('admin@admin.com')

    # Missing name
    response = client.post_json(
        '/api/crud',
        {
            'token': client.__token__,
            'actions': {
                'action': 'create',
                'model': 'user',
                'data': {
                    'email': 'test1@test.com',
                    'password': '123456'
                }
            }
        }
    )
    assert response.status_code == 200
    assert not response.json['success']
    assert response.json['error'] == 'InvalidNameException'

    # Missing email
    response = client.post_json(
        '/api/crud',
        {
            'token': client.__token__,
            'actions': {
                'action': 'create',
                'model': 'user',
                'data': {
                    'name': 'test',
                    'password': '123456'
                }
            }
        }
    )
    assert response.status_code == 200
    assert not response.json['success']
    assert response.json['error'] == 'InvalidEmailException'

    # Missing password
    response = client.post_json(
        '/api/crud',
        {
            'token': client.__token__,
            'actions': {
                'action': 'create',
                'model': 'user',
                'data': {
                    'name': 'test',
                    'email': 'test1@test.com'
                }
            }
        }
    )
    assert response.status_code == 200
    assert not response.json['success']
    assert response.json['error'] == 'InvalidPasswordException'


def test_crud_create_invalid_data(client):
    client.login('admin@admin.com')

    # Invalid name
    response = client.post_json(
        '/api/crud',
        {
            'token': client.__token__,
            'actions': {
                'action': 'create',
                'model': 'user',
                'data': {
                    'email': 'test1@test.com',
                    'name': 'a',
                    'password': '123456'
                }
            }
        }
    )
    assert response.status_code == 200
    assert not response.json['success']
    assert response.json['error'] == 'InvalidNameException'

    # Invalid email
    response = client.post_json(
        '/api/crud',
        {
            'token': client.__token__,
            'actions': {
                'action': 'create',
                'model': 'user',
                'data': {
                    'name': 'test',
                    'email': 'test',
                    'password': '123456'
                }
            }
        }
    )
    assert response.status_code == 200
    assert not response.json['success']
    assert response.json['error'] == 'InvalidEmailException'

    # Invalid password
    response = client.post_json(
        '/api/crud',
        {
            'token': client.__token__,
            'actions': {
                'action': 'create',
                'model': 'user',
                'data': {
                    'name': 'test',
                    'email': 'test1@test.com',
                    'password': 'inv'
                }
            }
        }
    )
    assert response.status_code == 200
    assert not response.json['success']
    assert response.json['error'] == 'InvalidPasswordException'


def test_crud_create_success(client):
    client.login('admin@admin.com')

    response = client.post_json(
        '/api/crud',
        {
            'token': client.__token__,
            'actions': {
                'action': 'create',
                'model': 'user',
                'data': {
                    'name': 'test',
                    'email': 'test1@test.com',
                    'password': '123456'
                }
            }
        }
    )
    assert response.status_code == 200
    assert response.json['success']
    assert response.json['results'][0]['name'] == 'test'
    assert response.json['results'][0]['email'] == 'test1@test.com'  # noqa

###############################################################################
# READ
###############################################################################


def test_crud_read_for_normal_user(client):
    user = client.login('test@test.com')

    with DbSessionContext(BROME_CONFIG['database']['mongo_database_name']) as session:  # noqa
        admin = session.query(User) \
                .filter(User.email == 'admin@admin.com').one()

    response = client.post_json(
        '/api/crud',
        {
            'token': client.__token__,
            'actions': {
                'action': 'read',
                'model': 'user',
                'uid': user.get_uid()
            }
        }
    )
    assert response.status_code == 200
    assert response.json['success']
    assert response.json['results'][0]['name'] == 'test'
    assert response.json['total'] == 1

    response = client.post_json(
        '/api/crud',
        {
            'token': client.__token__,
            'actions': {
                'action': 'read',
                'model': 'user',
                'uid': admin.get_uid()
            }
        }
    )
    assert response.status_code == 200
    assert not response.json['success']
    assert response.json['error'] == 'NotAuthorizedException'


def test_crud_read_specific_user_with_admin(client):
    client.login('admin@admin.com')

    with DbSessionContext(BROME_CONFIG['database']['mongo_database_name']) as session:  # noqa
        user = session.query(User) \
                .filter(User.email == 'test@test.com').one()

    response = client.post_json(
        '/api/crud',
        {
            'token': client.__token__,
            'actions': {
                'action': 'read',
                'model': 'user',
                'uid': user.get_uid()
            }
        }
    )
    assert response.status_code == 200
    assert response.json['success']
    assert len(response.json['results']) == 1
    assert response.json['results'][0]['name'] == 'test'


def test_crud_read_skip_and_limit_admin(client):
    client.login('admin@admin.com')

    response = client.post_json(
        '/api/crud',
        {
            'token': client.__token__,
            'actions': {
                'action': 'read',
                'model': 'user',
                'limit': 2,
                'skip': 3
            }
        }
    )
    assert response.status_code == 200
    assert response.json['success']
    assert len(response.json['results']) == 1
    assert response.json['results'][0]['name'] == 'disabled'


def test_crud_read_limit_admin(client):
    client.login('admin@admin.com')

    response = client.post_json(
        '/api/crud',
        {
            'token': client.__token__,
            'actions': {
                'action': 'read',
                'model': 'user',
                'limit': 2
            }
        }
    )
    assert response.status_code == 200
    assert response.json['success']
    assert len(response.json['results']) == 2
    assert response.json['results'][0]['name'] == 'test'


def test_crud_read_skip_admin(client):
    client.login('admin@admin.com')

    response = client.post_json(
        '/api/crud',
        {
            'token': client.__token__,
            'actions': {
                'action': 'read',
                'model': 'user',
                'skip': 2
            }
        }
    )
    assert response.status_code == 200
    assert response.json['success']
    assert len(response.json['results']) == 2
    assert response.json['results'][0]['name'] == 'admin'


def test_crud_read_admin(client):
    client.login('admin@admin.com')

    response = client.post_json(
        '/api/crud',
        {
            'token': client.__token__,
            'actions': {
                'action': 'read',
                'model': 'user',
            }
        }
    )
    assert response.status_code == 200
    assert response.json['success']
    assert len(response.json['results']) == 4


###############################################################################
# UPDATE
###############################################################################


def test_crud_update_normal_user_not_authorized(client):
    client.login('test@test.com')

    with DbSessionContext(BROME_CONFIG['database']['mongo_database_name']) as session:  # noqa
        admin = session.query(User) \
            .filter(User.email == 'admin@admin.com').one()

    response = client.post_json(
        '/api/crud',
        {
            'token': client.__token__,
            'actions': {
                'action': 'update',
                'model': 'user',
                'uid': admin.get_uid(),
                'data': {
                    'name': 'new_name'
                }
            }
        }
    )
    assert response.status_code == 200
    assert not response.json['success']
    assert response.json['error'] == 'NotAuthorizedException'


def test_crud_update_admin_other_user(client):
    client.login('admin@admin.com')

    with DbSessionContext(BROME_CONFIG['database']['mongo_database_name']) as session:  # noqa
        user = session.query(User) \
            .filter(User.email == 'test@test.com').one()

    response = client.post_json(
        '/api/crud',
        {
            'token': client.__token__,
            'actions': {
                'action': 'update',
                'model': 'user',
                'uid': user.get_uid(),
                'data': {
                    'name': 'new_name'
                }
            }
        }
    )
    assert response.status_code == 200
    assert response.json['success']

    with DbSessionContext(BROME_CONFIG['database']['mongo_database_name']) as session:  # noqa
        user = session.query(User) \
            .filter(User.email == 'test@test.com').one()
        assert user.name == 'new_name'


def test_crud_update_email(client):
    user = client.login('test@test.com')

    response = client.post_json(
        '/api/crud',
        {
            'token': client.__token__,
            'actions': {
                'action': 'update',
                'model': 'user',
                'uid': user.get_uid(),
                'data': {
                    'name': 'new_name',
                    'email': 'newemail@newemail.com'
                }
            }
        }
    )
    assert response.status_code == 200
    assert response.json['success']


def test_crud_update_invalid_data(client):
    user = client.login('test@test.com')

    # INVALID EMAIL
    response = client.post_json(
        '/api/crud',
        {
            'token': client.__token__,
            'actions': {
                'action': 'update',
                'model': 'user',
                'uid': user.get_uid(),
                'data': {
                    'email': 'invalid'
                }
            }
        }
    )
    assert response.status_code == 200
    assert not response.json['success']
    assert response.json['error'] == 'InvalidEmailException'

    # INVALID NAME
    response = client.post_json(
        '/api/crud',
        {
            'token': client.__token__,
            'actions': {
                'action': 'update',
                'model': 'user',
                'uid': user.get_uid(),
                'data': {
                    'name': 'i',
                    'email': 'test@test.com'
                }
            }
        }
    )
    assert response.status_code == 200
    assert not response.json['success']
    assert response.json['error'] == 'InvalidNameException'


def test_crud_update_sanitize_data(client):
    user = client.login('test@test.com')

    # CHANGING ROLE IS NOT ALLOWED FOR NORMAL USER
    response = client.post_json(
        '/api/crud',
        {
            'token': client.__token__,
            'actions': {
                'action': 'update',
                'model': 'user',
                'uid': user.get_uid(),
                'data': {
                    'role': 'admin'
                }
            }
        }
    )
    assert response.status_code == 200
    assert response.json['success']

    with DbSessionContext(BROME_CONFIG['database']['mongo_database_name']) as session:  # noqa
        user = session.query(User) \
            .filter(User.email == 'test@test.com').one()
        assert user.role == 'user'


def test_crud_update_name_with_same_email(client):
    user = client.login('test@test.com')

    response = client.post_json(
        '/api/crud',
        {
            'token': client.__token__,
            'actions': {
                'action': 'update',
                'model': 'user',
                'uid': user.get_uid(),
                'data': {
                    'name': 'new_name',
                    'email': 'test@test.com'
                }
            }
        }
    )
    assert response.status_code == 200
    assert response.json['success']

    with DbSessionContext(BROME_CONFIG['database']['mongo_database_name']) as session:  # noqa
        user = session.query(User) \
            .filter(User.email == 'test@test.com').one()
        assert user.name == 'new_name'


def test_crud_update_sanitize_data_admin(client):
    client.login('admin@admin.com')

    with DbSessionContext(BROME_CONFIG['database']['mongo_database_name']) as session:  # noqa
        user = session.query(User) \
            .filter(User.email == 'test@test.com').one()

    # CHANGING ROLE IS ALLOWED FOR ADMIN
    response = client.post_json(
        '/api/crud',
        {
            'token': client.__token__,
            'actions': {
                'action': 'update',
                'model': 'user',
                'uid': user.get_uid(),
                'data': {
                    'role': 'admin'
                }
            }
        }
    )
    assert response.status_code == 200
    assert response.json['success']

    with DbSessionContext(BROME_CONFIG['database']['mongo_database_name']) as session:  # noqa
        user = session.query(User) \
            .filter(User.email == 'test@test.com').one()
        assert user.role == 'admin'


def test_crud_update_new_password_success(client):
    user = client.login('test@test.com')

    response = client.post_json(
        '/api/crud',
        {
            'token': client.__token__,
            'actions': {
                'action': 'update',
                'model': 'user',
                'uid': user.get_uid(),
                'data': {
                    'old_password': '123456',
                    'new_password': '1asdf!!'
                }
            }
        }
    )
    assert response.status_code == 200
    assert response.json['success']

    response = client.post_json(
        '/api/logout',
        {
            'token': client.__token__
        }
    )
    assert response.status_code == 200

    response = client.post_json(
        '/api/login',
        {
            'email': 'test@test.com',
            'password': '123456',
            'token': client.__token__
        }
    )
    assert response.status_code == 200
    assert not response.json['success']

    response = client.post_json(
        '/api/login',
        {
            'email': 'test@test.com',
            'password': '1asdf!!',
            'token': client.__token__
        }
    )
    assert response.status_code == 200
    assert response.json['success']


def test_crud_update_new_password_invalid(client):
    user = client.login('test@test.com')

    response = client.post_json(
        '/api/crud',
        {
            'token': client.__token__,
            'actions': {
                'action': 'update',
                'model': 'user',
                'uid': user.get_uid(),
                'data': {
                    'old_password': '123456',
                    'new_password': '1'
                }
            }
        }
    )
    assert response.status_code == 200
    assert not response.json['success']
    assert response.json['error'] == 'InvalidPasswordException'


def test_crud_update_new_password_old_password_incorrect(client):
    user = client.login('test@test.com')

    response = client.post_json(
        '/api/crud',
        {
            'token': client.__token__,
            'actions': {
                'action': 'update',
                'model': 'user',
                'uid': user.get_uid(),
                'data': {
                    'old_password': '1111111',
                    'new_password': '1asdf!!'
                }
            }
        }
    )
    assert response.status_code == 200
    assert not response.json['success']
    assert response.json['error'] == 'WrongEmailOrPasswordException'


def test_crud_update_new_password_missing_old_password(client):
    user = client.login('test@test.com')

    response = client.post_json(
        '/api/crud',
        {
            'token': client.__token__,
            'actions': {
                'action': 'update',
                'model': 'user',
                'uid': user.get_uid(),
                'data': {
                    'new_password': '1asdf!!'
                }
            }
        }
    )
    assert response.status_code == 200
    assert not response.json['success']
    assert response.json['error'] == 'InvalidRequestException'


###############################################################################
# DELETE
###############################################################################


def test_crud_delete_not_allowed_for_normal_user(client):
    user = client.login('test@test.com')

    response = client.post_json(
        '/api/crud',
        {
            'token': client.__token__,
            'actions': {
                'action': 'delete',
                'model': 'user',
                'uid': user.get_uid()
            }
        }
    )
    assert response.status_code == 200
    assert not response.json['success']
    assert response.json['error'] == 'NotAuthorizedException'


def test_crud_delete_admin_success(client):
    client.login('admin@admin.com')

    with DbSessionContext(BROME_CONFIG['database']['mongo_database_name']) as session:  # noqa
        user = session.query(User) \
                .filter(User.email == 'test@test.com').one()

    user_uid = user.get_uid()

    response = client.post_json(
        '/api/crud',
        {
            'token': client.__token__,
            'actions': {
                'action': 'delete',
                'model': 'user',
                'uid': user_uid
            }
        }
    )
    assert response.status_code == 200
    assert response.json['success']
    assert response.json['total'] == 1

    with DbSessionContext(BROME_CONFIG['database']['mongo_database_name']) as session:  # noqa
        assert not session.query(User) \
                .filter(User.email == 'test@test.com').count()


def test_crud_delete_all_user_disabled_admin_success(client):
    client.login('admin@admin.com')

    response = client.post_json(
        '/api/crud',
        {
            'token': client.__token__,
            'actions': {
                'action': 'delete',
                'model': 'user',
                'filters': {
                    'enable': False
                }
            }
        }
    )
    assert response.status_code == 200
    assert response.json['success']
    assert response.json['total'] == 1

    with DbSessionContext(BROME_CONFIG['database']['mongo_database_name']) as session:  # noqa
        assert not session.query(User) \
                .filter(User.enable == False).count()  # noqa
