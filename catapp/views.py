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

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def cat_list(request):
    cat_all = Cat.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(cat_all, 50)
    try:
        cats = paginator.page(page)
    except PageNotAnInteger:
        cats = paginator.page(1)
    except EmptyPage:
        cats = paginator.page(paginator.num_pages)

    return render(request, 'cat_list.html', { 'cats': cats })

