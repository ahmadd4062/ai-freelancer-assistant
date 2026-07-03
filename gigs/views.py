from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import GigDescription
from utils.ai_helper import generate_gig_description

@login_required
def gig_list(request):
    gigs = GigDescription.objects.filter(user=request.user)
    return render(request, 'gigs/list.html', {'gigs': gigs})

@login_required
def gig_create(request):
    if request.method == 'POST':
        gig = GigDescription.objects.create(
            user=request.user,
            service_category=request.POST.get('service_category'),
            skills=request.POST.get('skills'),
            experience_level=request.POST.get('experience_level', 'intermediate'),
            delivery_time=request.POST.get('delivery_time'),
            features=request.POST.get('features'),
            revisions=request.POST.get('revisions', 1)
        )
        messages.success(request, 'Gig description created successfully!')
        return redirect('gig_detail', pk=gig.pk)
    return render(request, 'gigs/create.html')

@login_required
def gig_detail(request, pk):
    gig = get_object_or_404(GigDescription, pk=pk, user=request.user)
    return render(request, 'gigs/detail.html', {'gig': gig})

@login_required
def gig_edit(request, pk):
    gig = get_object_or_404(GigDescription, pk=pk, user=request.user)
    
    if request.method == 'POST':
        gig.service_category = request.POST.get('service_category')
        gig.skills = request.POST.get('skills')
        gig.experience_level = request.POST.get('experience_level', 'intermediate')
        gig.delivery_time = request.POST.get('delivery_time')
        gig.features = request.POST.get('features')
        gig.revisions = request.POST.get('revisions', 1)
        gig.save()
        
        messages.success(request, 'Gig description updated successfully!')
        return redirect('gig_detail', pk=gig.pk)
    
    return render(request, 'gigs/edit.html', {'gig': gig})

@login_required
def gig_delete(request, pk):
    gig = get_object_or_404(GigDescription, pk=pk, user=request.user)
    if request.method == 'POST':
        gig.delete()
        messages.success(request, 'Gig description deleted successfully!')
        return redirect('gig_list')
    return render(request, 'gigs/delete.html', {'gig': gig})

@login_required
def gig_generate(request, pk):
    gig = get_object_or_404(GigDescription, pk=pk, user=request.user)
    
    # Check if user has AI credits
    if request.user.profile.ai_credits <= 0:
        messages.error(request, 'You have no AI credits left. Please contact support.')
        return redirect('gig_detail', pk=gig.pk)
    
    if request.method == 'POST':
        # Generate gig description using AI
        generated_data = generate_gig_description(gig)
        
        # Save generated content
        gig.generated_description = generated_data.get('description', '')
        gig.seo_keywords = generated_data.get('seo_keywords', '')
        gig.faq_suggestions = generated_data.get('faq_suggestions', '')
        gig.save()
        
        # Deduct 1 AI credit
        request.user.profile.ai_credits -= 1
        request.user.profile.save()
        
        messages.success(request, 'Gig description generated successfully! 1 AI credit used.')
        return redirect('gig_detail', pk=gig.pk)
    
    return render(request, 'gigs/generate.html', {'gig': gig})