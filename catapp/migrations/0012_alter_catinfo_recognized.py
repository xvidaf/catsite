# Generated by Django 3.2.11 on 2022-04-25 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catapp', '0011_rename_français_catinfo_francais'),
    ]

    operations = [
        migrations.AlterField(
            model_name='catinfo',
            name='Recognized',
            field=models.CharField(max_length=100),
        ),
    ]
