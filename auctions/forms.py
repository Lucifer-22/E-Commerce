from django import forms
from .models import Listing

class listing_form(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ('title', 'price', 'description', 'image', 'category')