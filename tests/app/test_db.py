from app.models import Account
from tests.config import TestConfig
import unittest
from app import create_app, db


class AccountTest(unittest.TestCase):
    """
    Тестирует аккаунт
    """
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_account_create(self):
        """
        Тестирует создание аккаунта
        """
        account = Account(username='test', email='test@test.com')
        account.set_password('test')
        db.session.add(account)
        db.session.commit()
        self.assertTrue(account)

    def test_account_password_check(self):
        """
        Тестирует задание пароля в аккаунт
        """
        account = Account(username='test', email='test@test.com')
        account.set_password('test')
        db.session.add(account)
        db.session.commit()
        self.assertTrue(account.check_password('test'))
        self.assertFalse(account.check_password('not_test'))

