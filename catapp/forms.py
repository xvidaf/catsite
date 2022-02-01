from django import forms


class SearchForm(forms.Form):
    cat_name = forms.CharField(label='Name', max_length=5000,required=False, )
    cat_id = forms.CharField(label='ID', max_length=1000,required=False)
    cat_gender = forms.ChoiceField(label='Gender', choices=(('', '----'), ('Hane', 'Hane'),('Hona', 'Hona'),), required=False)
    cat_breed = forms.CharField(label='Breed', max_length=100,required=False)
    cat_birth = forms.DateField(label='Birthdate', widget=forms.SelectDateWidget,required=False)
    cat_fur = forms.CharField(label='Fur Code', max_length=1000,required=False)