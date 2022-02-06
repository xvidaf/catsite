from django.http import Http404
from django.shortcuts import render, redirect
from .models import Cat
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import SearchForm
import re

def home(request):
    return render(request, 'home.html', {})


def cat(request, cat_id):
    try:
        single_cat = Cat.objects.get(pk=cat_id)
        if single_cat.father:
            try:
                # Had to remove the parenthesis for a whole word match to work
                #cat_father = Cat.objects.get(number__icontains=single_cat.father)
                cat_father = Cat.objects.get(number__iregex=r"\y{0}\y".format(re.sub(r'\([^)]*\)', '', single_cat.father)))
            except Cat.DoesNotExist:
                cat_father = None
        else:
            cat_father = None
        if single_cat.mother:
            try:
                #Had to remove the parenthesis for a whole word match to work
                #cat_mother = Cat.objects.get(number__icontains=single_cat.mother)
                cat_mother = Cat.objects.get(number__iregex=r"\y{0}\y".format(re.sub(r'\([^)]*\)', '', single_cat.mother)))
            except Cat.DoesNotExist:
                cat_mother = None
        else:
            cat_mother = None
        return render(request, 'cat.html', {'single_cat': single_cat,
                                            'cat_father': cat_father,
                                            'cat_mother': cat_mother})
    except Cat.DoesNotExist:
        raise Http404("Cat does not exist")

def cat_list(request):
    cat_all = Cat.objects.all()
    if request.method == "GET":
        page = request.GET.get('page', 1)
        paginator = Paginator(cat_all, 50)
        cat_count = cat_all.count()
        try:
            cats = paginator.page(page)
        except PageNotAnInteger:
            #cats = paginator.page(1)
            return redirect(request.META.get('HTTP_REFERER'))
        except EmptyPage:
            cats = paginator.page(paginator.num_pages)

        return render(request, 'cat_list.html', { 'cats': cats, 'cat_count': cat_count})
    else:
        return redirect(request.META.get('HTTP_REFERER'))


def search_cat(request):
    if request.method == "GET":
        search_term = request.GET.get('cat_name', "")
        cat_id = request.GET.get('cat_ID', "")
        cat_gender = request.GET.get('cat_gender', "")
        cat_breed = request.GET.get('cat_breed', "")
        cat_date = request.GET.get('cat_date', "")
        cat_fur = request.GET.get('cat_fur', "")
        cat_date_before = request.GET.get('cat_date_before', "")
        cat_date_after = request.GET.get('cat_date_after', "")
        print(cat_id)
        cat_all = Cat.objects.all()

        if search_term:
            cat_all = cat_all.filter(name__icontains=search_term)
        if cat_id:
            cat_all = cat_all.filter(number__icontains=cat_id)
        if cat_gender:
            cat_all = cat_all.filter(gender=cat_gender)
        if cat_breed:
            cat_all = cat_all.filter(breed__icontains=cat_breed)
        if cat_date:
            cat_all = cat_all.filter(birth=cat_date)
        if cat_fur:
            cat_all = cat_all.filter(fur__icontains=cat_fur)
        if cat_date_before:
            cat_all = cat_all.filter(birth__lte=cat_date_before)
        if cat_date_after:
            cat_all = cat_all.filter(birth__gte=cat_date_after)

        cat_count = cat_all.count()
        paginator = Paginator(cat_all, 50)
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
                                                          'cat_date': cat_date, 'cat_fur': cat_fur,
                                                          'cat_count': cat_count, 'cat_date_before': cat_date_before,
                                                          'cat_date_after': cat_date_after})
    else:
        return redirect(request.META.get('HTTP_REFERER'))

def advanced_search(request):
    return render(request, 'advanced_search.html', {'search_form': SearchForm})

