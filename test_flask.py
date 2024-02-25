import unittest
from app import app, db, User

class FlaskTests(unittest.TestCase):
    def setUp(self):
        """Stuff to do before every test."""
        self.client = app.test_client()
        app.config['TESTING'] = True

        # Push an application context
        app.app_context().push()

        # Connect to test database
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
        db.create_all()

    def tearDown(self):
        """Stuff to do after every test."""
        db.session.rollback()
        db.drop_all()

    def test_redirect_to_users(self):
        with self.client as c:
            resp = c.get('/')
            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, 'http://localhost/users')

    def test_show_all_users(self):
        with self.client as c:
            resp = c.get('/users')
            self.assertEqual(resp.status_code, 200)
            self.assertIn(b'List of Users', resp.data)

    def test_add_new_user(self):
        with self.client as c:
            resp = c.post('/users/new', data={
                'first_name': 'John',
                'last_name': 'Doe',
                'image_url': 'test.jpg'
            }, follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn(b'John Doe', resp.data)

    def test_show_user_detail(self):
        # Create a test user
        user = User(first_name='Test', last_name='User', image_url='test.jpg')
        db.session.add(user)
        db.session.commit()

        with self.client as c:
            resp = c.get(f'/users/{user.id}')
            self.assertEqual(resp.status_code, 200)
            self.assertIn(b'Test User', resp.data)

if __name__ == '__main__':
    unittest.main()
