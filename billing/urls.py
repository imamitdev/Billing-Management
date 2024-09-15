
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

    path('invoices/', views.invoice_list, name='invoice_list'),

]
