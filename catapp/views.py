from datetime import datetime

from django.db.models import F, Count, Q
from django.db.models.functions import ExtractYear
from django.http import Http404
from django.shortcuts import render, redirect
from .models import Cat
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import SearchForm
import re
import plotly.express as px
from googletrans import Translator
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

    #Appearances
    cat_appearance_count = Cat.objects.values('fur').annotate(number=Count('fur')).order_by('-number')
    #Percentage of columns filled
    cat_name = Cat.objects.exclude(name__isnull=True).exclude(name__exact='').count()
    cat_breed = Cat.objects.exclude(breed__isnull=True).exclude(breed__exact='').count()
    cat_birth = Cat.objects.exclude(birth__isnull=True).count()
    cat_gender = Cat.objects.exclude(gender__isnull=True).exclude(gender__exact='').count()
    cat_fur = Cat.objects.exclude(fur__isnull=True).exclude(fur__exact='').count()
    cat_number = Cat.objects.exclude(number__isnull=True).exclude(number__exact='').count()
    cat_title = Cat.objects.exclude(title__isnull=True).exclude(title__exact='').count()
    cat_father = Cat.objects.exclude(father__isnull=True).exclude(father__exact='').count()
    cat_mother = Cat.objects.exclude(mother__isnull=True).exclude(mother__exact='').count()
    cat_site = Cat.objects.exclude(site__isnull=True).exclude(site__exact='').count()
    cat_health = Cat.objects.exclude(health__isnull=True).exclude(health__exact='').count()
    return render(request, 'home.html', {'cat_count': cat_count, 'cat_breed_graph': cat_breed_graph,
                                         'cat_breed_values': cat_breed_values, 'cat_gender_graph': cat_gender_graph,
                                         'cat_year_graph': cat_year_graph, 'cat_appearance_graph': cat_appearance_count[1:20],
                                         'cat_name': round(cat_name/cat_count*100, 2),'cat_breed': round(cat_breed/cat_count*100, 2),
                                         'cat_birth': round(cat_birth/cat_count*100, 2),'cat_gender': round(cat_gender/cat_count*100, 2),
                                         'cat_fur': round(cat_fur/cat_count*100, 2),'cat_number': round(cat_number/cat_count*100, 2),
                                         'cat_title': round(cat_title/cat_count*100, 2),'cat_father': round(cat_father/cat_count*100, 2),
                                         'cat_mother': round(cat_mother/cat_count*100, 2),'cat_site': round(cat_site/cat_count*100, 2),
                                         'cat_health': round(cat_health/cat_count*100, 2)})


def findParent(parent_id):
    if parent_id:
        # We try an exact match, if unsuccessful we try a word match
        try:
            parent = Cat.objects.get(number=parent_id)
        except Cat.DoesNotExist:
            try:
                # Had to remove the parenthesis for a whole word match to work
                parent = Cat.objects.get(number__iregex=r"\y{0}\y".format(re.sub(r'\([^)]*\)', '', parent_id)))
            except Cat.DoesNotExist:
                parent = None
            except Cat.MultipleObjectsReturned:
                # Should be fine, most same matches are duplicates, not different cats with same id
                parent = Cat.objects.filter(number__iregex=r"\y{0}\y".format(re.sub(r'\([^)]*\)', '', parent_id))).first()
        except Cat.MultipleObjectsReturned:
            #Should be fine, most same matches are duplicates, not different cats with same id
            parent = Cat.objects.filter(number=parent_id).first()
    else:
        parent = None
    return parent


def cat(request, cat_id):
    try:
        row1 = []
        row2 = []
        row3 = []
        single_cat = Cat.objects.get(pk=cat_id)
        if single_cat.father:
            row1.append(findParent(single_cat.father))
        else:
            row1.append(None)
        if single_cat.mother:
            row1.append(findParent(single_cat.mother))
        else:
            row1.append(None)

        for parent in row1:
            if parent:
                row2.append(findParent(parent.father))
                row2.append(findParent(parent.mother))
            else:
                row2.append(None)
                row2.append(None)
        for parent in row2:
            if parent:
                row3.append(findParent(parent.father))
                row3.append(findParent(parent.mother))
            else:
                row3.append(None)
                row3.append(None)
        #Find children
        idList = single_cat.number.split('(')
        cat_children = Cat.objects.all()
        for word in idList:
            cat_children = cat_children.filter(Q(father__icontains='(' + word) | Q(mother__icontains='(' + word))
        translateGET = request.GET.get('translate', "No")
        if translateGET == "Yes":
            translator = Translator()
            if single_cat.gender:
                translated_gender = translator.translate(single_cat.gender, src='sv').text
            else:
                translated_gender = ""
            if single_cat.breed:
                translated_breed = translator.translate(single_cat.breed, src='sv').text
            else:
                translated_breed = ""
            if single_cat.fur:
                translated_fur = translator.translate(single_cat.fur, src='sv').text
            else:
                translated_fur = ""
            if single_cat.health:
                translated_health = translator.translate(single_cat.health, src='sv').text
            else:
                translated_health = ""
            return render(request, 'cat.html', {'single_cat': single_cat,
                                                'cat_father': row1[0],
                                                'cat_mother': row1[1],
                                                'cat_grandfather1': row2[0],'cat_grandmother1': row2[1],
                                                'cat_grandfather2': row2[2],'cat_grandmother2': row2[3],
                                                'cat_grandfather1_father': row3[0],'cat_grandfather1_mother': row3[1],
                                                'cat_grandmother1_father': row3[2],'cat_grandmother1_mother': row3[3],
                                                'cat_grandfather2_father': row3[4], 'cat_grandfather2_mother': row3[5],
                                                'cat_grandmother2_father': row3[6], 'cat_grandmother2_mother': row3[7],
                                                'cat_children': cat_children, 'cat_children_amount': cat_children.count(),
                                                'translated_gender': translated_gender, 'translated_health': translated_health,
                                                'translated_breed': translated_breed,
                                                'translated_fur': translated_fur})
        else:
            return render(request, 'cat.html', {'single_cat': single_cat,
                                                'cat_father': row1[0],
                                                'cat_mother': row1[1],
                                                'cat_grandfather1': row2[0],'cat_grandmother1': row2[1],
                                                'cat_grandfather2': row2[2],'cat_grandmother2': row2[3],
                                                'cat_grandfather1_father': row3[0],'cat_grandfather1_mother': row3[1],
                                                'cat_grandmother1_father': row3[2],'cat_grandmother1_mother': row3[3],
                                                'cat_grandfather2_father': row3[4], 'cat_grandfather2_mother': row3[5],
                                                'cat_grandmother2_father': row3[6], 'cat_grandmother2_mother': row3[7],
                                                'cat_children': cat_children, 'cat_children_amount': cat_children.count()})

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

