from django import forms
from .models import MainDesc, AddDesc, Ingredients


class MainFoodForm(forms.Form):
    DescSearch = forms.CharField(label='Search MainFoodDesc for Foods', max_length=100)
