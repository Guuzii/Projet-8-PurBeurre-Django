from django.test import TestCase
from django.urls import reverse

from django.contrib.auth.models import User

from products.models import Category, Product, ProductCategories, ProductUsers
from products.forms import UserCreateForm, LoginForm

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

    # test that Search-result page returns a status code 200, products!=None, searched_product not in products
    # and substitute_product is in products, if product found
    def test_searchresult_page_returns_products_list(self):
        search_string = self.test_product.name
        response = self.client.post(reverse('product-search-results'), { 'product_name': search_string })
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context['products'])
        self.assertIn(self.test_substitute_product, response.context['products'])
        self.assertNotIn(self.test_product, response.context['products'])
        
    # test that Search-result page returns products=None, if product not found
    def test_searchresult_page_returns_none(self):
        search_string = "azerty"
        response = self.client.post(reverse('product-search-results'), { 'product_name': search_string })
        self.assertIsNone(response.context['products'])


# Product-details page
class ProductDetailsPage(TestCase):
    def setUp(self):
        self.test_product = Product.objects.create(name="Produit test", url="test.fr", nutri_score="c")
        test_category = Category.objects.create(name="test-category")
        ProductCategories.objects.create(product=self.test_product, category=test_category)

    # test that Product-Details page returns a status code 200 and the right product, if product exist
    def test_searchresult_page_returns_200(self):
        product_id = self.test_product.id
        response = self.client.get(reverse('product-details', args=(product_id,)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['searched_product'], self.test_product)
        
    # test that Product-Details page returns a status code 404, if product doesn't exist
    def test_searchresult_page_returns_404(self):
        product_id = self.test_product.id + 1 
        response = self.client.get(reverse('product-details', args=(product_id,)))
        self.assertEqual(response.status_code, 404)


# Product save


# User-create page
class UserCreatePage(TestCase):
    def setUp(self):
        self.test_create_form = UserCreateForm()

    # test that User-Create page returns a status code 200 and the right form, on get request
    def test_usercreate_page_get_returns_form(self):
        response = self.client.get(reverse('user-create'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form'].fields.keys(), self.test_create_form.fields.keys())
        
    # test that User-Create page create a new user and authenticate it, on post request with valid form
    def test_usercreate_page_post_valid_form(self):
        response = self.client.post(reverse('user-create'), { 
            'username': "testuser", 
            'first_name': "testuser name", 
            'email':  "test@test.fr",
            'password1': "test123+",
            'password2': "test123+"
        })
        self.assertIsNone(response.context)
        
        last_created_user = User.objects.latest('id')
        self.assertEqual(last_created_user.username, "testuser")
        self.assertEqual(last_created_user.id, int(self.client.session['_auth_user_id']))

    # test that User-Create page returns errors context, on post request with invalid form
    def test_usercreate_page_post_invalid_form(self):
        response = self.client.post(reverse('user-create'), { 
            'username': "testuserfail", 
            'first_name': "testuser name", 
            'email':  "testeur@test.fr",
            'password1': "123456",
            'password2': "123456"
        })
        self.assertIsNotNone(response.context['errors'])


# User-login page
class UserLoginPage(TestCase):
    def setUp(self):
        pass

    # test that User-login page returns a status code 200 and the right form, on get request
    def test_userlogin_page_get_returns_form(self):
        pass
    
    # test that User-login page log user and redirect to homepage, on post request with good credentials
    def test_userlogin_page_post_valid_credentials(self):
        pass
        
    # test that User-login page return errors context, on post request with bad credentials
    def test_userlogin_page_post_invalid_credentials(self):
        pass


# User-result Page
class UserResultPage(TestCase):
    def setUp(self):
        pass

    # test that User-result page returns a status code 200 and the right products
    def test_userresult_page_returns_200(self):
        pass
        
    # test that Search-result page returns a status code 404, if product doesn't exist
    def test_userresult_page_returns_404(self):
        pass

# User-details page

