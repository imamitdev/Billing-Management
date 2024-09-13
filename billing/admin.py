from django.contrib import admin

# Register your models here.
from .models import Product,InvoiceItem,Invoice,Customer


admin.site.register(Product)
admin.site.register(Invoice)
admin.site.register(InvoiceItem)
admin.site.register(Customer)