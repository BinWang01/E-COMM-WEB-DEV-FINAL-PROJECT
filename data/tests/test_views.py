from django.test import TestCase, RequestFactory, Client
from django.contrib.auth.models import User, Group
from data.views import index

class TestIndexView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_index_view(self):
        request = self.factory.get('/index')
        request.session = {}
        response = index(request)
        self.assertEquals(response.status_code, 200)

class TestLoggedInGreetingView(TestCase):
    def setUp(self):
        test_user = User.objects.create_user(username='testuser', password='test@#628password')
        test_user.save()
        self.client = Client()

    def test_user_greeting_not_authenticated(self):
        response = self.client.get('/managecontent')
        self.assertEquals(response.status_code, 302)

    def test_user_authenticated(self):
        login = self.client.login(username='testuser', password='test@#628password')
        response = self.client.get('/managecontent')
        self.assertEquals(response.status_code, 302)