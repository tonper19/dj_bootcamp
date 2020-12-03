from django import forms
from .models import Product

# class ProductForm(forms.Form):
#     title = forms.CharField()


class ProductModelForm(forms.ModelForm):
    # title = forms.CharField()
    class Meta:
        model = Product
        fields = [
            "title",
            "content",
            "price",
        ]

    def clean_title(self):
        data = self.cleaned_data.get("title")
        if len(data) < 3:
            raise forms.ValidationError(
                "Title must be 3 or more characters long")
        return data
