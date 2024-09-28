
from django.shortcuts import render
from billing.models import Product,Customer,Invoice,InvoiceItem
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Sum, F

@login_required(login_url="login")
def home(request):
    current_date = timezone.now()
    first_day_current_month = current_date.replace(day=1)
    customers = Customer.objects.all().count()
    total_invoices = Invoice.objects.count()
    total_paid_amount = Invoice.objects.aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
    total_amount = Invoice.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    total_due_amount = total_amount - total_paid_amount
    # Amounts for current month
    current_month_amount = Invoice.objects.filter(date__gte=first_day_current_month).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    
    # Amount for previous month
    first_day_previous_month = first_day_current_month - timezone.timedelta(days=1)
    first_day_previous_month = first_day_previous_month.replace(day=1)
    last_day_previous_month = first_day_current_month - timezone.timedelta(days=1)

    previous_month_amount = Invoice.objects.filter(date__gte=first_day_previous_month, date__lte=last_day_previous_month).aggregate(Sum('total_amount'))['total_amount__sum'] or 0

    context = {
        "customers":customers,

        'total_invoices': total_invoices,
        'total_paid_amount': total_paid_amount,
        'total_amount': total_amount,
        'total_due_amount': total_due_amount,
        'current_month_amount': current_month_amount,
        'previous_month_amount': previous_month_amount,
    }
    
    return render(request, "home.html",context)