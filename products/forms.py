from django import forms


# searchbar Form
class SearchForm(forms.Form):
    search = forms.CharField(max_length=20)
