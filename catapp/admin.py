from django.contrib import admin
from .models import Cat
import re

@admin.action(description='Decouple the healthstatus from the name')
def healthstatus_fix(modeladmin, request, queryset):
    for cat in queryset:
        if cat.name:
            # We match until we encounter a . for end, for us it is mostly till end of string
            found = re.search('Hälsostatus[^.]*', cat.name)
            if found:
                #We remove all the newlines and tabs from the name
                testName = cat.name
                newname = re.sub('Hälsostatus[^.]*','',testName)
                newname = ' '.join(newname.split())
                cat.name = newname
                cat.health = found[0]
                cat.save()
                #print("New name will be:" + newname)
                #print("Health status will be:" + found[0])


class CatAdmin(admin.ModelAdmin):
    actions = [healthstatus_fix]


admin.site.register(Cat,CatAdmin)
