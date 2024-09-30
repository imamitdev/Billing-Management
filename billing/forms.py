from django import forms
from .models import Product,Customer,InvoiceItem,Invoice,Payment
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
    
    

class PaymentForm(forms.ModelForm):
    payment_date = forms.DateTimeField(
        widget=forms.TextInput(attrs={
            'class': 'form-control datetimepicker',
            'placeholder': 'YYYY-MM-DD HH:MM',
        }),
        input_formats=['%Y-%m-%d %H:%M', '%Y-%m-%d'],  # Accept both date and datetime formats
    )

    class Meta:
        model = Payment
        fields = ['amount', 'payment_date', 'payment_method', 'note']  # Ensure 'invoice' is not included
        widgets = {
            "amount": forms.TextInput(attrs={"class": "form-control"}),
            "payment_method": forms.Select(attrs={"class": "form-control"}),
            'note': forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }
        
class PaymentFilterForm(forms.Form):
    customer = forms.ModelChoiceField(
        queryset=Customer.objects.all(), 
        required=False, 
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control datetimepicker'}),
        required=False
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control datetimepicker'}),
        required=False
    )