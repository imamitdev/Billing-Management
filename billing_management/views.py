
from django.shortcuts import render
from billing.models import Product,Customer,Invoice,InvoiceItem
from decimal import Decimal

from django.db.models import Sum, F
def home(request):
    invoices = Invoice.objects.all()
    total_invoices = invoices.count()  # All invoices
    total_invoice_amount = invoices.aggregate(Sum('total_amount'))['total_amount__sum'] or 0

    paid_invoices = invoices.filter(total_amount=F('paid_amount')).count()  # Fully paid invoices
    paid_invoice_amount = invoices.filter(total_amount=F('paid_amount')).aggregate(Sum('total_amount'))['total_amount__sum'] or 0

    unpaid_invoices = invoices.filter(total_amount__gt=F('paid_amount')).count()  # Unpaid invoices
    unpaid_invoice_amount = invoices.filter(total_amount__gt=F('paid_amount')).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    customers = Customer.objects.all().count()

    
    
    context={
        "invoices":invoices,
        'total_invoices': total_invoices,
        
        'total_invoice_amount': total_invoice_amount,
        'paid_invoices': paid_invoices,
        'paid_invoice_amount': paid_invoice_amount,
        'unpaid_invoices': unpaid_invoices,
        'unpaid_invoice_amount': unpaid_invoice_amount,
        "customers":customers
    
    }
    return render(request, "home.html",context)