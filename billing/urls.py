
from django.urls import path
from . import views

urlpatterns = [
    path('product/', views.product_list ,name='product_list'),
    path('edit-product/', views.edit_product, name='edit_product'),

    path('delete-product/', views.delete_product, name='delete_product'),

    path('customer_list/', views.customer_list ,name='customer_list'),
    path('customers/new/', views.customer_create, name='customer_create'),
    path('customers/edit/<int:customer_id>/', views.update_customer, name='update_customer'),

    path('addInovice/', views.add_invoice ,name='add_invoice'),
    path('create_invoice/', views.create_invoice ,name='create_invoice'),
    path('invoice_special/', views.invoice_special ,name='invoice_special'),
    path('addInvoice_special/', views.addInvoice_special ,name='addInvoice_special'),


    path('invoices/', views.invoice_list, name='invoice_list'),
    path('view-invoice/<int:id>/', views.get_invoice, name='get_invoice'),
    path('import_products/', views.import_products, name='import_products'),
    path('payments/add/<int:invoice_id>/', views.add_payment, name='add_payment'),
    path('report/payments/', views.payment_report, name='payment_report'),
    path('customer/<int:customer_id>/get/', views.customer_ledger, name='customer_get'),

    path('expense/', views.expense_list ,name='expense_list'),
    path('edit-expense/', views.edit_expense, name='edit_expense'),

    path('delete-expense/', views.delete_expense, name='delete_expense'),

]
