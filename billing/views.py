from django.shortcuts import render, redirect, get_object_or_404
from .models import Product,Customer,Invoice,InvoiceItem,Payment
from decimal import Decimal
import csv

from django.db.models import Sum, F

from .forms import ProductForm,CustomerForm,ProductImportForm,PaymentForm
from django.contrib import messages
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime,date



@login_required(login_url="login")
def product_list(request):
    products = Product.objects.all()

    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        if product_id:
            # Edit existing product
            product = get_object_or_404(Product, pk=product_id)
            form = ProductForm(request.POST, instance=product)
        else:
            # Create new product
            form = ProductForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('product_list')  # Redirect to the list after saving
    else:
        form = ProductForm()  # Empty form for new product

    return render(request, 'billing/product_list.html', {'products': products, 'form': form})

@login_required(login_url="login")
def edit_product(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id)

        product.name = request.POST.get('name')
        product.hsn_no = request.POST.get('hsn_no')
        product.mrp = request.POST.get('mrp')
        product.purchase_price = request.POST.get('purchase_price')
        product.sgst_rate = request.POST.get('sgst_rate')
        product.cgst_rate = request.POST.get('cgst_rate')
        product.stock_quantity = request.POST.get('stock_quantity')
        
        product.save()
        messages.success(request, 'Product updated successfully!')
        return redirect('product_list')

@login_required(login_url="login")
def delete_product(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id)

        # Delete the product
        product.delete()
        return redirect('product_list')

    return redirect('product_list')


@login_required(login_url="login")
def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm()
    return render(request, 'billing/customer_form.html', {'form': form})

@login_required(login_url="login")
def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'billing/customer_list.html', {'customers': customers})
@login_required(login_url="login")
def update_customer(request,customer_id):
    customer=get_object_or_404(Customer,id=customer_id)
    if request.method == 'POST':
        form = CustomerForm(request.POST , instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'billing/customer_form.html', {'form': form})


@login_required(login_url="login")
def add_invoice(request):
 

  

    # Pass customers to the template
    customers = Customer.objects.all()
    products = Product.objects.all()
    return render(request, 'billing/addInvoice.html', {'customers': customers, 'products': products})

