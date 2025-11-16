from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from cashify_app.models import Device, Transaction
from django.contrib.auth.decorators import login_required
from django import forms

def home(request):
    return render(request, 'cashify_app/home.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created successfully! You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'cashify_app/register.html', {'form': form})

def device_list(request):
    devices = Device.objects.all()
    return render(request, 'cashify_app/devices.html', {'devices':devices})

class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['name', 'brand', 'condition', 'price', 'description','image']

@login_required
def device_create(request):
    if request.method == 'POST':
        form = DeviceForm(request.POST)
        if form.is_valid():
            device = form.save(commit=False)
            device.owner = request.user
            device.save()
            return redirect('device_list')
    else:
        form = DeviceForm()
    return render(request, 'cashify_app/device_form.html', {'form': form})

def device_detail(request, pk):
    device = get_object_or_404(Device, pk=pk)
    return render(request, 'cashify_app/device_detail.html', {'device': device})


@login_required
def device_update(request, pk):
    device = get_object_or_404(Device, pk=pk)
    if device.owner != request.user:
        # Prevent editing others' devices (optional security check)
        return redirect('device_detail', pk=pk)
    if request.method == 'POST':
        form = DeviceForm(request.POST, instance=device)
        if form.is_valid():
            form.save()
            return redirect('device_detail', pk=device.pk)
    else:
        form = DeviceForm(instance=device)
    return render(request, 'cashify_app/device_form.html', {'form': form, 'edit_mode': True})

@login_required
def device_delete(request, pk):
    device = get_object_or_404(Device, pk=pk)
    if device.owner != request.user:
        return redirect('device_detail', pk=pk)
    if request.method == 'POST':
        device.delete()
        return redirect('device_list')
    return render(request, 'cashify_app/delete_confirm.html', {'device': device})


@login_required
def create_transaction(request, pk):
    device = get_object_or_404(Device, pk=pk)
    if device.owner == request.user:
        return redirect('device_detail', pk=pk)  # Prevent self-purchase
    transaction = Transaction.objects.create(
        device=device,
        buyer=request.user,
        seller=device.owner,
        status='Pending'
    )
    # Optional: Update device status (e.g., sold)
    device.status = 'Sold'
    device.save()
    return render(request, 'cashify_app/transaction.html', {'transaction': transaction})

@login_required
def transaction_list(request):
    transactions = Transaction.objects.filter(buyer=request.user) | Transaction.objects.filter(seller=request.user)
    return render(request, 'cashify_app/transactions_list.html', {'transactions': transactions})
