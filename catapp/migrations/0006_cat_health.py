# Generated by Django 3.2.11 on 2022-02-16 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catapp', '0005_alter_cat_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='cat',
            name='health',
            field=models.CharField(max_length=100, null=True, verbose_name='Health information about the cat'),
        ),
    ]
