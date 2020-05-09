# from django.http import HttpResponse
# from django.template import loader
from django.shortcuts import render

from django.conf import settings

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
            substitutes_products = Product.objects.filter(categories=searched_product.categories.first()).exclude(name__exact=searched_product.name).order_by('nutri_score')[:12]
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

    return render(request, 'products/details.html', context)

