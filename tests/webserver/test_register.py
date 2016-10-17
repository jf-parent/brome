from brome.core.settings import BROME_CONFIG
from brome.core.utils import DbSessionContext
from brome.model.user import User, NAME_MAX_LEN


DEFAULT_EMAIL = 'test.new@test.com'
DEFAULT_NAME = 'test.new'
DEFAULT_PASSWORD = '123456'


def test_register_empty_post(client):
    response = client.post_json('/api/register')
    assert response.status_code == 200
    assert response.json == {
        'success': False,
        'error': 'InvalidRequestException'
    }


def test_register_without_token(client):
    response = client.post_json(
        '/api/register',
        {
            'email': 'test@test.com',
            'name': 'test',
            'registration_token': 'registration_token',
            'password': '123456'
        }
    )
    assert response.status_code == 200
    assert response.json == {'success': False, 'error': 'CSRFMismatch'}


def test_register_with_wrong_token(client):
    response = client.post_json(
        '/api/register',
        {
            'email': DEFAULT_EMAIL,
            'name': DEFAULT_NAME,
            'password': DEFAULT_PASSWORD,
            'registration_token': 'registration_token',
            'token': '1337'
        }
    )
    assert response.status_code == 200
    assert response.json == {'success': False, 'error': 'CSRFMismatch'}


def test_register_name_too_short(client):
    email = DEFAULT_EMAIL
    name = 'I'
    password = DEFAULT_PASSWORD
    response = client.post_json(
        '/api/register',
        {
            'email': email,
            'name': name,
            'password': password,
            'registration_token': 'registration_token',
            'token': client.__token__
        }
    )
    assert response.status_code == 200
    assert response.json == {'success': False, 'error': 'InvalidNameException'}


def test_register_name_too_long(client):
    email = DEFAULT_EMAIL
    name = 'I' * (NAME_MAX_LEN + 1)
    password = DEFAULT_PASSWORD
    response = client.post_json(
        '/api/register',
        {
            'email': email,
            'name': name,
            'password': password,
            'registration_token': 'registration_token',
            'token': client.__token__
        }
    )
    assert response.status_code == 200
    assert response.json == {'success': False, 'error': 'InvalidNameException'}


def test_register_password_too_short(client):
    email = DEFAULT_EMAIL
    name = DEFAULT_NAME
    password = '1'
    response = client.post_json(
        '/api/register',
        {
            'email': email,
            'name': name,
            'password': password,
            'registration_token': 'registration_token',
            'token': client.__token__
        }
    )
    assert response.status_code == 200
    assert response.json == \
        {'success': False, 'error': 'InvalidPasswordException'}


def test_register_email_already_exist(client):
    email = 'test@test.com'
    name = DEFAULT_NAME
    password = DEFAULT_PASSWORD
    response = client.post_json(
        '/api/register',
        {
            'email': email,
            'name': name,
            'registration_token': 'registration_token',
            'password': password,
            'token': client.__token__
        }
    )
    assert response.status_code == 200
    assert response.json == \
        {'success': False, 'error': 'EmailAlreadyExistsException'}


def test_register_with_empty_email(client):
    email = ''
    name = DEFAULT_NAME
    password = DEFAULT_PASSWORD
    response = client.post_json(
        '/api/register',
        {
            'email': email,
            'name': name,
            'registration_token': 'registration_token',
            'password': password,
            'token': client.__token__
        }
    )
    assert response.status_code == 200
    assert response.json == \
        {'success': False, 'error': 'InvalidEmailException'}


def test_register_with_invalid_email(client):
    email = 'invalid'
    name = DEFAULT_NAME
    password = DEFAULT_PASSWORD
    response = client.post_json(
        '/api/register',
        {
            'email': email,
            'name': name,
            'registration_token': 'registration_token',
            'password': password,
            'token': client.__token__
        }
    )
    assert response.status_code == 200
    assert response.json == \
        {'success': False, 'error': 'InvalidEmailException'}


def test_register_with_right_token(client):
    response = client.post_json(
        '/api/register',
        {
            'email': DEFAULT_EMAIL,
            'name': DEFAULT_NAME,
            'registration_token': 'registration_token',
            'password': DEFAULT_PASSWORD,
            'token': client.__token__
        }
    )
    assert response.status_code == 200
    assert response.json['success']

    with DbSessionContext(BROME_CONFIG['database']['mongo_database_name']) as session:  # noqa
        user_query = session.query(User) \
            .filter(User.email == DEFAULT_EMAIL)

        assert user_query.count() == 1

        user = user_query.one()
        assert user.email == DEFAULT_EMAIL  # Obviously
        assert user.name == DEFAULT_NAME
        assert user.enable
        assert user.role == 'user'


def test_register_return_correct_user(client):
    response = client.post_json(
        '/api/register',
        {
            'email': DEFAULT_EMAIL,
            'name': DEFAULT_NAME,
            'registration_token': 'registration_token',
            'password': DEFAULT_PASSWORD,
            'token': client.__token__
        }
    )
    assert response.status_code == 200
    assert response.json['success']
    assert response.json['user']['email'] == DEFAULT_EMAIL
    assert response.json['user']['name'] == DEFAULT_NAME


def test_register_logout_login(client):
    # REGISTER
    response = client.post_json(
        '/api/register',
        {
            'email': DEFAULT_EMAIL,
            'name': DEFAULT_NAME,
            'registration_token': 'registration_token',
            'password': DEFAULT_PASSWORD,
            'token': client.__token__
        }
    )
    assert response.status_code == 200
    assert response.json['success']
    assert response.json['user']['email'] == DEFAULT_EMAIL
    assert response.json['user']['name'] == DEFAULT_NAME

    # LOGOUT
    response = client.post_json(
        '/api/logout',
        {
            'token': client.__token__
        }
    )
    assert response.status_code == 200
    assert response.json['success']

    # LOGIN
    response = client.post_json(
        '/api/login',
        {
            'email': DEFAULT_EMAIL,
            'password': DEFAULT_PASSWORD,
            'token': client.__token__
        }
    )
    assert response.status_code == 200
    assert response.json['success']
    assert response.json['user']['email'] == DEFAULT_EMAIL
    assert response.json['user']['name'] == DEFAULT_NAME


def test_register_without_registration_token(client):
    response = client.post_json(
        '/api/register',
        {
            'email': 'test@test.com',
            'name': 'test',
            'token': client.__token__,
            'password': '123456'
        }
    )
    assert response.status_code == 200
    assert response.json == \
        {'success': False, 'error': 'InvalidRegistrationTokenException'}


def test_register_with_wrong_registration_token(client):
    response = client.post_json(
        '/api/register',
        {
            'email': DEFAULT_EMAIL,
            'name': DEFAULT_NAME,
            'password': DEFAULT_PASSWORD,
            'registration_token': 'wrong',
            'token': client.__token__
        }
    )
    assert response.status_code == 200
    assert response.json == \
        {'success': False, 'error': 'InvalidRegistrationTokenException'}
