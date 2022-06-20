from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from products.models import Product
from products.constants import WEBSITE_CHOICES


class ProductForm(forms.ModelForm):
    url = forms.CharField(max_length=1000)
    class Meta:
        model = Product
        fields = ['url', 'site', 'name', 'category', 'price', 'target_price']
        # widgets = {
        #     'body': forms.TextInput(attrs={'placeholder': 'What\'s happening?'}),
        # }


class ProductCustomForm(forms.Form):
    name = forms.CharField(
        label='Product Name'
    )
    url = forms.CharField(
        label='Product Url',
        max_length=1000
    )
    website = forms.TypedChoiceField(
        label='Website',
        choices=WEBSITE_CHOICES,
        # coerce=
        widget=forms.RadioSelect
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'product_add'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = ''

        self.helper.add_input(Submit('submit', 'Submit'))
