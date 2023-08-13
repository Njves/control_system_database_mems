from app.models import Account, Mem
from tests.config import TestConfig
import unittest
from app import create_app, db
import pathlib

class AccountTest(unittest.TestCase):
    """
    Тестирует аккаунт
    """
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.account = Account(username='test', email='test@test.com')
        db.create_all()
        self.account.set_password('test')
        db.session.add(self.account)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_account_create(self):
        """
        Тестирует создание аккаунта
        """
        self.assertTrue(self.account)

    def test_account_password_check(self):
        """
        Тестирует задание пароля в аккаунт
        """
        self.account.set_password('test')
        self.assertTrue(self.account.check_password('test'))
        self.assertFalse(self.account.check_password('not_test'))

    def test_account_set_avatar(self):
        """
        Тестирует задание аватрки
        """
        self.assertEqual(self.account.avatar, 'icon/avatar_placeholder.png')
        self.assertRaises(FileNotFoundError,
                          self.account.set_avatar, 'picture.png')
        # TODO: Дописать

    def test_reset_password(self):
        token = self.account.get_reset_password_token()
        self.assertEqual(self.account.verify_reset_password_token(token), self.account)
        self.assertFalse(self.account.verify_reset_password_token(token) is None)
        token = self.account.get_reset_password_token(expires_in=0)
        self.assertEqual(self.account.verify_reset_password_token(token), None)

    def test_amount_mems(self):
        mems = [Mem(link='', owner=self.account), Mem(link='', owner=self.account)]
        self.assertEqual(self.account.amount, 2)
        mems.append(Mem(link='', owner=self.account))
        self.assertEqual(self.account.amount, 3)


if __name__ == '__main__':
    unittest.main(verbosity=2)

