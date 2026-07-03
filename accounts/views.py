from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
import os
from .models import Profile
from proposals.models import Proposal
from coverletters.models import CoverLetter
from gigs.models import GigDescription
from pricing.models import PricingHistory
from replies.models import ClientReply
from invoices.models import Invoice
from contracts.models import Contract


def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'accounts/home.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to AI Freelancer Assistant.')
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def dashboard(request):
    # Get counts for the current user
    proposal_count = Proposal.objects.filter(user=request.user).count()
    coverletter_count = CoverLetter.objects.filter(user=request.user).count()
    gig_count = GigDescription.objects.filter(user=request.user).count()
    pricing_count = PricingHistory.objects.filter(user=request.user).count()
    reply_count = ClientReply.objects.filter(user=request.user).count()  
    invoice_count = Invoice.objects.filter(user=request.user).count()  
    contract_count = Contract.objects.filter(user=request.user).count()  
    
    # Get recent activities (last 5 items across all types)
    recent_proposals = Proposal.objects.filter(user=request.user).order_by('-created_at')[:3]
    recent_coverletters = CoverLetter.objects.filter(user=request.user).order_by('-created_at')[:3]
    recent_gigs = GigDescription.objects.filter(user=request.user).order_by('-created_at')[:3]
    recent_pricing = PricingHistory.objects.filter(user=request.user).order_by('-created_at')[:3]
    recent_replies = ClientReply.objects.filter(user=request.user).order_by('-created_at')[:3]
    recent_invoices = Invoice.objects.filter(user=request.user).order_by('-created_at')[:3]
    recent_contracts = Contract.objects.filter(user=request.user).order_by('-created_at')[:3]
    
    # Combine and sort by created_at
    recent_activities = []
    
    for p in recent_proposals:
        recent_activities.append({
            'type': 'proposal',
            'title': p.project_title,
            'created_at': p.created_at,
            'url': f'/proposals/{p.pk}/'
        })
    for c in recent_coverletters:
        recent_activities.append({
            'type': 'coverletter',
            'title': f"{c.job_title} at {c.company_name}",
            'created_at': c.created_at,
            'url': f'/coverletters/{c.pk}/'
        })
    for g in recent_gigs:
        recent_activities.append({
            'type': 'gig',
            'title': g.service_category,
            'created_at': g.created_at,
            'url': f'/gigs/{g.pk}/'
        })
    for pr in recent_pricing:
        recent_activities.append({
            'type': 'pricing',
            'title': f"${pr.suggested_price} - {pr.get_complexity_display()}",
            'created_at': pr.created_at,
            'url': f'/pricing/{pr.pk}/'
        })
    for r in recent_replies:
        recent_activities.append({
            'type': 'reply',
            'title': r.client_message[:50] + '...' if len(r.client_message) > 50 else r.client_message,
            'created_at': r.created_at,
            'url': f'/replies/{r.pk}/'
        })
    for i in recent_invoices:
        recent_activities.append({
            'type': 'invoice',
            'title': f"{i.invoice_number} - {i.client_name}",
            'created_at': i.created_at,
            'url': f'/invoices/{i.pk}/'
        })
    for con in recent_contracts:
        recent_activities.append({
            'type': 'contract',
            'title': f"{con.contract_number} - {con.client_name}",
            'created_at': con.created_at,
            'url': f'/contracts/{con.pk}/'
        })
    
    # Sort by created_at (newest first)
    recent_activities.sort(key=lambda x: x['created_at'], reverse=True)
    recent_activities = recent_activities[:5]  # Show only 5 most recent
    
    context = {
        'user': request.user,
        'proposal_count': proposal_count,
        'coverletter_count': coverletter_count,
        'gig_count': gig_count,
        'pricing_count': pricing_count,
        'reply_count': reply_count,  
        'invoice_count': invoice_count,  
        'contract_count': contract_count,
        'recent_activities': recent_activities,
    }
    return render(request, 'accounts/dashboard.html', context)

@login_required
def profile_view(request):
    """View user profile"""
    return render(request, 'accounts/profile.html', {'user': request.user})

@login_required
def profile_edit(request):
    """Edit user profile"""
    profile = request.user.profile
    
    if request.method == 'POST':
        # Update user fields
        request.user.first_name = request.POST.get('first_name', '')
        request.user.last_name = request.POST.get('last_name', '')
        request.user.email = request.POST.get('email', '')
        request.user.save()
        
        # Update profile fields
        profile.bio = request.POST.get('bio', '')
        profile.skills = request.POST.get('skills', '')
        profile.hourly_rate = request.POST.get('hourly_rate', 0)
        profile.portfolio_url = request.POST.get('portfolio_url', '')
        profile.theme = request.POST.get('theme', 'light')
        profile.email_notifications = request.POST.get('email_notifications') == 'on'
        profile.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    
    return render(request, 'accounts/profile_edit.html', {'user': request.user})

@login_required
def change_password(request):
    """Change user password"""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keep user logged in
            messages.success(request, 'Password changed successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'accounts/change_password.html', {'form': form})

@login_required
def settings_view(request):
    """View settings page"""
    return render(request, 'accounts/settings.html', {'user': request.user})

@login_required
def settings_update(request):
    """Update settings"""
    if request.method == 'POST':
        profile = request.user.profile
        
        # Theme settings
        theme = request.POST.get('theme', 'light')
        if theme in ['light', 'dark']:
            profile.theme = theme
        
        # Notification settings
        profile.email_notifications = request.POST.get('email_notifications') == 'on'
        
        # API Key settings (store in environment or profile)
        api_key = request.POST.get('api_key', '')
        if api_key:
            profile.api_key = api_key  
        
        profile.save()
        
        messages.success(request, 'Settings updated successfully!')
        return redirect('settings')
    
    return redirect('settings')