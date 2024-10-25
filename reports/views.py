
from django.shortcuts import render
from billing.models import Invoice, Payment,Expense,InvoiceItem
from .forms import ReportForm
from django.db.models import Sum
from django.utils import timezone
from datetime import datetime



def parse_date(date_str):
    return datetime.strptime(date_str, '%d-%m-%Y')
def product_sale_report(request):
    product_sales = []

    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        start_date = timezone.datetime.strptime(start_date, '%d-%m-%Y')
        end_date = timezone.datetime.strptime(end_date, '%d-%m-%Y')
        # Aggregate total quantity sold and total revenue per product
        product_sales = InvoiceItem.objects.filter(invoice__date__range=[start_date, end_date]) 
    context = {
        'product_sales': product_sales,
    }
    return render(request, 'product_sale_report.html', context)
def sales_report(request):
    invoices = []
    total_sales = 0
    total_paid = 0
    total_sgst = 0
    total_cgst = 0

    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        start_date = timezone.datetime.strptime(start_date, '%d-%m-%Y')
        end_date = timezone.datetime.strptime(end_date, '%d-%m-%Y')

        # Get invoices within the date range
        invoices = Invoice.objects.filter(date__range=[start_date, end_date])

        # Aggregate total amounts
        total_sales = invoices.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        total_paid = invoices.aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
        total_sgst = invoices.aggregate(Sum('total_sgst'))['total_sgst__sum'] or 0
        total_cgst = invoices.aggregate(Sum('total_cgst'))['total_cgst__sum'] or 0

    context = {
        'invoices': invoices,
        'total_sales': total_sales,
        'total_paid': total_paid,
        'total_sgst': total_sgst,
        'total_cgst': total_cgst,
    }
    return render(request, 'sales.html', context)

def expense_report(request):
    expenses = []
    total_purchase = total_operational = total_other = total_expenses = 0

    if request.method == 'POST':
        start_date = parse_date(request.POST.get('start_date'))
        end_date = parse_date(request.POST.get('end_date'))

        # Filter expenses by date range
        expenses = Expense.objects.filter(date__range=[start_date, end_date])

        # Aggregate totals by expense type
        total_purchase = expenses.filter(expense_type='purchase').aggregate(Sum('amount'))['amount__sum'] or 0
        total_operational = expenses.filter(expense_type='operational').aggregate(Sum('amount'))['amount__sum'] or 0
        total_other = expenses.filter(expense_type='other').aggregate(Sum('amount'))['amount__sum'] or 0
        total_expenses = total_purchase + total_operational + total_other

    context = {
        'expenses': expenses,
        'total_purchase': total_purchase,
        'total_operational': total_operational,
        'total_other': total_other,
        'total_expenses': total_expenses,
    }
    return render(request, 'expense.html', context)


def profit_and_loss_report(request):
    total_revenue = 0
    total_expenses = 0
    profit = 0
    loss = 0
    invoices = []
    expenses = []

    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        # Convert string dates to datetime objects
        start_date = timezone.datetime.strptime(start_date, '%d-%m-%Y').date()
        end_date = timezone.datetime.strptime(end_date, '%d-%m-%Y').date()

        # Calculate total revenue from invoices
        total_revenue = Invoice.objects.filter(date__range=(start_date, end_date)).aggregate(Sum('total_amount'))['total_amount__sum'] or 0

        # Calculate total expenses
        total_expenses = Expense.objects.filter(date__range=(start_date, end_date)).aggregate(Sum('amount'))['amount__sum'] or 0

        # Calculate profit and loss
        if total_revenue > total_expenses:
            profit = total_revenue - total_expenses
        else:
            loss = total_expenses - total_revenue

        # Get list of invoices for display
        invoices = Invoice.objects.filter(date__range=(start_date, end_date))
        expenses = Expense.objects.filter(date__range=(start_date, end_date))

    context = {
        'total_revenue': total_revenue,
        'total_expenses': total_expenses,
        'profit': profit,
        'loss': loss,
        'invoices': invoices,
        'expenses': expenses,
    }
    return render(request, 'profit_loss_report.html', context)

def tax_report(request):
    total_sgst = 0
    total_cgst = 0
    invoices = []

    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        start_date = timezone.datetime.strptime(start_date, '%d-%m-%Y')
        end_date = timezone.datetime.strptime(end_date, '%d-%m-%Y')   

        # Filter Invoices based on date range
        invoices = Invoice.objects.filter(date__range=[start_date, end_date])

        # Calculate total SGST and CGST
        total_sgst = invoices.aggregate(Sum('sgst'))['sgst__sum'] or 0
        total_cgst = invoices.aggregate(Sum('cgst'))['cgst__sum'] or 0

    context = {
        'invoices': invoices,
        'total_sgst': total_sgst,
        'total_cgst': total_cgst,
    }
    return render(request, 'tax_report.html', context)

def today_payments_report(request):
    today = timezone.now().date()
    payments = Payment.objects.filter(payment_date__date=today)
    total_amount = payments.aggregate(total=Sum('amount'))['total'] or 0

    context = {
        'payments': payments,
        'total_amount': total_amount,
        'today': today,
    }
    return render(request, 'today_report.html', context)