# Generated by Django 3.2.11 on 2022-02-16 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catapp', '0006_cat_health'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cat',
            name='health',
            field=models.CharField(max_length=500, null=True, verbose_name='Health information about the cat'),
        ),
    ]
