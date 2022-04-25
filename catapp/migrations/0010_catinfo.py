# Generated by Django 3.2.11 on 2022-04-25 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catapp', '0009_breeds'),
    ]

    operations = [
        migrations.CreateModel(
            name='CatInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CODE', models.CharField(max_length=10)),
                ('Name', models.CharField(max_length=100)),
                ('URL', models.CharField(max_length=1000)),
                ('Recognized', models.IntegerField()),
                ('ImageURL', models.CharField(max_length=1000)),
                ('FifeURL', models.CharField(max_length=1000)),
                ('Deutsch', models.CharField(max_length=100)),
                ('Français', models.CharField(max_length=100)),
            ],
        ),
    ]
