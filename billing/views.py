from django.shortcuts import render, redirect, get_object_or_404
from .models import Product,Customer,Invoice,InvoiceItem
from decimal import Decimal
import csv

from django.db.models import Sum, F

from .forms import ProductForm,CustomerForm,ProductImportForm
from django.contrib import messages
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required



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
def invoice_list(request):
    invoices = Invoice.objects.all()
    total_invoices = invoices.count()  # All invoices
    total_invoice_amount = invoices.aggregate(Sum('total_amount'))['total_amount__sum'] or 0

    paid_invoices = invoices.filter(total_amount=F('paid_amount')).count()  # Fully paid invoices
    paid_invoice_amount = invoices.aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0


    unpaid_invoices = invoices.filter(total_amount__gt=F('paid_amount')).count()  # Unpaid invoices
    unpaid_invoice_amount = invoices.filter(total_amount__gt=F('paid_amount')).aggregate(Sum('total_amount'))['total_amount__sum'] or 0

    # If you have a status field for cancelled invoices
   
    for invoice in invoices:
        invoice.due_amount = invoice.total_amount - invoice.paid_amount
    
    context={
        "invoices":invoices,
        'total_invoices': total_invoices,
        'total_invoice_amount': total_invoice_amount,
        'paid_invoices': paid_invoices,
        'paid_invoice_amount': paid_invoice_amount,
        'unpaid_invoices': unpaid_invoices,
        'unpaid_invoice_amount': unpaid_invoice_amount,
    
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
    total_price = sum(item.total_price for item in invoice_items)
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