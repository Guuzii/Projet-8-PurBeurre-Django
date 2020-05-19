# from django.http import HttpResponse
# from django.template import loader
from django.shortcuts import render, redirect
from django.views import View
from django.conf import settings

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required

from products.models import Nutriment, Category, Product, ProductCategories, ProductNutriments
from products.forms import SearchForm, UserCreateForm, LoginForm

# Create your views here.

class HomeView(View):
    template_name = 'products/homepage.html'
    context = {
        'search_form': SearchForm()
    }

    def get(self, request):
        return render(request, self.template_name, self.context)


class UserView(View):
    template_name = 'products/user-details.html'
    context = {
        'search_form': SearchForm()
    }

    def get(self, request):
        self.context['title'] = 'Salut ' + request.user.first_name + ' !'
        self.context['user'] = request.user
        return render(request, self.template_name, self.context)
    
    def post(self, request):
        self.context['title'] = 'Salut ' + request.user.first_name + ' !'
        self.context['user'] = request.user
        return render(request, self.template_name, self.context)


class UserLogin(LoginView):
    template_name = 'products/user-login.html'
    authentication_form = LoginForm
    extra_context = {
        'title': 'Connexion utilisateur',
        'search_form': SearchForm()
    }


class UserLogout(LogoutView):
    def get(self, request, *args, **kwargs):
        return redirect('home')


class UserCreate(View):
    template_name = 'products/user-create.html'
    context = {
        'title': 'Création utilisateur',
        'search_form': SearchForm()
    }

    def get(self, request):
        """Return the signup template"""
        form = UserCreateForm()
        self.context['form'] = form
        return render(request, self.template_name, self.context)

    def post(self, request):
        """Process the UserCreate form, redirect and log the user if it is
        valid, return the signup template otherwise"""
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
        else :
            self.context['form'] = form
            self.context['errors'] = form.errors.items()
            return render(request, self.template_name, self.context)


class SearchResult(View):
    template_name = 'products/result-search.html'
    context = {
        'search_form': SearchForm()
    }

    def get(self, request):
        redirect('home')

    def post(self, request):
        form = SearchForm(request.POST)

        if form.is_valid():
            product_name = form.cleaned_data['product_name']
            searched_product = Product.objects.filter(name__icontains=product_name).first()

            if searched_product:
                substitutes_products = Product.objects.filter(categories=searched_product.categories.first()).exclude(name__exact=searched_product.name).order_by('nutri_score')[:12]
            else:
                substitutes_products = None    

            self.context['title'] = 'produit trouvé pour la recherche : "' + product_name + '"'
            self.context['searched_product'] = searched_product
            self.context['products'] = substitutes_products

            return render(request, self.template_name, self.context)
        else:
            self.context['errors'] = form.errors.items()
            return render(request, 'products/homepage.html', self.context)


class ProductDetails(View):
    context = {
        'search_form': SearchForm()
    }

    def get(self, request, product_id):
        searched_product = Product.objects.get(id=product_id)
        product_nutriments = searched_product.nutriments.all()
        clean_nutriments = []

        for nutriment in product_nutriments:
            clean_nutriments.append({
                "name": settings.NUTRIMENTS[nutriment.name]['name'],
                "unit": nutriment.unit,
                "quantity": ProductNutriments.objects.filter(product=searched_product, nutriment=nutriment).first().quantity
            }) 

        self.context['title'] = searched_product.name
        self.context['searched_product'] = searched_product
        self.context['product_nutriments'] = clean_nutriments

        return render(request, 'products/product-details.html', self.context)

    def post(self, request):
        return redirect('home')


class UserResults(View):
    template_name = 'products/result-user.html'
    context = {
        'search_form': SearchForm()
    }

    def get(self, request):
        self.context['title'] = 'Salut ' + request.user.first_name + ' !'
        return render(request, self.template_name, self.context)
    
    def post(self, request):
        self.context['title'] = 'Salut ' + request.user.first_name + ' !'
        return render(request, self.template_name, self.context)
