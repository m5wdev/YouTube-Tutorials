# from django.test import TestCase, SimpleTestCase
from django.test import TestCase
from django.urls import reverse


class TestCore(TestCase):
    def setUp(self):
        self.homepage_url = reverse('homepage')

    # def test_sample_test(self):
    #     assert 1 == 1

    def test_homepage(self):
        # response = self.client.get(reverse('homepage'))
        response = self.client.get(self.homepage_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'homepage/homepage.html')
