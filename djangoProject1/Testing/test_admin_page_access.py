from django.test import TestCase, Client

from djangoProject1.MethodFiles.GeneralMethods import CheckPermission
from djangoProject1.models import User

class TestAdminPageUnit(TestCase):
    def setUp(self):
        self.admin = User(role='Admin')
        self.instructor = User(role='instructor')
        self.ta = User(role='TA')

    def test_admin_user(self):
        self.assertTrue(CheckPermission.check_admin(self.admin))

    def test_instructor(self):
        self.assertFalse(CheckPermission.check_admin(self.instructor))

    def test_ta(self):
        self.assertFalse(CheckPermission.check_admin(self.ta))

    def test_no_user(self):
        self.assertFalse(CheckPermission.check_admin(None))

class TestAdminPageAcceptance(TestCase):
    def setUp(self):
        self.donkey = Client()
        self.admin = User(username='admin', role='Admin')
        self.instructor = User(username='instructor', role='Instructor')
        self.ta = User(username='ta', role='TA')
        self.admin.save()
        self.instructor.save()
        self.ta.save()

    def test_admin_access(self):
        response = self.donkey.post('/',{"username" : "admin", "password" : "Default_Password"}, follow=True)
        self.donkey.get('/admin_Home.html')

        #redirects to the admin page
        self.assertRedirects(response, "home.html", 302)

    def test_instructor_access(self):
        self.donkey.post('/', {"username": "instructor", "password": "Default_Password"}, follow=True)
        response = self.donkey.get('/admin_Home.html')
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.context)
        self.assertEqual(response.context["message"], "You cannot access this page.")

    def test_ta_access(self):
        self.donkey.post('/', {"username": "ta", "password": "Default_Password"}, follow=True)
        response = self.donkey.get('/admin_Home.html')

        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.context)
        self.assertEqual(response.context["message"], "You cannot access this page.")

    def test_no_user_access(self):
        response = self.donkey.get('/admin_Home.html')

        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.context)
        self.assertEqual(response.context["message"], "You cannot access this page.")
