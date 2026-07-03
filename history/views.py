from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from proposals.models import Proposal
from coverletters.models import CoverLetter
from gigs.models import GigDescription
from pricing.models import PricingHistory
from replies.models import ClientReply
from invoices.models import Invoice
from contracts.models import Contract

@login_required
def history_view(request):
    # Get all items for the current user
    proposals = Proposal.objects.filter(user=request.user)
    coverletters = CoverLetter.objects.filter(user=request.user)
    gigs = GigDescription.objects.filter(user=request.user)
    pricing = PricingHistory.objects.filter(user=request.user)
    replies = ClientReply.objects.filter(user=request.user)
    invoices = Invoice.objects.filter(user=request.user)
    contracts = Contract.objects.filter(user=request.user)
    
    # Get filter parameter
    filter_type = request.GET.get('type', 'all')
    
    # Prepare data for template
    all_items = []
    
    for p in proposals:
        all_items.append({
            'type': 'proposal',
            'title': p.project_title,
            'subtitle': f"Client: {p.client_name}",
            'created_at': p.created_at,
            'url': f'/proposals/{p.pk}/',
            'delete_url': f'/proposals/{p.pk}/delete/',
            'status': 'Generated' if p.generated_content else 'Draft',
            'icon': 'fa-file-alt',
            'color': 'primary'
        })
    
    for c in coverletters:
        all_items.append({
            'type': 'coverletter',
            'title': c.job_title,
            'subtitle': f"Company: {c.company_name}",
            'created_at': c.created_at,
            'url': f'/coverletters/{c.pk}/',
            'delete_url': f'/coverletters/{c.pk}/delete/',
            'status': 'Generated' if c.generated_content else 'Draft',
            'icon': 'fa-envelope',
            'color': 'success'
        })
    
    for g in gigs:
        all_items.append({
            'type': 'gig',
            'title': g.service_category,
            'subtitle': f"Level: {g.get_experience_level_display()}",
            'created_at': g.created_at,
            'url': f'/gigs/{g.pk}/',
            'delete_url': f'/gigs/{g.pk}/delete/',
            'status': 'Generated' if g.generated_description else 'Draft',
            'icon': 'fa-briefcase',
            'color': 'info'
        })
    
    for pr in pricing:
        all_items.append({
            'type': 'pricing',
            'title': f"${pr.suggested_price}",
            'subtitle': f"Complexity: {pr.get_complexity_display()}",
            'created_at': pr.created_at,
            'url': f'/pricing/{pr.pk}/',
            'delete_url': f'/pricing/{pr.pk}/delete/',
            'status': 'Calculated',
            'icon': 'fa-calculator',
            'color': 'warning'
        })
    
    for r in replies:
        all_items.append({
            'type': 'reply',
            'title': r.client_message[:50] + '...' if len(r.client_message) > 50 else r.client_message,
            'subtitle': f"Tone: {r.get_tone_display()}",
            'created_at': r.created_at,
            'url': f'/replies/{r.pk}/',
            'delete_url': f'/replies/{r.pk}/delete/',
            'status': 'Generated' if r.generated_reply else 'Draft',
            'icon': 'fa-comment-dots',
            'color': 'secondary'
        })
    
    for i in invoices:
        all_items.append({
            'type': 'invoice',
            'title': i.invoice_number,
            'subtitle': f"Client: {i.client_name} - ${i.total_amount}",
            'created_at': i.created_at,
            'url': f'/invoices/{i.pk}/',
            'delete_url': f'/invoices/{i.pk}/delete/',
            'status': i.get_status_display(),
            'icon': 'fa-file-invoice',
            'color': 'danger'
        })
    
    for con in contracts:
        all_items.append({
            'type': 'contract',
            'title': con.contract_number,
            'subtitle': f"Client: {con.client_name}",
            'created_at': con.created_at,
            'url': f'/contracts/{con.pk}/',
            'delete_url': f'/contracts/{con.pk}/delete/',
            'status': con.get_status_display(),
            'icon': 'fa-file-contract',
            'color': 'dark'
        })
    
    # Sort by created_at (newest first)
    all_items.sort(key=lambda x: x['created_at'], reverse=True)
    
    # Filter by type if specified
    if filter_type != 'all':
        all_items = [item for item in all_items if item['type'] == filter_type]
    
    context = {
        'items': all_items,
        'filter_type': filter_type,
        'total_count': len(all_items),
    }
    
    return render(request, 'history/history.html', context)