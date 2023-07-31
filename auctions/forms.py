from django import forms
from .models import Listing, Category, Bid


class ListingForm(forms.ModelForm):
    #categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), widget=forms.CheckboxSelectMultiple())
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        required=True,
        widget=forms.CheckboxSelectMultiple
    )
    class Meta:
        model = Listing
        fields = ['title', 'description', 'image', 'categories']

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['amount']