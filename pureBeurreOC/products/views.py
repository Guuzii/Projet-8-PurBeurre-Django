# from django.http import HttpResponse
# from django.template import loader
from django.shortcuts import render, redirect

from django.conf import settings

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from products.models import Nutriment, Category, Product, ProductCategories, ProductNutriments
from products.forms import SearchForm, UserForm, LoginForm

# Create your views here.
search_form_default = SearchForm()
user_form_default = UserForm()
login_form_default = LoginForm()

def index(request):
    context = {
        'search_form': search_form_default
    }

    return render(request, 'products/homepage.html', context)


@login_required()
def user(request):
    context = {
        'title': 'Salut ' + request.user.first_name + ' !',
        'search_form': search_form_default
    }

    return render(request, 'products/user-details.html', context)


def userCreate(request):
    context = {
        'title': 'Nouvel utilisateur',
        'user_form': user_form_default,
        'search_form': search_form_default
    }

    if request.method == "POST":
        form = UserForm(request.POST)

        if form.is_valid():
            created_user = User.objects.create_user(
                username=form.cleaned_data['username'], 
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name']
            )

            authenticated_user = authenticate(username=created_user.username, password=form.cleaned_data['password'])

            if authenticated_user is not None:
                login(request, authenticated_user)

                return redirect('home')
            else:
                return render(request, 'products/user-create.html', context)            
        else:
            return render(request, 'products/user-create.html', context)
    else:
        return render(request, 'products/user-create.html', context)


def UserLogin(request):
    context = {
        'title': 'Connexion utilisateur',
        'login_form': login_form_default,
        'search_form': search_form_default
    }

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            authenticated_user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])

            if authenticated_user is not None:
                login(request, authenticated_user)

                return redirect('home')
            else:
                return render(request, 'products/user-login.html', context)
        else:
            return render(request, 'products/user-login.html', context)
    else:
        return render(request, 'products/user-login.html', context)    


@login_required()
def UserLogout(request):
    logout(request)
    return redirect('home')


def searchResults(request):
    form = SearchForm(request.GET)

    if form.is_valid():
        product_name = form.cleaned_data['product_name']
        searched_product = Product.objects.filter(name__icontains=product_name).first()
        if searched_product:
            substitutes_products = Product.objects.filter(categories=searched_product.categories.first()).exclude(name__exact=searched_product.name).order_by('nutri_score')[:12]
        else:
            substitutes_products = None

    context = {
        'title': 'produit trouvé pour la recherche : "' + product_name + '"',
        'searched_product': searched_product,
        'products': substitutes_products,
        'search_form': search_form_default
    }

    return render(request, 'products/result-search.html', context)


@login_required()
def userResults(request):
    context = {
        'title': 'Salut ' + request.user.first_name + ' !',
        'search_form': search_form_default
    }

    return render(request, 'products/result-user.html', context)


def productDetails(request, product_id):
    searched_product = Product.objects.filter(id=product_id).first()
    product_nutriments = searched_product.nutriments.all()
    clean_nutriments = []

    # print(settings.NUTRIMENTS['fat'])

    # for test in settings.NUTRIMENTS:
    #     print(test)

    for nutriment in product_nutriments:
        clean_nutriments.append({
            "name": settings.NUTRIMENTS[nutriment.name]['name'],
            "unit": nutriment.unit,
            "quantity": ProductNutriments.objects.filter(product=searched_product, nutriment=nutriment).first().quantity
        })    

    context = {
        'title': searched_product.name,
        'searched_product': searched_product,
        'product_nutriments': clean_nutriments,
        'search_form': search_form_default
    }

    return render(request, 'products/product-details.html', context)

