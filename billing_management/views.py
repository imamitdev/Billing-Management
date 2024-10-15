
from django.shortcuts import render
from billing.models import Product,Customer,Invoice,InvoiceItem,Payment
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
    today = timezone.now().date()

    recent_invoices = Invoice.objects.filter(date=today)[:10]
    today_payments = Payment.objects.filter(payment_date__date=today)[:10]
    total_payment = today_payments.aggregate(total=Sum('amount'))['total'] or 0


    context = {
        "customers":customers,
        "recent_invoices":recent_invoices,
        "today_payments":today_payments,
        "total_payment":total_payment,
        'total_invoices': total_invoices,
        'total_paid_amount': total_paid_amount,
        'total_amount': total_amount,
        'total_due_amount': total_due_amount,
        'current_month_amount': current_month_amount,
        'previous_month_amount': previous_month_amount,
    }
    
    return render(request, "home.html",context)