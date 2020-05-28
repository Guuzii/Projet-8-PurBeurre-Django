from django.test import TestCase
from django.urls import reverse

from products.models import Nutriment, Category, Product, ProductCategories, ProductNutriments, ProductUsers

# Homepage page
class HomePageTestCase(TestCase):
    def test_homepage(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

# Search-result Page
class SearchResultPage(TestCase):
    def setUp(self):
        self.test_product = Product.objects.create(name="Produit test", url="test.fr", nutri_score="c")
        self.test_substitute_product = Product.objects.create(name="Substitut produit test", url="test-sub.fr", nutri_score="a")
        test_category = Category.objects.create(name="test-category")
        ProductCategories.objects.create(product=self.test_product, category=test_category)
        ProductCategories.objects.create(product=self.test_substitute_product, category=test_category)

    # test that Search-result page returns a 200 if product found
    def test_searchresult_page_returns_200(self):
        search_string = self.test_product.name
        response = self.client.post(reverse('product-search-results'), { 'product_name': search_string })
        self.assertEqual(response.status_code, 200)
        
    # test that Search-result page returns a 404 if product not found
    def test_searchresult_page_returns_404(self):
        search_string = "azerty"
        response = self.client.post(reverse('product-search-results'), { 'product_name': search_string })
        self.assertEqual(response.status_code, 404)

# Product-details page
class ProductDetailsPage(TestCase):
    def setUp(self):
        self.test_product = Product.objects.create(name="Produit test", url="test.fr", nutri_score="c")
        test_category = Category.objects.create(name="test-category")
        ProductCategories.objects.create(product=self.test_product, category=test_category)

    # test that Search-result page returns a 200 if product found
    def test_searchresult_page_returns_200(self):
        product_id = self.test_product.id
        response = self.client.get(reverse('product-details', args=(product_id,)))
        self.assertEqual(response.status_code, 200)
        
    # test that Search-result page returns a 404 if product not found
    def test_searchresult_page_returns_404(self):
        product_id = self.test_product.id + 1 
        response = self.client.get(reverse('product-details', args=(product_id,)))
        self.assertEqual(response.status_code, 404)

# Product save

# User-result Page

# User-details page

# User creation

