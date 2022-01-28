from django.db import models


class Cat(models.Model):
    internalID = models.IntegerField('Cat serial number from the csv')
    Name = models.CharField('Name of the cat', max_length=100)
    Breed = models.CharField('Breed of the cat', max_length=100)
    Birth = models.DateField('Birthdate of the cat')
    Gender = models.CharField('Gender of the cat', max_length=100)
    Fur = models.CharField('Fur code of the cat', max_length=100)
    Number = models.CharField('Identification number of the cat', max_length=200)
    Title = models.CharField('Titles of the cat', max_length=50)
    Father = models.CharField('Identification of the Father of the cat', max_length=200)
    Mother = models.CharField('Identification of the Mother of the cat', max_length=200)
    From = models.CharField('Site from which the cat is from', max_length=20)

    def __str__(self):
        return self.Name
