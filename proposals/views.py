from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Proposal
from utils.ai_helper import generate_proposal, render_to_pdf, clean_ai_response  # Updated import

@login_required
def proposal_list(request):
    proposals = Proposal.objects.filter(user=request.user)
    return render(request, 'proposals/list.html', {'proposals': proposals})

@login_required
def proposal_create(request):
    if request.method == 'POST':
        proposal = Proposal.objects.create(
            user=request.user,
            client_name=request.POST.get('client_name'),
            project_title=request.POST.get('project_title'),
            project_description=request.POST.get('project_description'),
            skills=request.POST.get('skills'),
            budget=request.POST.get('budget'),
            timeline=request.POST.get('timeline'),
            tone=request.POST.get('tone', 'professional')
        )
        messages.success(request, 'Proposal created successfully!')
        return redirect('proposal_detail', pk=proposal.pk)
    return render(request, 'proposals/create.html')

@login_required
def proposal_detail(request, pk):
    proposal = get_object_or_404(Proposal, pk=pk, user=request.user)
    return render(request, 'proposals/detail.html', {'proposal': proposal})

@login_required
def proposal_edit(request, pk):
    proposal = get_object_or_404(Proposal, pk=pk, user=request.user)
    
    if request.method == 'POST':
        # Update proposal fields
        proposal.client_name = request.POST.get('client_name')
        proposal.project_title = request.POST.get('project_title')
        proposal.project_description = request.POST.get('project_description')
        proposal.skills = request.POST.get('skills')
        proposal.budget = request.POST.get('budget')
        proposal.timeline = request.POST.get('timeline')
        proposal.tone = request.POST.get('tone', 'professional')
        proposal.save()
        
        messages.success(request, 'Proposal updated successfully!')
        return redirect('proposal_detail', pk=proposal.pk)
    
    return render(request, 'proposals/edit.html', {'proposal': proposal})

@login_required
def proposal_delete(request, pk):
    proposal = get_object_or_404(Proposal, pk=pk, user=request.user)
    if request.method == 'POST':
        proposal.delete()
        messages.success(request, 'Proposal deleted successfully!')
        return redirect('proposal_list')
    return render(request, 'proposals/delete.html', {'proposal': proposal})

@login_required
def proposal_generate(request, pk):
    proposal = get_object_or_404(Proposal, pk=pk, user=request.user)
    
    # Check if user has AI credits
    if request.user.profile.ai_credits <= 0:
        messages.error(request, 'You have no AI credits left. Please contact support.')
        return redirect('proposal_detail', pk=proposal.pk)
    
    if request.method == 'POST':
        # Generate proposal using AI
        generated_content = generate_proposal(proposal)
        
        # Save generated content
        proposal.generated_content = generated_content
        proposal.save()
        
        # Deduct 1 AI credit
        request.user.profile.ai_credits -= 1
        request.user.profile.save()
        
        messages.success(request, 'Proposal generated successfully! 1 AI credit used.')
        return redirect('proposal_detail', pk=proposal.pk)
    
    return render(request, 'proposals/generate.html', {'proposal': proposal})

@login_required
def proposal_export_pdf(request, pk):
    proposal = get_object_or_404(Proposal, pk=pk, user=request.user)
    
    if not proposal.generated_content:
        messages.warning(request, 'Please generate the proposal content first.')
        return redirect('proposal_generate', pk=proposal.pk)
    
    # Clean the content using the imported function
    clean_content = clean_ai_response(proposal.generated_content)
    
    context = {
        'proposal': proposal,
        'clean_content': clean_content
    }
    return render_to_pdf('proposals/pdf_template.html', context)