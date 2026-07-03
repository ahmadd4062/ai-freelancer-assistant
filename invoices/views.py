from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .models import Invoice
from utils.ai_helper import render_to_pdf
import datetime

@login_required
def invoice_list(request):
    invoices = Invoice.objects.filter(user=request.user)
    return render(request, 'invoices/list.html', {'invoices': invoices})

@login_required
def invoice_create(request):
    if request.method == 'POST':
        invoice = Invoice.objects.create(
            user=request.user,
            client_name=request.POST.get('client_name'),
            client_email=request.POST.get('client_email'),
            client_address=request.POST.get('client_address'),
            project_title=request.POST.get('project_title'),
            project_description=request.POST.get('project_description'),
            services=request.POST.get('services'),
            amount=request.POST.get('amount'),
            tax=request.POST.get('tax', 0),
            due_date=request.POST.get('due_date'),
            status=request.POST.get('status', 'draft')
        )
        messages.success(request, 'Invoice created successfully!')
        return redirect('invoice_detail', pk=invoice.pk)
    
    # Get today's date for default due date (30 days from now)
    today = datetime.date.today()
    default_due_date = today + datetime.timedelta(days=30)
    
    return render(request, 'invoices/create.html', {
        'default_due_date': default_due_date.isoformat()
    })

@login_required
def invoice_detail(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk, user=request.user)
    return render(request, 'invoices/detail.html', {'invoice': invoice})

@login_required
def invoice_edit(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk, user=request.user)
    
    if request.method == 'POST':
        invoice.client_name = request.POST.get('client_name')
        invoice.client_email = request.POST.get('client_email')
        invoice.client_address = request.POST.get('client_address')
        invoice.project_title = request.POST.get('project_title')
        invoice.project_description = request.POST.get('project_description')
        invoice.services = request.POST.get('services')
        invoice.amount = request.POST.get('amount')
        invoice.tax = request.POST.get('tax', 0)
        invoice.due_date = request.POST.get('due_date')
        invoice.status = request.POST.get('status', 'draft')
        invoice.save()
        
        messages.success(request, 'Invoice updated successfully!')
        return redirect('invoice_detail', pk=invoice.pk)
    
    return render(request, 'invoices/edit.html', {'invoice': invoice})

@login_required
def invoice_delete(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk, user=request.user)
    if request.method == 'POST':
        invoice.delete()
        messages.success(request, 'Invoice deleted successfully!')
        return redirect('invoice_list')
    return render(request, 'invoices/delete.html', {'invoice': invoice})

@login_required
def invoice_pdf(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk, user=request.user)
    context = {
        'invoice': invoice,
        'user': request.user,  
    }
    return render_to_pdf('invoices/pdf_template.html', context)