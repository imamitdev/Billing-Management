from django.urls import path
from . import views

urlpatterns = [
    path('sales/', views.sales_report ,name='sales_report'),
    path('product-sale-report/', views.product_sale_report ,name='product_sale_report'),

    path('profit-loss-report/', views.profit_and_loss_report ,name='profit_loss_report'),
    path('expense-report/', views.expense_report ,name='expense_report'),

    path('tax-report/', views.tax_report ,name='tax_report'),
    path('today-payments-report/', views.today_payments_report ,name='today_payments_report'),

]