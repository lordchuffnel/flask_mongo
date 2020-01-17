import unittest

from mongoengine import get_db

from application import create_app as create_app_base
from user.models import User


class UserTest(unittest.TestCase):

  def create_app(self):
    self.db_name = 'flask_test'
    return create_app_base(
      MONGO_SETTINGS={'DB': self.db_name},
      TESTING=True,
      WTF_CSRF_ENABLED = False
    )

  def setUp(self):
    self.app_factory = self.create_app()
    self.app = self.app_factory.test_client()

  def tearDown(self):
    db = get_db
    db.client.drop_database(db)

  def test_register_user(self):
    # basic registration
    rv = self.app.post('/register', data=dict(
      first_name='frank',
      last_name='billy',
      username='filly',
      email='test@test.com',
      password='test123',
      confirm='test123'
    ), follow_redirects=True)
    assert User.objects.filter(username='frank') == 1
