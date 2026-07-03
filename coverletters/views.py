from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CoverLetter
from utils.ai_helper import generate_cover_letter

@login_required
def coverletter_list(request):
    coverletters = CoverLetter.objects.filter(user=request.user)
    return render(request, 'coverletters/list.html', {'coverletters': coverletters})

@login_required
def coverletter_create(request):
    if request.method == 'POST':
        coverletter = CoverLetter.objects.create(
            user=request.user,
            job_title=request.POST.get('job_title'),
            company_name=request.POST.get('company_name'),
            experience=request.POST.get('experience'),
            skills=request.POST.get('skills'),
            portfolio_url=request.POST.get('portfolio_url'),
            tone=request.POST.get('tone', 'professional')
        )
        messages.success(request, 'Cover letter created successfully!')
        return redirect('coverletter_detail', pk=coverletter.pk)
    return render(request, 'coverletters/create.html')

@login_required
def coverletter_detail(request, pk):
    coverletter = get_object_or_404(CoverLetter, pk=pk, user=request.user)
    return render(request, 'coverletters/detail.html', {'coverletter': coverletter})

@login_required
def coverletter_edit(request, pk):
    coverletter = get_object_or_404(CoverLetter, pk=pk, user=request.user)
    
    if request.method == 'POST':
        # Update cover letter fields
        coverletter.job_title = request.POST.get('job_title')
        coverletter.company_name = request.POST.get('company_name')
        coverletter.experience = request.POST.get('experience')
        coverletter.skills = request.POST.get('skills')
        coverletter.portfolio_url = request.POST.get('portfolio_url')
        coverletter.tone = request.POST.get('tone', 'professional')
        coverletter.save()
        
        messages.success(request, 'Cover letter updated successfully!')
        return redirect('coverletter_detail', pk=coverletter.pk)
    
    return render(request, 'coverletters/edit.html', {'coverletter': coverletter})

@login_required
def coverletter_delete(request, pk):
    coverletter = get_object_or_404(CoverLetter, pk=pk, user=request.user)
    if request.method == 'POST':
        coverletter.delete()
        messages.success(request, 'Cover letter deleted successfully!')
        return redirect('coverletter_list')
    return render(request, 'coverletters/delete.html', {'coverletter': coverletter})

@login_required
def coverletter_generate(request, pk):
    coverletter = get_object_or_404(CoverLetter, pk=pk, user=request.user)
    
    # Check if user has AI credits
    if request.user.profile.ai_credits <= 0:
        messages.error(request, 'You have no AI credits left. Please contact support.')
        return redirect('coverletter_detail', pk=coverletter.pk)
    
    if request.method == 'POST':
        # Generate cover letter using AI
        generated_content = generate_cover_letter(coverletter)
        
        # Save generated content
        coverletter.generated_content = generated_content
        coverletter.save()
        
        # Deduct 1 AI credit
        request.user.profile.ai_credits -= 1
        request.user.profile.save()
        
        messages.success(request, 'Cover letter generated successfully! 1 AI credit used.')
        return redirect('coverletter_detail', pk=coverletter.pk)
    
    return render(request, 'coverletters/generate.html', {'coverletter': coverletter})