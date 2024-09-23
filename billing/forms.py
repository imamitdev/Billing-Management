from django import forms
from .models import Product,Customer,InvoiceItem,Invoice
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'hsn_no','mrp','purchase_price', 'sgst_rate', 'cgst_rate', 'stock_quantity']
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "required": True}),
            "hsn_no": forms.TextInput(attrs={"class": "form-control"}),
            "mrp": forms.TextInput(attrs={"class": "form-control"}),
            "purchase_price": forms.TextInput(attrs={"class": "form-control"}),
            "sgst_rate": forms.TextInput(attrs={"class": "form-control"}),
            "cgst_rate": forms.TextInput(attrs={"class": "form-control"}),
            "stock_quantity": forms.TextInput(attrs={"class": "form-control"}),


        }



class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['customer_name', 'mobile_number','address']
        widgets = {
            "customer_name": forms.TextInput(attrs={"class": "form-control", "required": True}),
            "mobile_number": forms.TextInput(attrs={"class": "form-control"}),
            "address": forms.Textarea(attrs={"class": "form-control"}),
       


        }
        
        
class ProductImportForm(forms.Form):
    file = forms.FileField()