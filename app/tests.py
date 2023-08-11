import unittest

from app import db
from app.models import Account

class AccountModelCase(unittest.TestCase):
    def setUp(self) -> None:
        db.create_all()

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        account = Account(username='Egor')
        account.set_password('123456')
        self.assertFalse(account.check_password('12345'))
        self.assertTrue(account.check_password('123456'))
