from datetime import datetime

from django.db.models import F, Count
from django.db.models.functions import ExtractYear
from django.http import Http404
from django.shortcuts import render, redirect
from .models import Cat
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import SearchForm
import re
import plotly.express as px
import pandas

def home(request):
    cat_count = Cat.objects.all().count()
    # Cat breeds
    cat_breed_count = Cat.objects.values('breed').annotate(number = Count('breed'))
    cat_breed_values = Cat.objects.order_by('breed').values_list('breed', flat=True).distinct()
    #Remove values () and ( ) and replace them for readability
    cat_breed_values= list(cat_breed_values)
    cat_breed_values.remove('()')
    cat_breed_values.remove('( )')
    cat_breed_values.append('Unspecified')

    #Convert to two lists
    names = []
    values = []
    other_count = 0
    for count in cat_breed_count:
        if count['number'] >= 5000:
            names.append(count['breed'])
            values.append(count['number'])
        else:
            other_count = other_count + count['number']
    #Append cat breeds with less than 1% distribution
    names.append("Other")
    values.append(other_count)

    fig = px.pie(values=values, names=names, title='Breed Distribution')
    cat_breed_graph = fig.to_html()

    #Cat genders
    cat_gender_count = Cat.objects.values('gender').annotate(number=Count('gender'))
    names = []
    values = []
    for count in cat_gender_count:
        names.append(count['gender'])
        values.append(count['number'])
    fig = px.pie(values=values, names=names, title='Gender Distribution')
    cat_gender_graph = fig.to_html()

    #Birthyears
    cat_birth_count = Cat.objects.annotate(Year=ExtractYear('birth'))
    cat_birth_count = cat_birth_count.values('Year').annotate(number=Count('Year'))
    names = []
    values = []
    #lessthan1960 = 0
    for count in cat_birth_count:
        if count['Year'] and count['Year'] <= datetime.today().year:
            names.append(count['Year'])
            values.append(count['number'])
    fig = px.bar(x=names, y=values, title='Registrations by Year')
    cat_year_graph = fig.to_html()
    return render(request, 'home.html', {'cat_count': cat_count, 'cat_breed_graph': cat_breed_graph,
                                         'cat_breed_values': cat_breed_values, 'cat_gender_graph': cat_gender_graph,
                                         'cat_year_graph': cat_year_graph})


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
    cat_all = Cat.objects.all().order_by('id')
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
        cat_order_by = request.GET.get('cat_order_by', "id")
        cat_order = request.GET.get('cat_order', "")
        if cat_order == "-":
            cat_all = Cat.objects.all().order_by(F(cat_order_by).desc(nulls_last=True))#(cat_order+cat_order_by)
        else:
            cat_all = Cat.objects.all().order_by(F(cat_order_by).asc(nulls_last=True))  # (cat_order+cat_order_by)
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
                                                          'cat_date_after': cat_date_after,
                                                          'cat_order': cat_order, 'cat_order_by': cat_order_by})
    else:
        return redirect(request.META.get('HTTP_REFERER'))

def advanced_search(request):
    return render(request, 'advanced_search.html', {'search_form': SearchForm})

