from django import forms

class FormSearchArts(forms.Form):
    titulo = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={ 'class' : 'form-control' }))
