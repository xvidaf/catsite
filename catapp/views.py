from django.http import Http404
from django.shortcuts import render
from .models import Cat
# Create your views here.


def home(request):
    return render(request, 'home.html', {})


def cat(request, cat_id):
    try:
        single_cat = Cat.objects.get(pk=cat_id)
        return render(request, 'cat.html', {'single_cat': single_cat})
    except Cat.DoesNotExist:
        raise Http404("Poll does not exist")

