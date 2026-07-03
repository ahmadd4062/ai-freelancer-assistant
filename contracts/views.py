from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Contract
from utils.ai_helper import generate_contract, render_to_pdf

@login_required
def contract_list(request):
    contracts = Contract.objects.filter(user=request.user)
    return render(request, 'contracts/list.html', {'contracts': contracts})

@login_required
def contract_create(request):
    if request.method == 'POST':
        contract = Contract.objects.create(
            user=request.user,
            client_name=request.POST.get('client_name'),
            client_email=request.POST.get('client_email'),
            client_company=request.POST.get('client_company'),
            freelancer_name=request.POST.get('freelancer_name'),
            freelancer_email=request.POST.get('freelancer_email'),
            project_title=request.POST.get('project_title'),
            project_scope=request.POST.get('project_scope'),
            timeline=request.POST.get('timeline'),
            payment_terms=request.POST.get('payment_terms'),
            total_amount=request.POST.get('total_amount'),
            terms_conditions=request.POST.get('terms_conditions'),
            start_date=request.POST.get('start_date'),
            end_date=request.POST.get('end_date'),
            status=request.POST.get('status', 'draft')
        )
        messages.success(request, 'Contract created successfully!')
        return redirect('contract_detail', pk=contract.pk)
    return render(request, 'contracts/create.html')

@login_required
def contract_detail(request, pk):
    contract = get_object_or_404(Contract, pk=pk, user=request.user)
    return render(request, 'contracts/detail.html', {'contract': contract})

@login_required
def contract_edit(request, pk):
    contract = get_object_or_404(Contract, pk=pk, user=request.user)
    
    if request.method == 'POST':
        contract.client_name = request.POST.get('client_name')
        contract.client_email = request.POST.get('client_email')
        contract.client_company = request.POST.get('client_company')
        contract.freelancer_name = request.POST.get('freelancer_name')
        contract.freelancer_email = request.POST.get('freelancer_email')
        contract.project_title = request.POST.get('project_title')
        contract.project_scope = request.POST.get('project_scope')
        contract.timeline = request.POST.get('timeline')
        contract.payment_terms = request.POST.get('payment_terms')
        contract.total_amount = request.POST.get('total_amount')
        contract.terms_conditions = request.POST.get('terms_conditions')
        contract.start_date = request.POST.get('start_date')
        contract.end_date = request.POST.get('end_date')
        contract.status = request.POST.get('status', 'draft')
        contract.save()
        
        messages.success(request, 'Contract updated successfully!')
        return redirect('contract_detail', pk=contract.pk)
    
    return render(request, 'contracts/edit.html', {'contract': contract})

@login_required
def contract_delete(request, pk):
    contract = get_object_or_404(Contract, pk=pk, user=request.user)
    if request.method == 'POST':
        contract.delete()
        messages.success(request, 'Contract deleted successfully!')
        return redirect('contract_list')
    return render(request, 'contracts/delete.html', {'contract': contract})

@login_required
def contract_generate(request, pk):
    contract = get_object_or_404(Contract, pk=pk, user=request.user)
    
    # Check if user has AI credits
    if request.user.profile.ai_credits <= 0:
        messages.error(request, 'You have no AI credits left. Please contact support.')
        return redirect('contract_detail', pk=contract.pk)
    
    if request.method == 'POST':
        # Generate contract using AI
        generated_content = generate_contract(contract)
        
        # Save generated content
        contract.generated_contract = generated_content
        contract.save()
        
        # Deduct 1 AI credit
        request.user.profile.ai_credits -= 1
        request.user.profile.save()
        
        messages.success(request, 'Contract generated successfully! 1 AI credit used.')
        return redirect('contract_detail', pk=contract.pk)
    
    return render(request, 'contracts/generate.html', {'contract': contract})

@login_required
def contract_pdf(request, pk):
    contract = get_object_or_404(Contract, pk=pk, user=request.user)
    context = {'contract': contract}
    return render_to_pdf('contracts/pdf_template.html', context)