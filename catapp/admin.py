from django.contrib import admin
from .models import Cat, Breeds, AppearanceCodes, CatInfo
import re
from django.db.models import Count
from import_export.admin import ImportExportModelAdmin
from import_export import resources

from .views import findParent


@admin.action(description='Decouple the healthstatus from the name')
def healthstatus_fix(modeladmin, request, queryset):
    #Cats with healtinfo have H in the name, we remove it
    p = re.compile(r'\b(?:%s)\b' % '|'.join(["H"]))
    for cat in queryset:
        if cat.name:
            # We match until we encounter a ; for end, for us it is mostly till end of string
            found = re.search('Hälsostatus[^.]*', cat.name)
            if found:
                #We remove all the newlines and tabs from the name
                testName = cat.name
                #We remove the H from the name
                newname = re.sub('Hälsostatus[^.]*','',testName)
                newname = p.sub("", newname)
                newname = ' '.join(newname.split())
                cat.name = newname
                #If the cat already has health information
                if cat.health:
                    cat.health = cat.health + found[0]
                else:
                    cat.health = found[0]
                cat.save()
                #print("New name will be:" + newname)
                #print("Health status will be:" + found[0])

@admin.action(description='Delete duplicates')
def delete_duplicates(modeladmin, request, queryset):
    for row in Cat.objects.all().reverse():
        if Cat.objects.filter(name=row.name, breed=row.breed, number=row.number, gender=row.gender).count() > 1:
            row.delete()


@admin.action(description='Decouple titles from name')
def title_fix(modeladmin, request, queryset):
    # Known titles of cats, used to check for them in the name, and remove them
    listOfTitles = ["CH", "P", "IC", "IP", "GIC", "GIP", "EC", "EP", "SC", "SP", "JW", "DSM", "DVM", "NW", "WW", "RW",
                    "Int.", "Ch", "Cham", "RW", "CH", "GCH", "DGCH", "TGCH", "QGCH", ",", "DM"]
    p = re.compile(r'\b(?:%s)\b' % '|'.join(listOfTitles))  # For regex searching
    for cat in queryset:
        if cat.name:
            if cat.title:
                new_name = p.sub("", cat.name)
                new_title = cat.title + "," + ",".join(re.findall(p, cat.name))
            else:
                new_name = p.sub("", cat.name)
                new_title = ",".join(re.findall(p, cat.name))
            if new_title != cat.title and new_name != cat.name:
                cat.name = ' '.join(new_name.split())
                cat.title = cat.title
                cat.save()

@admin.action(description='Fix leading spaces, remove cat breed from code')
def breedcodes_fix(modeladmin, request, queryset):
    for code in queryset:
        if code.CODE:
            code.CODE = re.sub(r'[A-Z]', '', code.CODE)
            code.CODE = code.CODE.replace('/', '')
            code.CODE = code.CODE.strip()
        if code.English:
            code.English = code.English.strip()
        if code.Deutsch:
            code.Deutsch = code.Deutsch.strip()
        if code.Français:
            code.Français = code.Français.strip()
        code.save()


@admin.action(description='Add foreign key based on father and mother column')
def add_cat_foreign(modeladmin, request, queryset):
    #Crete a foreign key from the parents of the cat
    newQuerySet = queryset.filter(fatherLink__isnull=True,motherLink__isnull=True)
    newQuerySet = newQuerySet.order_by('id')
    for cat in newQuerySet:
        print(cat.id)
        if cat.father and not cat.fatherLink:
            father = findParent(cat.father)
            if father:
                cat.fatherLink = father
                cat.save(update_fields=['fatherLink'])
        if cat.mother and not cat.motherLink:
            mother = findParent(cat.mother)
            if mother:
                cat.motherLink = mother
                cat.save(update_fields=['motherLink'])


class AppearanceCodesResource(resources.ModelResource):
    class Meta:
        model = AppearanceCodes


class AppearanceCodesAdmin(ImportExportModelAdmin):
    resource_class = AppearanceCodesResource
    actions = [breedcodes_fix]


class BreedsResource(resources.ModelResource):
    class Meta:
        model = Breeds


class BreedsAdmin(ImportExportModelAdmin):
    resource_class = BreedsResource


class CatResource(resources.ModelResource):
    class Meta:
        model = Cat


class CatAdmin(ImportExportModelAdmin):
    actions = [healthstatus_fix, delete_duplicates, title_fix, add_cat_foreign]
    resource_class = CatResource
    raw_id_fields = ['fatherLink', 'motherLink']


admin.site.register(Cat, CatAdmin)
admin.site.register(AppearanceCodes, AppearanceCodesAdmin)
admin.site.register(Breeds, BreedsAdmin)
admin.site.register(CatInfo)
