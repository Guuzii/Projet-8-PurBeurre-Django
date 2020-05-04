# from django.http import HttpResponse
# from django.template import loader
from django.shortcuts import render

from products.models import Nutriment, Category, Product, ProductCategories, ProductNutriments
from products.forms import SearchForm

# Create your views here.
search_form_default = SearchForm()

def index(request):
    context = {
        'search_form': search_form_default
    }

    return render(request, 'products/homepage.html', context)

def searchResults(request):
    form = SearchForm(request.GET)

    if form.is_valid():
        product_name = form.cleaned_data['product_name']
        searched_product = Product.objects.filter(name__icontains=product_name).first()
        if searched_product:
            substitutes_products = Product.objects.filter(categories=searched_product.categories.first()).order_by('nutri_score')[:10]
        else:
            substitutes_products = None

    context = {
        'title': 'produit trouvé pour la recherche : "' + product_name + '"',
        'searched_product': searched_product,
        'products': substitutes_products,
        'search_form': search_form_default
    }

    return render(request, 'products/search-result.html', context)

def userResults(request):
    context = {
        'title': 'nom utilisateur',
        'search_form': search_form_default
    }

    return render(request, 'products/user-result.html', context)

