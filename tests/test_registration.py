
import re
from tests.test_utils import try_post_route

REGISTER_VARIANTS = ['/register', '/sign-up', '/signup']

def post_register(app_client, data):
    route, r = try_post_route(app_client, REGISTER_VARIANTS, data=data)
    return route, r

def test_email_format_validation(app_client):
    bad_emails = ['plainaddress', 'a@b', 'x@@y.com', 'a b@c.com', 'a@c', 'a@.com']
    for e in bad_emails:
        _, r = post_register(app_client, {'name':'User','email': e, 'password':'p@ss'})
        assert r.status_code == 200
        assert re.search(r"(invalid|email)", r.get_data(as_text=True), re.I), f"Should reject {e}"

def test_email_case_insensitive_uniqueness(app_client):
    _ , r1 = post_register(app_client, {'name':'User','email':'CaseUser@example.com','password':'p@ss'})
    _ , r2 = post_register(app_client, {'name':'User2','email':'caseuser@EXAMPLE.com','password':'p@ss2'})
    assert r2.status_code == 200
    assert re.search(r"(exists|duplicate|already)", r2.get_data(as_text=True), re.I)

def test_password_not_stored_in_plaintext():
    # This is an intentionally failing discovery test until hashing is implemented
    from app import users, User
    u = User('plain@test.com','secret','Plain','Addr')
    assert getattr(u, 'password', None) != 'secret', 'Password stored in plaintext (security issue)'
