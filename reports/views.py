
from django.shortcuts import render
from billing.models import Invoice, Payment,Expense,InvoiceItem
from .forms import ReportForm
from django.db.models import Sum
from django.utils import timezone

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





def profit_loss_report(request):
    form = ReportForm(request.GET or None)
    total_revenue = 0
    total_expenses = 0
    profit_or_loss = 0
    expenses = []
    invoices = []

    if form.is_valid():
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']

        # Total Revenue from Invoices
        invoices = Invoice.objects.filter(date__range=[start_date, end_date])
        total_revenue = invoices.aggregate(Sum('total_amount'))['total_amount__sum'] or 0

        # Total Expenses from the Expense model
        expenses = Expense.objects.filter(date__range=[start_date, end_date])
        total_expenses = expenses.aggregate(Sum('amount'))['amount__sum'] or 0

        # Profit or Loss calculation
        profit_or_loss = total_revenue - total_expenses

    context = {
        'form': form,
        'invoices': invoices,
        'expenses': expenses,
        'total_revenue': total_revenue,
        'total_expenses': total_expenses,
        'profit_or_loss': profit_or_loss,
    }
    return render(request, 'profit_loss_report.html', context)



def tax_report(request):
    
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')
    start_date = timezone.datetime.strptime(start_date, '%d-%m-%Y')
    end_date = timezone.datetime.strptime(end_date, '%d-%m-%Y')

    total_sgst = 0
    total_cgst = 0
    invoice_items = []

   


        # Filter InvoiceItems based on invoice date range
    invoice_items = InvoiceItem.objects.filter(invoice__date__range=[start_date, end_date])

        # Calculate total SGST and CGST
    total_sgst = invoice_items.aggregate(Sum('sgst'))['sgst__sum'] or 0
    total_cgst = invoice_items.aggregate(Sum('cgst'))['cgst__sum'] or 0

    context = {
        'invoice_items': invoice_items,
        'total_sgst': total_sgst,
        'total_cgst': total_cgst,
    }
    return render(request, 'tax_report.html', context)