@login_required(login_url="login")
@csrf_exempt
def create_invoice(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            customer_id = data.get('customer')
            manual_amount = Decimal(data.get('manual_amount', 0))  # Fixed this line
            total_amount = Decimal(data.get('total_amount', 0))  # Fixed this line
            total_sgst = Decimal(data.get('total_sgst', 0))  # Fixed this line
            total_cgst = Decimal(data.get('total_cgst', 0))  # Fixed this line

            print(total_amount)
            items = data.get('items', [])

            # Get the customer and create the invoice
            customer = get_object_or_404(Customer, id=customer_id)
            invoice = Invoice.objects.create(customer=customer, total_amount=total_amount, paid_amount=manual_amount,total_sgst=total_sgst,total_cgst=total_cgst)

            # Create invoice items
            for item in items:
                product_id = item.get('product')
                quantity = Decimal(item.get('quantity', 0))
                price = Decimal(item.get('price', 0))
                amount = Decimal(item.get('amount', 0))
                current_amount = Decimal(item.get('current_amount', 0))

                discount = Decimal(item.get('discount', 0))

                product = get_object_or_404(Product, id=product_id)
                InvoiceItem.objects.create(
                    invoice=invoice,
                    product=product,
                    quantity=quantity,
                    amount=current_amount,
                    price=price,
                    total_price=amount,
                    sgst=product.sgst_rate,
                    cgst=product.cgst_rate
                )
            invoice.paid_amount = float(manual_amount)

            invoice.save()

            return JsonResponse({'status': 'success'}, status=200)

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


@login_required(login_url="login")
def invoice_special(request):
 

  

    # Pass customers to the template
    customers = Customer.objects.all()
    products = Product.objects.all()
    return render(request, 'billing/specialbilling.html', {'customers': customers, 'products': products})

@csrf_exempt
def addInvoice_special(request):
    if request.method == 'POST':
        try:
            # Parse the form data from JSON
            data = json.loads(request.body)
            
            # Log the received data for debugging
            print("Received data:", data)

            # Get the customer
            customer_id = data.get('customer')
            customer = get_object_or_404(Customer, id=customer_id)

            # Create a new Invoice
            invoice = Invoice.objects.create(
                customer=customer,
                total_amount=data.get('taxable_amount',0),
                paid_amount=data.get('manual_amount', 0),
                # Add other fields if necessary
            )

            # Return a success response
            return JsonResponse({"message": "Invoice saved successfully!"}, status=200)

        except Exception as e:
            # Log the exception for easier debugging
            print("Error occurred:", str(e))
            return JsonResponse({"error": str(e)}, status=400)
    
    return JsonResponse({"error": "Invalid request method."}, status=400)
@login_required(login_url="login")
def invoice_list(request):
    invoices = Invoice.objects.annotate(
        due_amount=F('total_amount') - F('paid_amount')  # Calculate due amount dynamically
    )

    # Filter invoices where the due amount is greater than 0
    invoices_with_due = invoices.filter(due_amount__gt=0)

    

    context = {
        "invoices": invoices_with_due,  # Pass only invoices with a due amount > 0
    
    }

    return render(request, 'billing/Invoices.html', context)


@login_required(login_url="login")
def get_invoice(request, id):
    invoices = get_object_or_404(Invoice, id=id)
    invoice_items = InvoiceItem.objects.filter(invoice=invoices)
    
    # Calculate totals
    taxable_amount = sum(item.total_amount for item in invoice_items)
    cgst_total = sum(item.cgst for item in invoice_items)
    sgst_total = sum(item.sgst for item in invoice_items)
    total_price =  sum(item.total_price for item in invoice_items)
    due_amount = invoices.total_amount - invoices.paid_amount

    context = {
        'invoices': invoices,
        'invoice_item': invoice_items,
        'taxable_amount': taxable_amount,
        'cgst_total': cgst_total,
        'sgst_total': sgst_total,
        'total_price': total_price,
        "due_amount":due_amount,
    }
    
    return render(request, 'billing/view-invoice.html', context)




@login_required(login_url="login")
def import_products(request):
    if request.method == 'POST':
        form = ProductImportForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']

            # Check if the file is a CSV file
            if not file.name.endswith('.csv'):
                messages.error(request, 'This is not a CSV file')
                return redirect('import_products')

            try:
                # Decode the file to read the CSV
                decoded_file = file.read().decode('utf-8').splitlines()
                reader = csv.DictReader(decoded_file)

                # Iterate through the CSV and create Product objects
                for row in reader:
                    Product.objects.create(
                        name=row['name'],
                        hsn_no=row.get('hsn_no', ''),
                        mrp=row['mrp'],
                        purchase_price=row['purchase_price'],
                        sgst_rate=row.get('sgst_rate', 0.00),
                        cgst_rate=row.get('cgst_rate', 0.00),
                        stock_quantity=row['stock_quantity'],
                    )
                messages.success(request, 'Products imported successfully!')
                return redirect('product_list')

            except Exception as e:
                messages.error(request, f'Error processing file: {e}')
                return redirect('import_products')
    else:
        form = ProductImportForm()

    return render(request, 'billing/productimport.html', {'form': form})




@login_required(login_url="login")
def add_payment(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)

    if request.method == 'POST':
        # Collecting data from the form
        payment_date = request.POST.get('payment_date')
        amount = request.POST.get('amount')
        payment_method = request.POST.get('payment_method')
        note = request.POST.get('note')
        print(payment_date)
        print( timezone.datetime.strptime(payment_date, '%d-%m-%Y')
)
        # Validate the date format if needed
        try:
            payment_date = timezone.datetime.strptime(payment_date, '%d-%m-%Y')
        except ValueError:
            messages.error(request, 'Invalid date format. Please use YYYY-MM-DD.')
            return redirect('add_payment', invoice_id=invoice.id)
        amount = Decimal(amount)

        # Create a new payment instance
        payment = Payment(
            invoice=invoice,
            payment_date=payment_date,
            amount=amount,
            payment_method=payment_method,
            note=note
        )
        payment.save()

        # Update the invoice's paid amount after payment is made
        invoice.paid_amount += payment.amount
        invoice.save()

        messages.success(request, 'Payment added successfully!')
        return redirect('payment_report')

    return render(request, 'invoices/add-payment.html', {'invoice': invoice})


def payment_report(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    payments = Payment.objects.all()

    if start_date and end_date:
        try:
            # Parse the date strings into datetime objects
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d') + timezone.timedelta(days=1)  # Include end date
            payments = payments.filter(payment_date__range=(start_date, end_date))
        except ValueError:
            payments = []

    return render(request, 'reports/payments.html', {
        'payments': payments
    })




def customer_ledger(request, customer_id):
    # Get the customer
    customer = get_object_or_404(Customer, id=customer_id)
    
    # Get all invoices for the customer
    invoices = Invoice.objects.filter(customer=customer).only('id', 'date', 'total_amount')
    
    # Get all payments related to those invoices
    payments = Payment.objects.filter(invoice__customer=customer).only('id', 'payment_date', 'amount', 'invoice')
    
    # Initialize total variables using aggregate for performance
    total_invoiced = invoices.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    total_paid = payments.aggregate(Sum('amount'))['amount__sum'] or 0
    outstanding_balance = total_invoiced - total_paid

    # Prepare ledger entries combining invoices and payments
    ledger_entries = []
    
    # Add entries for each invoice, followed by payments for that invoice
    for invoice in invoices:
        # Add the invoice entry (Debit for the total invoiced amount)
        ledger_entries.append({
            'date': invoice.date,
            'description': f"Invoice #{invoice.id}",
            'debit': invoice.total_amount,  # Total amount invoiced
            'credit': None,
            'balance': None  # Running balance to be calculated later
        })

        # Get all payments made towards this invoice
        invoice_payments = payments.filter(invoice=invoice)

        # Add individual payment entries as credits below the invoice
        for payment in invoice_payments:
            ledger_entries.append({
                'date': payment.payment_date.date(),  # Convert datetime to date
                'description': f"Payment #{payment.id} for Invoice #{invoice.id}",
                'debit': None,
                'credit': payment.amount,
                'balance': None  # Running balance to be calculated later
            })

    # Sort ledger entries by date
    ledger_entries.sort(key=lambda x: x['date'] or date.min)

    # Calculate running balance
    running_balance = 0
    for entry in ledger_entries:
        if entry['debit']:
            running_balance += entry['debit']
        if entry['credit']:
            running_balance -= entry['credit']
        entry['balance'] = running_balance

    context = {
        'customer': customer,
        'ledger_entries': ledger_entries,
        'total_invoiced': total_invoiced,
        'total_paid': total_paid,
        'outstanding_balance': outstanding_balance,
    }

    return render(request, 'customer/customer-detail.html', context)
