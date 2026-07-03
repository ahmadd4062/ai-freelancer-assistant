from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import PricingHistory
from utils.ai_helper import generate_pricing_suggestions

@login_required
def pricing_list(request):
    pricings = PricingHistory.objects.filter(user=request.user)
    return render(request, 'pricing/list.html', {'pricings': pricings})

@login_required
def pricing_calculator(request):
    result = None
    ai_suggestions = None
    
    if request.method == 'POST':
        # Get form data
        hourly_rate = float(request.POST.get('hourly_rate', 0))
        estimated_hours = float(request.POST.get('estimated_hours', 0))
        complexity = request.POST.get('complexity', 'medium')
        urgency = request.POST.get('urgency', 'normal')
        additional_charges = float(request.POST.get('additional_charges', 0))
        tax = float(request.POST.get('tax', 0))
        
        # Calculate pricing
        base_price = hourly_rate * estimated_hours
        
        # Complexity multiplier
        complexity_multipliers = {'low': 1.0, 'medium': 1.3, 'high': 1.6}
        complexity_mult = complexity_multipliers.get(complexity, 1.0)
        
        # Urgency multiplier
        urgency_multipliers = {'normal': 1.0, 'urgent': 1.2, 'very_urgent': 1.5}
        urgency_mult = urgency_multipliers.get(urgency, 1.0)
        
        # Total calculation
        subtotal = base_price * complexity_mult * urgency_mult
        total = subtotal + additional_charges + tax
        
        # Save to database
        pricing = PricingHistory.objects.create(
            user=request.user,
            hourly_rate=hourly_rate,
            estimated_hours=estimated_hours,
            complexity=complexity,
            urgency=urgency,
            additional_charges=additional_charges,
            tax=tax,
            suggested_price=total
        )
        
        # Get AI suggestions (if user has credits)
        if request.user.profile.ai_credits > 0:
            ai_suggestions = generate_pricing_suggestions(pricing)
            pricing.market_analysis = ai_suggestions.get('market_analysis', '')
            pricing.service_tips = ai_suggestions.get('service_tips', '')
            pricing.recommended_delivery = ai_suggestions.get('recommended_delivery', '')
            pricing.save()
            
            # Deduct 1 AI credit
            request.user.profile.ai_credits -= 1
            request.user.profile.save()
        
        result = {
            'pricing': pricing,
            'base_price': base_price,
            'complexity_mult': complexity_mult,
            'urgency_mult': urgency_mult,
            'subtotal': subtotal,
            'total': total,
            'ai_suggestions': ai_suggestions
        }
        
        messages.success(request, 'Pricing calculated successfully!')
        
    return render(request, 'pricing/calculator.html', {'result': result})

@login_required
def pricing_detail(request, pk):
    pricing = get_object_or_404(PricingHistory, pk=pk, user=request.user)
    return render(request, 'pricing/detail.html', {'pricing': pricing})

@login_required
def pricing_delete(request, pk):
    pricing = get_object_or_404(PricingHistory, pk=pk, user=request.user)
    if request.method == 'POST':
        pricing.delete()
        messages.success(request, 'Pricing record deleted successfully!')
        return redirect('pricing_list')
    return render(request, 'pricing/delete.html', {'pricing': pricing})