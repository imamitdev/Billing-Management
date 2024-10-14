from django.urls import path
from . import views

urlpatterns = [
    path('sales/', views.sales_report ,name='sales_report'),
        path('product-sale-report/', views.product_sale_report ,name='product_sale_report'),

    path('profit-loss-report/', views.profit_loss_report ,name='profit_loss_report'),
    path('tax-report/', views.tax_report ,name='tax_report'),

]