from django.shortcuts import render, redirect, get_object_or_404
from .models import Product,Customer
from .forms import ProductForm,CustomerForm
from django.contrib import messages

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