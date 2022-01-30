from django.http import Http404
from django.shortcuts import render, redirect
from .models import Cat
# Create your views here.


def home(request):
    return render(request, 'home.html', {})


def cat(request, cat_id):
    try:
        single_cat = Cat.objects.get(pk=cat_id)
        return render(request, 'cat.html', {'single_cat': single_cat})
    except Cat.DoesNotExist:
        raise Http404("Cat does not exist")

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def cat_list(request):
    cat_all = Cat.objects.all()
    if request.method == "GET":
        page = request.GET.get('page', 1)
    if request.method == "POST":
        page = request.POST.get('page_search')
        if not page:
            return redirect(request.META.get('HTTP_REFERER'))
    paginator = Paginator(cat_all, 50)
    try:
        cats = paginator.page(page)
    except PageNotAnInteger:
        #cats = paginator.page(1)
        return redirect(request.META.get('HTTP_REFERER'))
    except EmptyPage:
        cats = paginator.page(paginator.num_pages)

    return render(request, 'cat_list.html', { 'cats': cats })

def search_cat(request):
    if request.method == "POST":
        pageSearch = request.POST.get('cat_search')
        if pageSearch:
            print(pageSearch)
            return render(request, 'search_cat.html', {'pageSearch' : pageSearch})
        else:
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect(request.META.get('HTTP_REFERER'))

def advanced_search(request):
    return render(request, 'advanced_search.html', {})
