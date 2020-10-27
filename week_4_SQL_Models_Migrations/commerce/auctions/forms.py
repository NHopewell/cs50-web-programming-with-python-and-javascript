from django import forms

from .models import Listing

class NewListingForm(forms.ModelForm):

    class Meta:
        model = Listing
        fields = ["title", "category", "image", "description", "starting_bid"]

    """    
    title = forms.CharField(max_length=100, label="Listing Title")
    category = forms.ChoiceField(required=False, choices=CATEGORY_CHOICES)
    image = forms.ImageField(required=False)
    description = forms.CharField(widget=forms.Textarea, label="Listing Description")
    starting_bid = forms.DecimalField(max_digits=8, decimal_places=2)
    """