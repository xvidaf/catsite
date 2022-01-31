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
        paginator = Paginator(cat_all, 50)
        try:
            cats = paginator.page(page)
        except PageNotAnInteger:
            #cats = paginator.page(1)
            return redirect(request.META.get('HTTP_REFERER'))
        except EmptyPage:
            cats = paginator.page(paginator.num_pages)

        return render(request, 'cat_list.html', { 'cats': cats })
    else:
        return redirect(request.META.get('HTTP_REFERER'))


def search_cat(request):
    if request.method == "GET":
        search_term = request.GET.get('search_term', None)
        if search_term:
            print(search_term)
            cat_all = Cat.objects.filter(name__icontains=search_term)
            paginator = Paginator(cat_all, 1)
            page = request.GET.get('page', 1)
            print(page)
            try:
                cats = paginator.page(page)
            except PageNotAnInteger:
                # cats = paginator.page(1)
                return redirect(request.META.get('HTTP_REFERER'))
            except EmptyPage:
                cats = paginator.page(paginator.num_pages)
            return render(request, 'cat_list_searched.html', {'cats': cats, 'searched_term': search_term})
        else:
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect(request.META.get('HTTP_REFERER'))

def advanced_search(request):
    return render(request, 'advanced_search.html', {})
