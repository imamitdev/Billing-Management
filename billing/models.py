from django.db import models
from django.utils import timezone
# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255)
    hsn_no= models.CharField(max_length=100,blank=True)
    mrp = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    sgst_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)  # Default SGST 9%
    cgst_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)  # Default CGST 9%
    stock_quantity = models.IntegerField(default=0)
    created_date = models.DateTimeField(default=timezone.now)  # Use default
    modified_date = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

    def get_total_tax(self):
        return self.sgst_rate + self.cgst_rate
    
class Customer(models.Model):
    customer_name=models.CharField(max_length=255)
    mobile_number=models.CharField(max_length=50)
    address = models.CharField(max_length=250, blank=True)
    created_date = models.DateTimeField(default=timezone.now)  # Use default
    modified_date = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.customer_name


class Invoice(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,null=True)
    date = models.DateField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_sgst=models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_cgst=models.DecimalField(max_digits=10, decimal_places=2, default=0)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_date = models.DateTimeField(default=timezone.now)  # Use default
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Invoice {self.id} - {self.customer.customer_name}"

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    amount = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    sgst = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    cgst = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2,default=0)

    total_price = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    total_paid = models.DecimalField(max_digits=10, decimal_places=2,default=0)

    created_date = models.DateTimeField(default=timezone.now)  # Use default
    modified_date = models.DateTimeField(auto_now=True)
    def save(self, *args, **kwargs):
        # Calculate SGST and CGST
        self.total_amount = self.amount * self.quantity
        self.sgst = (self.product.sgst_rate / 100) * self.total_amount
        self.cgst = (self.product.cgst_rate / 100) * self.total_amount
        self.total_price = self.total_amount + self.sgst + self.cgst
        super().save(*args, **kwargs)
        
class Payment(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField()
    payment_method = models.CharField(max_length=50, choices=[('Cash', 'Cash'), ('Credit Card', 'Credit Card'), ('Bank Transfer', 'Bank Transfer')])
    note = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Payment of {self.amount} for Invoice {self.invoice.id}"

class Expense(models.Model):
    EXPENSE_TYPE_CHOICES = [
        ('purchase', 'Purchase'),
        ('operational', 'Operational'),
        ('other', 'Other'),
    ]
    
    expense_type = models.CharField(max_length=50, choices=EXPENSE_TYPE_CHOICES)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=timezone.now)
    
    created_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.description} - ₹{self.amount}"