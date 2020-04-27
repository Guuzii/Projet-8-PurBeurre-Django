# from django.http import HttpResponse
# from django.template import loader
from django.shortcuts import render

# Create your views here.

def index(request):
    # template = loader.get_template('homepage/index.html')
    return render(request, 'products/homepage.html')

def searchResults(request):
    context = {
        'title': 'produit',
    }

    return render(request, 'products/search-result.html', context)

def userResults(request):
    context = {
        'title': 'nom utilisateur',
    }

    return render(request, 'products/user-result.html', context)

