import unittest

import app
from tests.config import TestConfig


class AppCreateTest(unittest.TestCase):
    """
    Тестирует приложение
    """
    def test_app_create(self):
        """
        Проверяет фабрику приложения
        """
        self.assertFalse(app.create_app(TestConfig) is None, True)

