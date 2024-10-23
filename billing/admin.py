from django.contrib import admin
from .models import Product, InvoiceItem, Invoice, Customer, Payment, Expense

# Customize Product Admin
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'hsn_no', 'mrp', 'purchase_price', 'stock_quantity', 'created_date', 'modified_date')
    search_fields = ('name', 'hsn_no')  # Fields you want to be searchable

# Customize Customer Admin
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'mobile_number', 'gst_no', 'address', 'created_date', 'modified_date')
    search_fields = ('customer_name', 'mobile_number', 'gst_no')  # Searching by customer name, mobile, and GST number

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'date', 'total_amount', 'paid_amount', 'created_date', 'modified_date')
    search_fields = ['id', 'customer__customer_name']  # Use a list or tuple here
    list_filter = ('date', 'customer')

# Customize InvoiceItem Admin
class InvoiceItemAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'product', 'quantity', 'price', 'total_amount', 'sgst', 'cgst', 'total_price', 'created_date', 'modified_date')
    search_fields = ('invoice__id', 'product__name')  # Searching by invoice ID or product name

# Customize Payment Admin
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'amount', 'payment_date', 'payment_method', 'note')
    search_fields = ('invoice__id', 'payment_method')  # Searching by invoice ID or payment method
    list_filter = ('payment_method', 'payment_date')  # Adding filter for payment method and date

# Customize Expense Admin
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('description', 'expense_type', 'amount', 'date', 'created_date', 'modified_date')
    search_fields = ('description', 'expense_type')  # Searching by description or expense type
    list_filter = ('expense_type', 'date')  # Adding filter for expense type and date

# Register models with the admin site
admin.site.register(Product, ProductAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(InvoiceItem, InvoiceItemAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Expense, ExpenseAdmin)
