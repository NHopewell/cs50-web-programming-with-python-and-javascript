from django import forms
nums = '1 2 3 4 5 6 7'.split()
labs = ['Art & Collectibles', 'Clothing', 
'Electronics', 'Health & Beauty', 'Home & Yard', 
'Jewellery', 'Sporting Goods']

CATEGORY_CHOICES = list(zip(nums, labs))

class NewListingForm(forms.Form):
    title = forms.CharField(max_length=100, label="Listing Title")
    category = forms.ChoiceField(required=False, choices=CATEGORY_CHOICES)
    picture = forms.ImageField(required=False)
    description = forms.CharField(widget=forms.Textarea, label="Listing Description")
    starting_bid = forms.DecimalField(max_digits=8, decimal_places=2)
