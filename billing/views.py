from django.shortcuts import render, redirect, get_object_or_404
from .models import Product,Customer,Invoice,InvoiceItem
from decimal import Decimal

from django.db.models import Sum, F

from .forms import ProductForm,CustomerForm
from django.contrib import messages
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
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

def delete_product(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id)

        # Delete the product
        product.delete()
        return redirect('product_list')

    return redirect('product_list')


def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm()
    return render(request, 'billing/customer_form.html', {'form': form})

def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'billing/customer_list.html', {'customers': customers})
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


def add_invoice(request):
 

  

    # Pass customers to the template
    customers = Customer.objects.all()
    products = Product.objects.all()
    return render(request, 'billing/addInvoice.html', {'customers': customers, 'products': products})

@csrf_exempt
def create_invoice(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            customer_id = data.get('customer')
            manual_amount = Decimal(data.get('manual_amount', 0))  # Fixed this line

            items = data.get('items', [])

            # Get the customer and create the invoice
            customer = get_object_or_404(Customer, id=customer_id)
            invoice = Invoice.objects.create(customer=customer, total_amount=0, paid_amount=manual_amount)
            total_amount = Decimal('0.00')

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
                total_amount += amount
            invoice.total_amount = total_amount
            invoice.paid_amount = float(manual_amount)

            invoice.save()

            return JsonResponse({'status': 'success'}, status=200)

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)



def invoice_list(request):
    invoices = Invoice.objects.all()
    total_invoices = invoices.count()  # All invoices
    total_invoice_amount = invoices.aggregate(Sum('total_amount'))['total_amount__sum'] or 0

    paid_invoices = invoices.filter(total_amount=F('paid_amount')).count()  # Fully paid invoices
    paid_invoice_amount = invoices.filter(total_amount=F('paid_amount')).aggregate(Sum('total_amount'))['total_amount__sum'] or 0

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

def get_invoice(request,id):
    invoices = get_object_or_404(Invoice, id=id)
    invoice_items = InvoiceItem.objects.filter(invoice=invoices)
    

    context={
        'invoices': invoices,
        'invoice_item': invoice_items

    }
    return render(request,'billing/view-invoice.html', context)