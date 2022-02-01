from django.http import Http404
from django.shortcuts import render, redirect
from .models import Cat
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import SearchForm


def home(request):
    return render(request, 'home.html', {})


def cat(request, cat_id):
    try:
        single_cat = Cat.objects.get(pk=cat_id)
        return render(request, 'cat.html', {'single_cat': single_cat})
    except Cat.DoesNotExist:
        raise Http404("Cat does not exist")

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
        search_term = request.GET.get('cat_name', "")
        cat_id = request.GET.get('cat_id', "")
        cat_gender = request.GET.get('cat_gender', "")
        cat_breed = request.GET.get('cat_breed', "")
        cat_date = request.GET.get('cat_date', "")
        cat_fur = request.GET.get('cat_fur', "")
        print(search_term)
        cat_all = Cat.objects.all()

        if search_term:
            cat_all = cat_all.filter(name__icontains=search_term)
        if cat_id:
            cat_all = cat_all.filter(number__icontains=cat_id)
        if cat_gender:
            cat_all = cat_all.filter(gender=cat_gender)
        if cat_breed:
            cat_all = cat_all.filter(breed=cat_breed)
        if cat_date:
            cat_all = cat_all.filter(birth=cat_date)
        if cat_fur:
            cat_all = cat_all.filter(fur__icontains=cat_fur)

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
        return render(request, 'cat_list_searched.html', {'cats': cats, 'searched_term': search_term,
                                                          'cat_id': cat_id, 'cat_gender': cat_gender,
                                                          'cat_breed': cat_id,
                                                          'cat_date': cat_date, 'cat_fur': cat_fur})
    else:
        return redirect(request.META.get('HTTP_REFERER'))

def advanced_search(request):
    return render(request, 'advanced_search.html', {'search_form': SearchForm})

