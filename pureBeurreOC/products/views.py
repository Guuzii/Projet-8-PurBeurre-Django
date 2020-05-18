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
    search_form = SearchForm()
    context = {
        'search_form': search_form
    }

    return render(request, 'products/homepage.html', context)


@login_required()
def user(request):
    search_form = SearchForm()

    context = {
        'title': 'Salut ' + request.user.first_name + ' !',
        'search_form': search_form
    }

    return render(request, 'products/user-details.html', context)


def userCreate(request):
    context = {
        'title': 'Nouvel utilisateur',
        'search_form': search_form_default
    }

    if request.method == "POST":
        form = UserForm(request.POST)

        if form.is_valid():
            if not User.objects.filter(username__iexact=form.cleaned_data['username']).exists():
                if not User.objects.filter(email__iexact=form.cleaned_data['email']).exists():
                    created_user = User.objects.create_user(
                        username=form.cleaned_data['username'], 
                        email=form.cleaned_data['email'],
                        password=form.cleaned_data['password'],
                        first_name=form.cleaned_data['first_name']
                    )

                    if created_user is not None:
                        authenticated_user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
                        
                        if authenticated_user is not None:
                            login(request, authenticated_user)

                            return redirect('home')
                        else:
                            context['errors'] = [('user-auth', "Problème lors de l'authentification de l'utilisateur")]

                    else:
                        context['errors'] = [('user-create', "Problème lors de la création de l'utilisateur.")]
                
                else:
                    context['errors'] = [('email', 'Un utilisateur avec cet email existe déjà.')]
            
            else:
                context['errors'] = [('username', "Un utilisateur avec cet identifiant existe déjà")]
        
        else:
            context['errors'] = form.errors.items()

    else:
        form = UserForm()
    
    # print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    # print(context['errors'])
    # print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    
    context['user_form'] = form
    return render(request, 'products/user-create.html', context)


def UserLogin(request):
    context = {
        'title': 'Connexion utilisateur',
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
                context['errors'] = [('user-login', "L'identifiant et/ou le mot de passe ne correspondent pas.")]
        else:
            context['errors'] = form.errors.items()
    else:
        form = LoginForm()

    context['login_form'] = form   
    return render(request, 'products/user-login.html', context)    


@login_required()
def UserLogout(request):
    logout(request)
    return redirect('home')


def searchResults(request):
    context = {
        'search_form': search_form_default
    }

    if request.method == 'POST':
        form = SearchForm(request.POST)

        if form.is_valid():
            product_name = form.cleaned_data['product_name']
            searched_product = Product.objects.filter(name__icontains=product_name).first()

            if searched_product:
                substitutes_products = Product.objects.filter(categories=searched_product.categories.first()).exclude(name__exact=searched_product.name).order_by('nutri_score')[:12]
            else:
                substitutes_products = None    

            context['title'] = 'produit trouvé pour la recherche : "' + product_name + '"'
            context['searched_product'] = searched_product
            context['products'] = substitutes_products

            return render(request, 'products/result-search.html', context)
        else:
            context['errors'] = form.errors.items()
    
    else:
        return redirect('home')


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

