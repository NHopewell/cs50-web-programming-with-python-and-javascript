from django import forms

class NewListingForm(forms.Form):
    title = forms.CharField(max_length=100, label="Listing Title")
    description = forms.CharField(widget=forms.Textarea, label="Listing Description")
    starting_bid = forms.DecimalField(max_digits=8, decimal_places=2)
