from django import test

from catalog.models import Author
from django.urls import reverse

class AuthorListViewTest(test.TestCase):
	@classmethod
	def setUpTestData(cls):
		number_of_authors = 13
		for author_num in range(number_of_authors):
			Author.objects.create(first_name=f'christian{author_num}', last_name=f'Surname{author_num}')
	def test_view_url_exists_at_desired_location(self):
		resp = self.client.get('/catalog/authors/')
		self.assertEqual(resp.status_code, 200)
	def test_view_url_accesible_by_name(self):
		resp = self.client.get(reverse('catalog:authors'))
		self.assertEqual(resp.status_code, 200)
		self.assertEqual(resp, 'catalog/authors.html')